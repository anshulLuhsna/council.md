#!/usr/bin/env bash
# council — council.md CLI helper
# No API keys. No network. No LLM calls. Just file scaffolding and validation.
#
# Usage:
#   council init [profile]     Scaffold a new council from a profile
#   council status             Show current phase, contributions, vote status
#   council next               Print what to do next
#   council validate           Check all required files and sections
#   council summary            Generate optional summary.html from synthesizer.md UI data
#   council help               Show this help

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
COUNCIL_DIR="${COUNCIL_DIR:-./council}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

ok()   { echo -e "${GREEN}✓${RESET} $*"; }
warn() { echo -e "${YELLOW}⚠${RESET}  $*"; }
err()  { echo -e "${RED}✗${RESET}  $*"; }
info() { echo -e "${BLUE}→${RESET} $*"; }
bold() { echo -e "${BOLD}$*${RESET}"; }

usage() {
  cat <<EOF

${BOLD}council.md CLI${RESET}

Usage: council <command> [options]

Commands:
  init [profile] [dir]   Scaffold a new council from a profile (default: decision)
                         Profiles: decision, review, planning
                         dir: target directory (default: ./council)
  status [dir]           Show current phase, contributions, and vote status
  next [dir]             Print what to do next in the session
  validate [--strict] [dir]   Check all required files, headings, and frontmatter
  summary [dir]               Generate optional summary.html from synthesizer.md
  remind [dir]           Post-decision review due / overdue (requires python3)
  help                   Show this message

Environment:
  COUNCIL_DIR            Default council directory (default: ./council)

Examples:
  council init decision ./my-decision
  council status ./my-decision
  council validate
  council next

EOF
}

# ─── INIT ────────────────────────────────────────────────────────────────────

cmd_init() {
  local profile="${1:-decision}"
  local target="${2:-$COUNCIL_DIR}"

  local profile_dir="$REPO_ROOT/profiles/$profile"

  if [[ ! -d "$profile_dir" ]]; then
    err "Profile '$profile' not found. Available profiles: decision, review, planning"
    exit 1
  fi

  if [[ -d "$target" ]]; then
    warn "Directory '$target' already exists."
    read -rp "Overwrite? [y/N] " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
      info "Aborted."
      exit 0
    fi
  fi

  cp -r "$profile_dir" "$target"
  ok "Council scaffolded from '$profile' profile → $target"
  echo ""
  info "Next step:"
  echo "  Open $target/coordinator.md in your AI model of choice."
  echo "  Paste its contents into Claude, ChatGPT, Gemini, or any capable model."
  echo "  Answer the coordinator's questions to set up your session."
  echo ""
  info "See docs/invocation-guides.md for model-specific instructions."
}

# ─── STATUS ──────────────────────────────────────────────────────────────────

cmd_status() {
  local dir="${1:-$COUNCIL_DIR}"
  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/council.py" status "$dir"
    return
  fi
  _require_council_dir "$dir"

  bold "Council status: $dir"
  echo ""

  # Phase from votes.md
  local votes_file="$dir/votes.md"
  if [[ -f "$votes_file" ]]; then
    local status
    status=$(grep -m1 '^status:' "$votes_file" | awk '{print $2}' | tr -d '"')
    local quorum
    quorum=$(grep -m1 '^quorum_rule:' "$votes_file" | awk '{print $2}' | tr -d '"')
    echo -e "  Phase:       ${BOLD}${status:-unknown}${RESET}"
    echo -e "  Quorum rule: ${quorum:-not set}"
  else
    warn "votes.md not found — has the council been initialized?"
  fi

  echo ""

  # Agent contribution status from discussion.md
  local discussion_file="$dir/discussion.md"
  if [[ -f "$discussion_file" ]]; then
    bold "Agent contributions:"
    local agents
    agents=$(grep -oP '(?<=### Agent: ).*' "$discussion_file" || true)
    while IFS= read -r agent; do
      [[ -z "$agent" ]] && continue
      # Check if the section after the heading has content or just a comment
      local has_content
      has_content=$(awk "/^### Agent: ${agent}/{found=1; next} found && /^### Agent:/{exit} found && /^[^<]/{print; exit}" "$discussion_file" || true)
      if [[ -n "$has_content" ]]; then
        ok "  $agent — contributed"
      else
        warn "  $agent — not yet contributed"
      fi
    done <<< "$agents"
  else
    warn "discussion.md not found"
  fi

  echo ""

  # Synthesis status
  if [[ -f "$discussion_file" ]]; then
    local synthesis_content
    synthesis_content=$(awk '/^## Synthesis/{found=1; next} found && /^## /{exit} found{print}' "$discussion_file" | grep -v '<!--' | tr -d '[:space:]' || true)
    if [[ -n "$synthesis_content" ]]; then
      ok "Synthesis: complete"
    else
      warn "Synthesis: not yet written"
    fi
  fi
}

# ─── NEXT ─────────────────────────────────────────────────────────────────────

cmd_next() {
  local dir="${1:-$COUNCIL_DIR}"
  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/council.py" next "$dir"
    return
  fi
  _require_council_dir "$dir"

  local votes_file="$dir/votes.md"
  local discussion_file="$dir/discussion.md"

  local status="unknown"
  [[ -f "$votes_file" ]] && status=$(grep -m1 '^status:' "$votes_file" | awk '{print $2}' | tr -d '"')

  bold "What to do next:"
  echo ""

  case "$status" in
    open)
      info "The council is open. Run the coordinator to set up the session."
      echo "  1. Open $dir/coordinator.md"
      echo "  2. Paste its contents into your AI model"
      echo "  3. Answer the coordinator's questions"
      echo "  4. The coordinator will write context.md, scaffold discussion.md, and initialize votes.md"
      ;;
    contributing)
      info "Agents are contributing. Check who still needs to write."
      echo ""
      if [[ -f "$discussion_file" ]]; then
        local pending=()
        local agents
        agents=$(grep -oP '(?<=### Agent: ).*' "$discussion_file" || true)
        while IFS= read -r agent; do
          [[ -z "$agent" ]] && continue
          local has_content
          has_content=$(awk "/^### Agent: ${agent}/{found=1; next} found && /^### Agent:/{exit} found && /^[^<]/{print; exit}" "$discussion_file" || true)
          if [[ -z "$has_content" ]]; then
            pending+=("$agent")
          fi
        done <<< "$agents"

        if [[ ${#pending[@]} -eq 0 ]]; then
          ok "All agents have contributed."
          info "Next: vote to proceed to synthesis."
          echo "  Update votes.md to record the motion and votes, then set status: synthesizing"
          echo "  Run: council validate $dir (to confirm everything is ready)"
        else
          for agent in "${pending[@]}"; do
            warn "  $agent has not yet contributed"
            local agent_file
            agent_file=$(find "$dir/agents" -iname "*.md" | head -1)
            echo "    → Give this agent: context.md + agents/$(basename "${agent_file:-agent.md}")"
            echo "      Ask it to fill in its section in discussion.md"
          done
        fi
      fi
      ;;
    synthesizing)
      info "All agents have contributed. Time to run the synthesizer."
      echo "  1. Open $dir/synthesizer.md"
      echo "  2. Give the synthesizer: context.md + discussion.md (complete) + synthesizer.md"
      echo "  3. Ask it to fill in the ## Synthesis section of discussion.md"
      echo "  4. Paste the synthesis into discussion.md"
      echo "  5. Update votes.md status to: decided"
      ;;
    decided)
      ok "The council has reached a decision."
      info "Write your final decision into synthesizer.md under ## Human Decision"
      echo "  Then update votes.md status to: archived"
      ;;
    archived)
      ok "This council is archived. The files are a permanent record."
      ;;
    *)
      warn "Unknown status: $status"
      info "Check votes.md and ensure status is one of: open, contributing, synthesizing, decided, archived"
      ;;
  esac

  echo ""
}

cmd_remind() {
  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/council.py" remind "$@"
    return
  fi
  err "remind requires python3 (install Python 3 or use synthesizer.md manually)"
  exit 1
}

cmd_summary() {
  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/council.py" summary "$@"
    return
  fi
  err "summary requires python3 (install Python 3 or use the UI template manually)"
  exit 1
}

# ─── VALIDATE (fallback) ─────────────────────────────────────────────────────

cmd_validate() {
  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/council.py" validate "$@"
    return
  fi
  local dir="${COUNCIL_DIR}"
  for a in "$@"; do
    if [[ "$a" != "--strict" ]]; then
      dir="$a"
    fi
  done
  _require_council_dir "$dir"

  bold "Validating council: $dir"
  echo ""

  local errors=0
  local warnings=0

  # Required files
  local required_files=("coordinator.md" "context.md" "discussion.md" "votes.md" "synthesizer.md")
  for f in "${required_files[@]}"; do
    if [[ -f "$dir/$f" ]]; then
      ok "$f exists"
    else
      err "$f is missing"
      ((errors++))
    fi
  done

  # At least one agent file
  local agent_count=0
  if [[ -d "$dir/agents" ]]; then
    agent_count=$(find "$dir/agents" -name "*.md" | wc -l | tr -d ' ')
  fi
  if [[ "$agent_count" -gt 0 ]]; then
    ok "agents/ — $agent_count agent file(s) found"
  else
    err "agents/ — no agent files found"
    ((errors++))
  fi

  echo ""

  # votes.md structure
  if [[ -f "$dir/votes.md" ]]; then
    bold "Checking votes.md:"
    local status
    status=$(grep -m1 '^status:' "$dir/votes.md" | awk '{print $2}' | tr -d '"' || true)
    local valid_statuses=("open" "contributing" "synthesizing" "decided" "archived")
    if [[ " ${valid_statuses[*]} " == *" $status "* ]]; then
      ok "  status: $status (valid)"
    else
      err "  status: '$status' is not a valid phase (expected: open, contributing, synthesizing, decided, archived)"
      ((errors++))
    fi

    if grep -q 'registered_agents:' "$dir/votes.md"; then
      ok "  registered_agents block found"
    else
      warn "  registered_agents block not found in votes.md"
      ((warnings++))
    fi
  fi

  echo ""

  # discussion.md structure
  if [[ -f "$dir/discussion.md" ]]; then
    bold "Checking discussion.md:"
    local agent_headings
    agent_headings=$(grep -c '^### Agent:' "$dir/discussion.md" || true)
    if [[ "$agent_headings" -gt 0 ]]; then
      ok "  $agent_headings agent section(s) found"
    else
      warn "  No agent sections found (expected ### Agent: headings)"
      ((warnings++))
    fi

    if grep -q '^## Synthesis' "$dir/discussion.md"; then
      ok "  ## Synthesis section exists"
      local synthesis_empty
      synthesis_empty=$(awk '/^## Synthesis/{found=1; next} found && /^## /{exit} found{print}' "$dir/discussion.md" | grep -v '<!--' | tr -d '[:space:]' || true)
      if [[ -n "$synthesis_empty" ]]; then
        ok "  ## Synthesis section has content"
      else
        warn "  ## Synthesis section is empty"
        ((warnings++))
      fi
    else
      err "  ## Synthesis section missing from discussion.md"
      ((errors++))
    fi
  fi

  echo ""

  # context.md has required sections
  if [[ -f "$dir/context.md" ]]; then
    bold "Checking context.md:"
    if grep -q '^## Question' "$dir/context.md"; then
      ok "  ## Question section found"
    else
      warn "  ## Question section missing from context.md"
      ((warnings++))
    fi
  fi

  echo ""

  # Agent files have required frontmatter fields
  if [[ -d "$dir/agents" ]]; then
    bold "Checking agent files:"
    while IFS= read -r agent_file; do
      local fname
      fname=$(basename "$agent_file")
      local has_name has_role
      has_name=$(grep -c '^name:' "$agent_file" || true)
      has_role=$(grep -c '^role:' "$agent_file" || true)
      if [[ "$has_name" -gt 0 && "$has_role" -gt 0 ]]; then
        ok "  $fname — frontmatter ok"
      else
        warn "  $fname — missing name: or role: in frontmatter"
        ((warnings++))
      fi
    done < <(find "$dir/agents" -name "*.md")
  fi

  echo ""
  bold "Validation summary:"
  if [[ "$errors" -eq 0 && "$warnings" -eq 0 ]]; then
    ok "All checks passed. Council is ready."
  elif [[ "$errors" -eq 0 ]]; then
    ok "No errors. $warnings warning(s)."
    warn "Review warnings above before proceeding."
  else
    err "$errors error(s), $warnings warning(s)."
    echo "  Fix errors before running the council."
    exit 1
  fi
}

# ─── HELPERS ─────────────────────────────────────────────────────────────────

_require_council_dir() {
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    err "Council directory not found: $dir"
    info "Run 'council init [profile] $dir' to scaffold a new council."
    exit 1
  fi
}

# ─── DISPATCH ────────────────────────────────────────────────────────────────

command="${1:-help}"
shift || true

case "$command" in
  init)     cmd_init "$@" ;;
  status)   cmd_status "$@" ;;
  next)     cmd_next "$@" ;;
  validate) cmd_validate "$@" ;;
  summary)  cmd_summary "$@" ;;
  remind)   cmd_remind "$@" ;;
  help|--help|-h) usage ;;
  *)
    err "Unknown command: $command"
    usage
    exit 1
    ;;
esac
