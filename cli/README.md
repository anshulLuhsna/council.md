# council.md CLI

Lightweight helper for council.md sessions. No API keys, no network, no LLM calls.

The CLI scaffolds councils, tracks session state, and validates files. It never touches an AI model — that part is always you.

---

## Requirements

**Shell version (`council.sh`):** bash 4+ (macOS ships with bash 3 — use `brew install bash` or use the Python version)

**Python version (`council.py`):** Python 3.9+

---

## Installation

### Option 1: Run directly

```bash
# Shell
bash /path/to/council.md/cli/council.sh help

# Python
python3 /path/to/council.md/cli/council.py help
```

### Option 2: Add to PATH

```bash
# Add an alias to your shell config (~/.zshrc or ~/.bashrc)
alias council="python3 /path/to/council.md/cli/council.py"

# Or symlink
ln -s /path/to/council.md/cli/council.py /usr/local/bin/council
```

### Option 3: Run from repo root

```bash
cd /path/to/council.md
./cli/council.sh help
# or
python3 cli/council.py help
```

---

## Commands

### `council init [profile] [dir]`

Scaffold a new council from a profile template.

```bash
council init decision ./my-decision
council init review ./api-review
council init planning ./q3-plan
```

Profiles: `decision`, `review`, `planning`

If no directory is specified, creates `./council`.

After running `init`, open `coordinator.md` in your AI model of choice and start the session.

---

### `council status [dir]`

Show the current phase, which agents have contributed, and synthesis status.

```bash
council status
council status ./my-decision
```

Example output:
```
Council status: ./my-decision

  Phase:       contributing
  Quorum rule: simple_majority

Agent contributions:
✓  Strategist — contributed
⚠  Operator — not yet contributed
⚠  Risk Analyst — not yet contributed
✓  Challenger — contributed

⚠  Synthesis: not yet written
```

---

### `council next [dir]`

Print the next action to take in the current session.

```bash
council next
council next ./my-decision
```

Reads `votes.md` to determine the current phase and tells you exactly what to do. Useful when you come back to a session after a break.

---

### `council validate [--strict] [dir]`

Check required files, headings, frontmatter, and structural integrity.

```bash
council validate
council validate ./my-decision
council validate --strict ./my-decision
```

**Default:** heuristic checks; many issues are **warnings** so work-in-progress sessions still validate. Several warnings correspond to **SPEC-rules** (operational hygiene), not always **SPEC-core §2** violations.

**`--strict`:** promotes checks that map to **SPEC-core §2** (normative core) where detectable — duplicate narrative phase in `votes.md`, placeholder **`model:`**, wrong **`### Motion:`** level, forbidden **`##`** under **`### Agent:`**, **`## Human Decision`** in **`discussion.md`**, **`## Synthesis` / `## Council Synthesis`** in **`discussion.md`**. It may also treat selected **SPEC-rules** migration items as errors (e.g. deprecated **`### Agent: … — Round 2`** heading — **SPEC-rules §5c**). Intended for **CI** — see **SPEC-core §3**.

Checks (**SPEC-core** + **SPEC-rules** v0.2) include:

- Required files: `coordinator.md`, `context.md`, `discussion.md`, `votes.md`, `synthesizer.md`, `agents/*.md`
- `votes.md` YAML: valid `status:`, `registered_agents`, non-placeholder **`model:`** per agent (warns on `replace-me` unless `--strict`)
- Warns if duplicate `## Current Phase` exists in `votes.md` body (should use frontmatter only); **error under `--strict`**
- `discussion.md`: `### Agent:` headings; **errors** if `## Synthesis` / `## Council Synthesis` appears here
- `synthesizer.md`: **`## Council Synthesis`** present with body; **`## Human Decision`**
- `context.md`: `## Question`
- Agent files: `name:` and `role:` in frontmatter

The **`council.sh`** implementation delegates `validate`, `status`, `next`, and **`remind`** to **`council.py`** when `python3` is available.

Returns a non-zero exit code on errors (useful in CI or pre-session checks).

### `council summary [dir]`

Generate an optional session-local `summary.html` from the structured UI payload inside `synthesizer.md`.

```bash
council summary
council summary ./my-decision
```

Behavior:

- reads `## Summary UI Data` from `synthesizer.md`
- expects exactly one fenced `json` block in that section
- validates required keys
- injects the payload into the canonical standalone HTML template
- writes `summary.html` into the session root

If the UI data section is missing or malformed, the command fails clearly without affecting protocol compliance.

`summary.html` is optional and non-authoritative. The source of truth remains `discussion.md`, `synthesizer.md`, and `votes.md`.

---

### `council remind [dir]`

Reads **`## Post-Decision Review`** in **`synthesizer.md`** and compares **`Scheduled review date:`** to today. Warns if **overdue** and **`Outcome observed:`** is still empty — lightweight substitute for a calendar when humans forget the regret loop.

```bash
council remind
council remind ./my-decision
```

---

## Environment variable

Set `COUNCIL_DIR` to change the default council directory:

```bash
export COUNCIL_DIR=./my-project-council
council status
```

---

## Philosophy

The CLI is **optional** tooling. **Compliance is defined by [SPEC-core.md](../SPEC-core.md), [SPEC-rules.md](../SPEC-rules.md), and your markdown files**, not by this script (**SPEC-core §3**).

- **`validate`** (default) — convenience + warnings for incomplete sessions and **SPEC-rules** guidance (locks, attestation reminders, etc.).
- **`validate --strict`** — CI-oriented; focuses on **SPEC-core §2** detectable violations; may include selected **SPEC-rules** hygiene.

Everything the CLI does can be done manually:
- `init` = copy a profile folder
- `status` = read `discussion.md` and `votes.md`
- `next` = read `votes.md` status and decide what to do
- `validate` / `validate --strict` = structural checks
- `summary` = translate `## Summary UI Data` into a standalone `summary.html`
- `remind` = grep **`Scheduled review date:`** in `synthesizer.md`

If you are on a system without bash or Python, you do not need the CLI. Just work with the files directly.
