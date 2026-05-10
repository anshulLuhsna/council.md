#!/usr/bin/env python3
"""
council.md CLI — Python implementation
No API keys. No network. No LLM calls. Just file scaffolding and validation.

Usage:
    council init [profile] [dir]    Scaffold a new council from a profile
    council status [dir]            Show current phase and contribution status
    council next [dir]              Print what to do next
    council validate [--strict] [dir]  Check files (strict = CI-style errors)
    council summary [dir]           Generate optional summary.html from synthesizer.md UI data
    council remind [dir]            Post-decision review due / overdue (synthesizer.md)
    council help                    Show this message
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_DIR = Path("./council")

VALID_STATUSES = {"open", "contributing", "synthesizing", "decided", "archived"}
VALID_PROFILES = {"decision", "review", "planning", "self-improvement"}
PLACEHOLDER_MODELS = frozenset({"", "replace-me", '""', "''"})


class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def ok(msg):    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")
def warn(msg):  print(f"{Colors.YELLOW}⚠{Colors.RESET}  {msg}")
def err(msg):   print(f"{Colors.RED}✗{Colors.RESET}  {msg}")
def info(msg):  print(f"{Colors.BLUE}→{Colors.RESET} {msg}")
def bold(msg):  print(f"{Colors.BOLD}{msg}{Colors.RESET}")


def require_council_dir(council_dir: Path):
    if not council_dir.is_dir():
        err(f"Council directory not found: {council_dir}")
        info(f"Run 'council init [profile] {council_dir}' to scaffold a new council.")
        sys.exit(1)


def get_votes_status(votes_path: Path) -> str:
    if not votes_path.exists():
        return "unknown"
    content = votes_path.read_text()
    match = re.search(r"^status:\s*[\"']?(\w+)[\"']?", content, re.MULTILINE)
    return match.group(1) if match else "unknown"


def yaml_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---\n", 3)
    if end == -1:
        return ""
    return text[3:end]


def parse_frontmatter_bool(yaml_block: str, key: str) -> bool | None:
    m = re.search(rf"^{re.escape(key)}:\s*(true|false)\s*$", yaml_block, re.MULTILINE | re.IGNORECASE)
    if not m:
        return None
    return m.group(1).lower() == "true"


def parse_session_mode(yaml_block: str) -> str | None:
    m = re.search(r"^session_mode:\s*[\"']?(\w+)[\"']?", yaml_block, re.MULTILINE)
    return m.group(1) if m else None


def parse_lock_ttl_hours(yaml_block: str) -> float:
    m = re.search(r"^  ttl_hours:\s*([0-9.]+)\s*$", yaml_block, re.MULTILINE)
    if m:
        return float(m.group(1))
    return 24.0


def parse_lock_acquired_at(yaml_block: str) -> str:
    m = re.search(r"^  acquired_at:\s*[\"']?([^\"'\n]+)[\"']?\s*$", yaml_block, re.MULTILINE)
    return m.group(1).strip() if m else ""


def lock_expired(yaml_block: str) -> bool:
    """True if acquired_at parses and is older than ttl_hours (default 24)."""
    raw = parse_lock_acquired_at(yaml_block)
    if not raw:
        return False
    ttl = parse_lock_ttl_hours(yaml_block)
    try:
        ts = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return False
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) > ts + timedelta(hours=ttl)


def normalize_agent_heading(raw_title: str) -> str:
    """Strip deprecated ` — Round N` suffix so one logical agent maps to one name."""
    t = raw_title.strip()
    m = re.match(r"^(.+?)\s*[—\-]\s*Round\s+\d+\s*$", t, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return t


def iter_agent_sections(discussion_text: str):
    heads = list(re.finditer(r"^### Agent:\s*(.+)$", discussion_text, re.MULTILINE))
    for i, m in enumerate(heads):
        title = m.group(1).strip()
        start_body = m.end()
        end_body = heads[i + 1].start() if i + 1 < len(heads) else len(discussion_text)
        yield normalize_agent_heading(title), title, discussion_text[start_body:end_body]


def parse_registered_agents(yaml_block: str) -> list[dict[str, str]]:
    """Minimal YAML subset for registered_agents list items."""
    agents: list[dict[str, str]] = []
    lines = yaml_block.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("registered_agents:"):
            i += 1
            current: dict[str, str] = {}
            while i < len(lines):
                raw = lines[i]
                stripped = raw.strip()
                if (
                    raw
                    and not raw[0].isspace()
                    and re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*", raw)
                    and not stripped.startswith("-")
                ):
                    break
                if stripped.startswith("- name:"):
                    if current.get("name"):
                        agents.append(current)
                    current = {"name": stripped.split(":", 1)[1].strip().strip('"\'')}
                elif stripped.startswith("model:") and current:
                    current["model"] = stripped.split(":", 1)[1].strip().strip('"\'')
                elif stripped.startswith("participation:") and current:
                    current["participation"] = stripped.split(":", 1)[1].strip().strip('"\'')
                i += 1
            if current.get("name"):
                agents.append(current)
            break
        i += 1
    return agents


def registered_agent_names(votes_path: Path) -> list[str]:
    if not votes_path.exists():
        return []
    return [a["name"] for a in parse_registered_agents(yaml_frontmatter(votes_path.read_text()))]


def agent_section_body(discussion_text: str, agent_name: str) -> str:
    """All bodies for this logical agent (canonical block + deprecated `— Round N` heading)."""
    parts: list[str] = []
    for base, _title, body in iter_agent_sections(discussion_text):
        if base == agent_name:
            parts.append(body)
    return "".join(parts)


def agent_has_contributed(discussion_text: str, agent_name: str) -> bool:
    body = agent_section_body(discussion_text, agent_name)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).strip()
    if not body:
        return False
    low = body.lower()
    if "has not yet contributed" in low:
        return False
    if re.search(r"<!--[^>]*pending[^>]*-->", body, re.IGNORECASE):
        return False
    return True


def synthesis_chunk_substantive(chunk: str) -> bool:
    """True if synthesis section has real content, not only [TBD…] placeholders."""
    chunk = re.sub(r"<!--.*?-->", "", chunk, flags=re.DOTALL)
    lines: list[str] = []
    for line in chunk.splitlines():
        s = line.strip()
        if not s:
            continue
        if re.match(r"^\[TBD", s, re.IGNORECASE):
            continue
        if re.match(r"^[\*_\-]+$", s):
            continue
        lines.append(line)
    text = "\n".join(lines).strip()
    return len(text) > 50


def synthesis_in_synthesizer(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text()
    if not re.search(r"^## Council Synthesis\s*$", text, re.MULTILINE):
        return False
    rest = text.split("## Council Synthesis", 1)[1]
    chunk = rest.split("## Human Decision", 1)[0]
    if "## Rules you must follow" in chunk:
        chunk = chunk.split("## Rules you must follow", 1)[0]
    return synthesis_chunk_substantive(chunk)


def discussion_strict_normative_violations(d_text: str) -> list[str]:
    """SPEC-core §2 checks automatable from discussion.md (strict mode)."""
    errs: list[str] = []
    if re.search(r"^##\s+Human Decision\s*$", d_text, re.MULTILINE):
        errs.append("discussion.md must not contain ## Human Decision (SPEC-core §2) — use synthesizer.md only")
    heads = list(re.finditer(r"^### Agent:\s*(.+)$", d_text, re.MULTILINE))
    for i, _m in enumerate(heads):
        start = heads[i].end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(d_text)
        block = d_text[start:end]
        for ln in block.splitlines():
            if re.match(r"^##\s+\S", ln):
                errs.append(
                    f"Under ### Agent: … found {ln.strip()[:70]} — use #### subsections, not ## (SPEC-core §2)"
                )
                break
    return errs


def deprecated_round2_heading_present(d_text: str) -> bool:
    return bool(re.search(r"^### Agent:\s*.+[—\-]\s*Round\s+\d+\s*$", d_text, re.MULTILINE))


def extract_post_decision_review_section(synth_text: str) -> str:
    m = re.search(r"^## Post-Decision Review\s*$", synth_text, re.MULTILINE)
    if not m:
        return ""
    tail = synth_text[m.end() :]
    nxt = re.search(r"^## [^\s]", tail, re.MULTILINE)
    return tail[: nxt.start()] if nxt else tail


def extract_markdown_h2_section(text: str, heading: str) -> str:
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not m:
        return ""
    tail = text[m.end() :]
    nxt = re.search(r"^## [^\s]", tail, re.MULTILINE)
    return tail[: nxt.start()] if nxt else tail


def extract_summary_ui_json(synth_text: str) -> tuple[dict | None, str | None]:
    sec = extract_markdown_h2_section(synth_text, "Summary UI Data")
    if not sec.strip():
        return None, "Missing `## Summary UI Data` section in synthesizer.md"
    fence = re.search(r"```json\s*(\{.*?\})\s*```", sec, re.DOTALL)
    if not fence:
        return None, "Missing fenced ```json block under `## Summary UI Data`"
    try:
        return json.loads(fence.group(1)), None
    except json.JSONDecodeError as exc:
        return None, f"Malformed JSON in `## Summary UI Data`: {exc}"


def validate_summary_payload(data: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["Summary UI data must be a JSON object"]

    required_top = ["session", "overview", "agents", "agreements", "conflicts", "openQuestions"]
    for key in required_top:
        if key not in data:
            errs.append(f"Missing top-level key: {key}")

    session = data.get("session")
    if not isinstance(session, dict):
        errs.append("session must be an object")
    else:
        for key in ("title", "type", "synthesisConfidence"):
            if not isinstance(session.get(key), str) or not session.get(key, "").strip():
                errs.append(f"session.{key} must be a non-empty string")

    overview = data.get("overview")
    if not isinstance(overview, dict):
        errs.append("overview must be an object")
    else:
        for key in ("primaryQuestion", "primaryTension", "nonRecommendationCopy"):
            if not isinstance(overview.get(key), str) or not overview.get(key, "").strip():
                errs.append(f"overview.{key} must be a non-empty string")
        if not isinstance(overview.get("executiveBrief"), list) or not overview.get("executiveBrief"):
            errs.append("overview.executiveBrief must be a non-empty array")

    if not isinstance(data.get("agents"), list) or not data.get("agents"):
        errs.append("agents must be a non-empty array")
    if not isinstance(data.get("agreements"), list):
        errs.append("agreements must be an array")
    if not isinstance(data.get("conflicts"), list):
        errs.append("conflicts must be an array")
    if not isinstance(data.get("openQuestions"), list):
        errs.append("openQuestions must be an array")
    if "topKillRisks" in data and not isinstance(data.get("topKillRisks"), list):
        errs.append("topKillRisks must be an array when present")
    if "candidatePaths" in data and not isinstance(data.get("candidatePaths"), list):
        errs.append("candidatePaths must be an array when present")
    if "candidateOptions" in data and not isinstance(data.get("candidateOptions"), list):
        errs.append("candidateOptions must be an array when present")

    return errs


def normalize_summary_payload(data: dict) -> dict:
    out = dict(data)
    if "candidatePaths" not in out and "candidateOptions" in out:
        out["candidatePaths"] = out["candidateOptions"]
    out.setdefault("topKillRisks", [])
    out.setdefault("candidatePaths", [])
    return out


def render_summary_html(template_text: str, payload: dict) -> str:
    json_text = json.dumps(payload, indent=2, ensure_ascii=False)
    replacement = f'<script type="application/json" id="council-summary">\n{json_text}\n  </script>'
    rendered = re.sub(
        r'<script type="application/json" id="council-summary">.*?</script>',
        replacement,
        template_text,
        count=1,
        flags=re.DOTALL,
    )
    if rendered == template_text:
        raise ValueError("Template missing council-summary JSON block")
    return rendered


def parse_scheduled_review_date(section: str) -> datetime | None:
    for pat in (
        r"\*\*Scheduled review date:\*\*\s*(\d{4}-\d{2}-\d{2})",
        r"\*\*Review date:\*\*\s*(\d{4}-\d{2}-\d{2})",
    ):
        m = re.search(pat, section)
        if m:
            try:
                return datetime.fromisoformat(m.group(1)).replace(tzinfo=timezone.utc)
            except ValueError:
                return None
    return None


def outcome_observed_filled(section: str) -> bool:
    idx = section.find("**Outcome observed:**")
    if idx < 0:
        return False
    rest = section[idx + len("**Outcome observed:**") :]
    nxt = re.search(r"^\*\*", rest, re.MULTILINE)
    chunk = rest[: nxt.start()] if nxt else rest
    chunk = chunk.strip()
    if not chunk:
        return False
    low = chunk.lower()
    if low in ("[tbd]", "tbd", "…", "...", "*"):
        return False
    return True


# ─── INIT ────────────────────────────────────────────────────────────────────

def cmd_init(args):
    profile = args.profile if args.profile else "decision"
    target = Path(args.dir) if args.dir else DEFAULT_DIR

    if profile not in VALID_PROFILES:
        err(f"Profile '{profile}' not found. Available profiles: {', '.join(sorted(VALID_PROFILES))}")
        sys.exit(1)

    profile_dir = REPO_ROOT / "profiles" / profile

    if not profile_dir.is_dir():
        err(f"Profile directory not found: {profile_dir}")
        sys.exit(1)

    if target.exists():
        warn(f"Directory '{target}' already exists.")
        confirm = input("Overwrite? [y/N] ").strip().lower()
        if confirm != "y":
            info("Aborted.")
            sys.exit(0)
        shutil.rmtree(target)

    shutil.copytree(profile_dir, target)
    ok(f"Council scaffolded from '{profile}' profile → {target}")
    print()
    info("Next step:")
    print(f"  Open {target}/coordinator.md in your AI model of choice.")
    print("  Answer the coordinator's questions.")
    print()
    info("See docs/how-it-works.md and SPEC-rules §6 (drafts/ blind workflow).")


# ─── STATUS ──────────────────────────────────────────────────────────────────

def cmd_status(args):
    council_dir = Path(args.dir) if args.dir else DEFAULT_DIR
    require_council_dir(council_dir)

    bold(f"Council status: {council_dir}")
    print()

    votes_path = council_dir / "votes.md"
    if votes_path.exists():
        content = votes_path.read_text()
        status_match = re.search(r"^status:\s*[\"']?(\w+)[\"']?", content, re.MULTILINE)
        quorum_match = re.search(r"^quorum_rule:\s*[\"']?(\S+)[\"']?", content, re.MULTILINE)
        sm_match = re.search(r"^session_mode:\s*[\"']?(\w+)[\"']?", content, re.MULTILINE)
        status = status_match.group(1) if status_match else "unknown"
        quorum = quorum_match.group(1).rstrip('"\'') if quorum_match else "not set"
        sm = sm_match.group(1) if sm_match else "not set"
        print(f"  Phase:         {Colors.BOLD}{status}{Colors.RESET}")
        print(f"  Quorum rule:   {quorum}")
        print(f"  Session mode:  {sm}")
        lock_h = re.search(r"^  holder:\s*[\"']?([^\"'\n]*)[\"']?", content, re.MULTILINE)
        if lock_h:
            print(f"  Lock holder:   {lock_h.group(1) or '(none)'}")
        yb = yaml_frontmatter(content)
        if lock_h and lock_h.group(1) and lock_expired(yb):
            warn("  Lock appears expired (acquired_at + ttl_hours) — any human may clear (SPEC-rules §12)")
    else:
        warn("votes.md not found — has the council been initialized?")

    print()

    discussion_path = council_dir / "discussion.md"
    votes_txt = votes_path.read_text() if votes_path.exists() else ""
    agents_spec = registered_agent_names(votes_path) if votes_path.exists() else []

    if discussion_path.exists():
        bold("Agent contributions:")
        d_content = discussion_path.read_text()
        if agents_spec:
            names = agents_spec
        else:
            raw_names = re.findall(r"^### Agent:\s*(.+)$", d_content, re.MULTILINE)
            seen: set[str] = set()
            names = []
            for raw in raw_names:
                base = normalize_agent_heading(raw.strip())
                if base not in seen:
                    seen.add(base)
                    names.append(base)
        for name in names:
            if agent_has_contributed(d_content, name):
                ok(f"  {name} — contributed")
            else:
                warn(f"  {name} — not yet contributed")

        print()
        syn_path = council_dir / "synthesizer.md"
        if synthesis_in_synthesizer(syn_path):
            ok("Council synthesis (synthesizer.md): present")
        else:
            warn("Council synthesis (synthesizer.md): missing or empty under ## Council Synthesis")


# ─── NEXT ─────────────────────────────────────────────────────────────────────

def cmd_next(args):
    council_dir = Path(args.dir) if args.dir else DEFAULT_DIR
    require_council_dir(council_dir)

    status = get_votes_status(council_dir / "votes.md")

    bold("What to do next:")
    print()

    if status == "open":
        info("The council is open. Run the coordinator to set up the session.")
        print(f"  1. Open {council_dir}/coordinator.md")

    elif status == "contributing":
        info("Agents are contributing. Use drafts/ for blind rounds (SPEC-rules §6).")
        discussion_path = council_dir / "discussion.md"
        votes_path = council_dir / "votes.md"
        if discussion_path.exists() and votes_path.exists():
            d_content = discussion_path.read_text()
            for name in registered_agent_names(votes_path):
                if not agent_has_contributed(d_content, name):
                    warn(f"  {name} — not yet contributed (merge from drafts/ when ready)")

    elif status == "synthesizing":
        info("Deliberation closed. Run the synthesizer.")
        print("  Fill ## Council Synthesis in synthesizer.md only (not discussion.md).")
        print("  Inputs: context.md + discussion.md + votes.md + synthesizer.md")
        print("  Optional: also fill ## Summary UI Data so you can generate summary.html.")

    elif status == "decided":
        ok("Decision recorded.")
        print("  Optional: run `council summary` to generate summary.html from synthesizer.md.")
        print("  Then archive when you are done.")

    elif status == "archived":
        ok("Session archived.")

    else:
        warn(f"Unknown status: {status}")

    print()


# ─── REMIND ──────────────────────────────────────────────────────────────────

def cmd_remind(args):
    council_dir = Path(args.dir) if args.dir else DEFAULT_DIR
    require_council_dir(council_dir)

    votes_path = council_dir / "votes.md"
    synth_path = council_dir / "synthesizer.md"
    status = get_votes_status(votes_path)

    bold(f"Post-decision review: {council_dir}")
    print()

    if status not in ("decided", "archived"):
        info(
            f"Phase is `{status}` — calendar review is most meaningful after `status: decided` "
            "(you can still set **Scheduled review date:** early)."
        )
        print()

    if not synth_path.exists():
        err("synthesizer.md not found")
        sys.exit(1)

    stext = synth_path.read_text()
    sec = extract_post_decision_review_section(stext)
    if not sec.strip():
        warn("No ## Post-Decision Review section — add from templates/synthesizer.md (docs/eval.md).")
        sys.exit(0)

    due = parse_scheduled_review_date(sec)
    if not due:
        warn("Set **Scheduled review date:** YYYY-MM-DD under ## Post-Decision Review (calendar hook).")
        sys.exit(0)

    today = datetime.now(timezone.utc).date()
    due_d = due.date()
    filled = outcome_observed_filled(sec)

    print(f"  Scheduled review date: {due_d.isoformat()}")
    print(f"  Outcome observed filled: {'yes' if filled else 'no'}")
    print()

    if filled:
        ok("Review section looks filled — optional follow-up only.")
        return

    if due_d < today:
        warn(f"OVERDUE — scheduled date was {due_d.isoformat()}; fill **Outcome observed:** when ready.")
    elif due_d == today:
        warn("Due today — fill **Outcome observed:** when you have signal.")
    else:
        info(f"Not yet due (in {(due_d - today).days} days).")


# ─── SUMMARY ─────────────────────────────────────────────────────────────────

def cmd_summary(args):
    council_dir = Path(args.dir) if args.dir else DEFAULT_DIR
    require_council_dir(council_dir)

    synth_path = council_dir / "synthesizer.md"
    if not synth_path.exists():
        err("synthesizer.md not found")
        sys.exit(1)

    template_path = REPO_ROOT / "ui" / "public" / "summary.html"
    if not template_path.exists():
        err(f"Summary template not found: {template_path}")
        sys.exit(1)

    payload, parse_err = extract_summary_ui_json(synth_path.read_text())
    if parse_err:
        err(parse_err)
        info("Add a valid `## Summary UI Data` section to synthesizer.md, then rerun `council summary`.")
        sys.exit(1)

    assert payload is not None
    validation_errors = validate_summary_payload(payload)
    if validation_errors:
        err("Summary UI data is incomplete:")
        for msg in validation_errors:
            err(f"  {msg}")
        sys.exit(1)

    payload = normalize_summary_payload(payload)
    html = render_summary_html(template_path.read_text(), payload)
    out_path = council_dir / "summary.html"
    out_path.write_text(html)
    ok(f"Generated {out_path}")
    info("This artifact is optional and non-authoritative. Source of truth remains synthesizer.md + session markdown.")


# ─── VALIDATE ────────────────────────────────────────────────────────────────

def cmd_validate(args):
    council_dir = Path(args.dir) if args.dir else DEFAULT_DIR
    require_council_dir(council_dir)

    strict = getattr(args, "strict", False)

    bold(f"Validating council: {council_dir}")
    if strict:
        info("Strict mode ON — SPEC-core §2-oriented checks fail as errors (SPEC-core §3).")
    print()

    errors = 0
    warnings = 0

    required_files = ["coordinator.md", "context.md", "discussion.md", "votes.md", "synthesizer.md"]
    for fname in required_files:
        if (council_dir / fname).exists():
            ok(f"{fname} exists")
        else:
            err(f"{fname} is missing")
            errors += 1

    agents_dir = council_dir / "agents"
    if agents_dir.is_dir() and list(agents_dir.glob("*.md")):
        ok(f"agents/ — {len(list(agents_dir.glob('*.md')))} agent file(s) found")
    else:
        err("agents/ — no agent files found")
        errors += 1

    print()

    votes_path = council_dir / "votes.md"
    votes_text = votes_path.read_text() if votes_path.exists() else ""

    if votes_path.exists():
        bold("Checking votes.md:")
        st = get_votes_status(votes_path)
        if st in VALID_STATUSES:
            ok(f"  status: {st} (valid)")
        else:
            err(f"  status: '{st}' is not a valid phase")
            errors += 1

        if "registered_agents:" in votes_text:
            ok("  registered_agents block found")
        else:
            warn("  registered_agents block not found")
            warnings += 1

        if re.search(r"^##\s+Current Phase\s*:", votes_text, re.MULTILINE):
            if strict:
                err("  Remove duplicate '## Current Phase' — use only YAML status: (SPEC-core §5)")
                errors += 1
            else:
                warn("  Remove duplicate '## Current Phase' — use only YAML status: (SPEC-core §5)")
                warnings += 1

        agents = parse_registered_agents(yaml_frontmatter(votes_text))
        yb = yaml_frontmatter(votes_text)
        session_mode = parse_session_mode(yb) or ""
        attested = parse_frontmatter_bool(yb, "distinct_underlying_models_attested")
        for ag in agents:
            m = ag.get("model", "")
            if m in PLACEHOLDER_MODELS or not m:
                if strict:
                    err(f"  model: for '{ag.get('name')}' must be non-empty (SPEC-rules §4.5)")
                    errors += 1
                else:
                    warn(f"  model: for '{ag.get('name')}' must be non-empty (SPEC-rules §4.5)")
                    warnings += 1
        distinct_models = {a.get("model", "").strip() for a in agents if a.get("model")}
        distinct_models.discard("")
        if len(distinct_models) >= 2:
            ok(
                "  Two+ distinct model: strings — weak diversity signal "
                "(strings ≠ distinct backends; SPEC-rules §4.5)"
            )
            if session_mode == "council" and attested is False:
                warn(
                    "  distinct_underlying_models_attested is false — treat agent votes as "
                    "advisory unless humans confirm transitions (SPEC-rules §4.5)"
                )
            elif session_mode == "council" and attested is True:
                ok("  distinct_underlying_models_attested: true — human attestation recorded")
        elif agents:
            warn(
                "  Fewer than two distinct model: values — use session_mode: rehearsal "
                "or expect advisory votes (SPEC-rules §4.5)"
            )

        if re.search(r"^##\s+Motion:", votes_text, re.MULTILINE):
            if strict:
                err("  Use ### Motion: under ## Phase Transition Log (SPEC-rules §7), not ## Motion:")
                errors += 1
            else:
                warn("  Prefer ### Motion: under ## Phase Transition Log (SPEC-rules §7), not ## Motion:")
                warnings += 1

        yb_lock = yaml_frontmatter(votes_text)
        lock_holder_m = re.search(r"^  holder:\s*[\"']?([^\"'\n]*)[\"']?", votes_text, re.MULTILINE)
        if lock_holder_m and lock_holder_m.group(1).strip():
            if not parse_lock_acquired_at(yb_lock):
                warn(
                    "  lock.holder set but acquired_at empty — advisory lock until reconciled "
                    "(SPEC-rules §12)"
                )
                warnings += 1

    print()

    discussion_path = council_dir / "discussion.md"
    if discussion_path.exists():
        bold("Checking discussion.md:")
        d_text = discussion_path.read_text()
        if re.search(r"^##\s+Synthesis\b", d_text, re.MULTILINE):
            err("  legacy ## Synthesis / synthesis content must not live in discussion.md (SPEC-rules §8) — use synthesizer.md")
            errors += 1
        if re.search(r"^##\s+Council Synthesis\b", d_text, re.MULTILINE):
            err("  ## Council Synthesis must be only in synthesizer.md")
            errors += 1
        if re.search(r"^### Agent:", d_text, re.MULTILINE):
            ok("  ### Agent: heading(s) found")
        else:
            warn("  No ### Agent: sections found")
            warnings += 1

        if deprecated_round2_heading_present(d_text):
            msg = (
                "  Deprecated `### Agent: … — Round N` heading — merge into one block "
                "(SPEC-rules §5c; tooling will reject new uses in v0.3)"
            )
            if strict:
                err(msg)
                errors += 1
            else:
                warn(msg)
                warnings += 1

        if strict:
            for msg in discussion_strict_normative_violations(d_text):
                err(f"  {msg}")
                errors += 1

    print()

    synth_path = council_dir / "synthesizer.md"
    if synth_path.exists():
        bold("Checking synthesizer.md:")
        stext = synth_path.read_text()
        if re.search(r"^## Council Synthesis\s*$", stext, re.MULTILINE):
            ok("  ## Council Synthesis section present")
            if synthesis_in_synthesizer(synth_path):
                ok("  ## Council Synthesis has body text")
            else:
                warn("  ## Council Synthesis is empty or placeholder")
                warnings += 1
        else:
            err("  ## Council Synthesis missing (SPEC-rules §8)")
            errors += 1
        if re.search(r"^## Human Decision\s*$", stext, re.MULTILINE):
            ok("  ## Human Decision present")
        else:
            warn("  ## Human Decision missing")
            warnings += 1

    print()

    context_path = council_dir / "context.md"
    if context_path.exists():
        bold("Checking context.md:")
        c_text = context_path.read_text()
        if re.search(r"^## Question", c_text, re.MULTILINE):
            ok("  ## Question section found")
        else:
            warn("  ## Question section missing")
            warnings += 1

    print()

    if agents_dir.is_dir():
        bold("Checking agent files:")
        for agent_file in agents_dir.glob("*.md"):
            content = agent_file.read_text()
            has_name = bool(re.search(r"^name:", content, re.MULTILINE))
            has_role = bool(re.search(r"^role:", content, re.MULTILINE))
            if has_name and has_role:
                ok(f"  {agent_file.name} — frontmatter ok")
            else:
                warn(f"  {agent_file.name} — missing name: or role: in frontmatter")
                warnings += 1

    print()
    bold("Validation summary:")
    if errors == 0 and warnings == 0:
        ok("All checks passed. Council is ready.")
    elif errors == 0:
        ok(f"No errors. {warnings} warning(s).")
        warn("Review warnings above before proceeding.")
    else:
        err(f"{errors} error(s), {warnings} warning(s).")
        print("  Fix errors before running the council.")
        sys.exit(1)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="council",
        description="council.md CLI — no API keys, no network, just files",
        add_help=False,
    )
    subparsers = parser.add_subparsers(dest="command")

    p_init = subparsers.add_parser("init", help="Scaffold a new council from a profile")
    p_init.add_argument("profile", nargs="?", default="decision",
                        help="Profile: decision, review, planning, self-improvement")
    p_init.add_argument("dir", nargs="?", default=None,
                        help="Target directory (default: ./council)")

    p_status = subparsers.add_parser("status", help="Show current phase and contributions")
    p_status.add_argument("dir", nargs="?", default=None)

    p_next = subparsers.add_parser("next", help="Print what to do next")
    p_next.add_argument("dir", nargs="?", default=None)

    p_validate = subparsers.add_parser(
        "validate",
        help="Validate files (strict → SPEC-core §2-oriented checks; see cli/README.md)",
    )
    p_validate.add_argument("--strict", action="store_true",
                            help="Treat SPEC-core §2-oriented issues as errors (CI; SPEC-core §3)")
    p_validate.add_argument("dir", nargs="?", default=None)

    p_summary = subparsers.add_parser(
        "summary",
        help="Generate optional summary.html from synthesizer.md UI data",
    )
    p_summary.add_argument("dir", nargs="?", default=None)

    p_remind = subparsers.add_parser(
        "remind",
        help="Post-decision review due / overdue (reads synthesizer.md)",
    )
    p_remind.add_argument("dir", nargs="?", default=None)

    subparsers.add_parser("help", help="Show this message")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "next":
        cmd_next(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "summary":
        cmd_summary(args)
    elif args.command == "remind":
        cmd_remind(args)
    elif args.command == "help" or args.command is None:
        print(__doc__)
    else:
        err(f"Unknown command: {args.command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
