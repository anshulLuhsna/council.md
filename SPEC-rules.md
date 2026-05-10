# council.md — SPEC-rules (operational detail) v0.2

> **Elaborates [SPEC-core.md](SPEC-core.md).**  
> If a change here would **not** require a compatible fork to edit session files, it belongs here — not in SPEC-core. **Core §2** remains the compliance surface.

---

## 4. Phase transitions and voting *(elaborates SPEC-core §5–6)*

### 4.1 When voting is allowed

**Voting on phase transitions opens only after the blind round is closed** (if a blind round is used).

During blind round:

- Agents do not yet see each other’s substantive contributions or motions in `votes.md` that depend on knowing others’ positions.
- The human may record **`participation`** updates (see §5b) but **does not call quorum on motions that require deliberation context** until blind contributions are merged into `discussion.md` and agents could reasonably vote.

**Order of operations (default):**

1. Blind contributions captured (`drafts/` or redacted paste — see §6).
2. Merge into `discussion.md`; set `blind_round_closed: true` in `votes.md` frontmatter (recommended field).
3. **Then** optional Round 2 contributions (same `### Agent:` block — **`#### Round 2`** — §5c).
4. **Then** motions such as “Proceed to synthesizing” and agent votes.

### 4.2 Quorum rules

**Default:** `quorum_rule: simple_majority` of registered agents who have `participation: contributed` (non-declined).

**`quorum_rule: human_only`**

- Agents may append non-binding advisory votes (`YES` / `NO` / `ABSTAIN`) as notes for the record.
- **Only the human** updates `votes.md` to record **Result:** and **`Confirmed by human:`** for each transition.
- Quorum is satisfied when the human confirms — not when agents tally.

### 4.3 After `status: synthesizing`

**No new agent contributions** to `discussion.md` unless the human explicitly **reopens** deliberation:

1. Human records a motion: “Reopen deliberation” with reason (e.g., missing agent, material error).
2. Human sets `status: contributing` in frontmatter.
3. Synthesizer should prepend a note in **`synthesizer.md`** that prior **`## Council Synthesis`** may be stale if substantive new contributions follow — **or** archive prior synthesis into **`synthesizer-archive.md`** (optional file).

If someone pastes a contribution while status is still `synthesizing` without reopening, treat it as **protocol violation / out-of-band** — the synthesizer run should be repeated after reopening; do not silently merge.

The earlier clause “agents continue after a vote passes” applies **only while `status: contributing`**: late agents may still complete blind drafts before the motion to synthesize closes deliberation; it does **not** mean “keep contributing after synthesis has started.”

### 4.4 Session mode: `council` vs `rehearsal`

`session_mode` in `votes.md` frontmatter:

| Value | Meaning |
|---|---|
| `council` | **Distinct underlying models** intended; agent votes can satisfy quorum per `quorum_rule` when diversity requirements are met (§4.5). |
| `rehearsal` | Same model or insufficient diversity — **role-play only**; agent votes are **advisory**; **every** phase transition must include explicit **`Confirmed by human:`** (same practical effect as documented rehearsal / “no false quorum”). |

### 4.5 Model identity *(detail for SPEC-core §6)*

Each registered agent MUST have a non-empty `model:` string in `votes.md` (self-declared when pasting: e.g. `gpt-5`, `claude-opus-4`, `gemini-2.5-pro`, or `same-chat-session-gpt5` if honest about reuse).

**String equality is not proof of distinct backends.** Two labels such as `gpt-5` and `gpt-5-creative` may still be the same provider stack; the protocol cannot normalize vendor taxonomies for you.

**Human attestation (recommended for `session_mode: council`):** set **`distinct_underlying_models_attested: true`** in `votes.md` frontmatter only when the human confirms that **≥ two agents used meaningfully distinct inference backends** (not merely distinct strings). If false or omitted, treat distinct `model:` strings as **weak evidence** only — prefer **`session_mode: rehearsal`** or explicit human confirmation on each motion.

**Self-attestation limits.** Like `model:` strings, this flag is **self-reported**. Someone dishonest about labels can lie about the boolean too; **no protocol can cryptographically verify which inference backends ran.** For high-stakes audits, attach **session transcripts or exports** as evidence alongside `votes.md`; treat attestation as documentation of intent, not proof.

**Quorum on agent votes (token-level heuristic):** in `council` mode, if **≥ two distinct `model:` strings** appear among `participation: contributed` agents **and** (optional) **`distinct_underlying_models_attested: true`**, agent votes may satisfy `quorum_rule` as designed. If strings differ but attestation is false, **downgrade** to advisory votes unless the human confirms transitions.

---

## 5. Agent contribution format *(recommended shape under SPEC-core §2)*

Each agent writes under:

```markdown
### Agent: [Name]
```

**Recommended subsections** (semi-structured):

```markdown
### Agent: [Name]

#### Position
…

#### Reasoning
…

#### Risks
…

#### Unknowns
…

#### Counterpoints
…

#### Confidence
HIGH | MEDIUM | LOW — one sentence why.
```

**Confidence gate:** If LOW, say what is missing; do not guess.

**Anti-sycophancy (enforceable):** Blind round + structured counterpoints make independent reasoning **process-enforced**. Do **not** rely on rules about what an agent “would have thought before reading others” — that is not verifiable from text.

---

## 5b. Participation states (declined / refused / truncated)

Per-agent participation is tracked in `votes.md` under each agent or in an `agent_participation:` map (either is fine):

| Status | Meaning |
|---|---|
| `pending` | Not yet contributed |
| `contributed` | Normal completion |
| `declined` | Agent refuses the task (policy, capability) |
| `refused` | Model refused output (e.g. safety) |
| `truncated` | Output cut off; human should retry or mark skipped |

If any agent is not `contributed`, the synthesizer MUST include **`### Incomplete Council`** under **`## Council Synthesis`** in **`synthesizer.md`** stating which agents are missing and how synthesis is limited. The human may proceed or reopen.

---

## 5c. Round 2+ (addressing) — **canonical form**

Use **one** `### Agent: [Name]` block and optional **`#### Round 1`** / **`#### Round 2`** subsections inside it:

```markdown
### Agent: [Name]

#### Round 1
…

#### Round 2
…
```

**Deprecated (do not use for new sessions):** a second markdown heading `### Agent: [Name] — Round 2`. It breaks agent-name parsing and duplicates identity. Older sessions may contain it — merge into one block when editing.

**Removal schedule:** New sessions MUST NOT add this heading pattern. **v0.3** will treat extra `### Agent:` lines with `— Round N` as non-conformant in tooling (migrate legacy sessions before upgrading).

Do not overwrite Round 1 text with Round 2.

---

## 6. Blind round and shared `discussion.md`

A single `discussion.md` containing all agent stubs **leaks other agents’ sections** if pasted wholesale.

**Normative blind workflow (pick one):**

### Option A — `drafts/` staging *(recommended)*

1. Coordinator creates `drafts/[slug].md` per agent, where `slug` matches `agents/[slug].md` basename (e.g. `drafts/strategist.md`).
2. Human runs each agent with: `context.md` + `agents/strategist.md` + **only that agent’s empty draft template** — **not** full `discussion.md`.
3. When the draft is complete, human copies into `discussion.md` under the correct `### Agent:` stub **or** replaces stub via merge.

### Option B — Redacted paste

Human manually removes other agents’ sections before pasting into the model UI (error-prone; still valid).

After all blind drafts are merged, set `blind_round_closed: true` in `votes.md` frontmatter.

---

## 6b. Discussion length and rollover

If `discussion.md` approaches the synthesizer’s context limit:

1. Freeze **`discussion-r1.md`** (copy of current file).
2. Continue Round 2 in fresh **`discussion.md`** with a header pointing to `discussion-r1.md` for prior text.
3. Synthesizer reads **all** round files the human points to.

## 6c. Compaction aids

If the human chooses to create a compact brief for a later round or for synthesis, the brief is **non-authoritative**.

- Briefs may help a model fit within context limits.
- Briefs must not replace `discussion.md`, `context.md`, `votes.md`, or `synthesizer.md` as the archival record.
- Briefs should preserve agent names, disagreements, confidence levels, and unresolved questions.
- If synthesis relies on a brief instead of full discussion, prefer **`PARTIAL`** synthesis confidence unless the human confirms no material loss.

---

## 7. Voting format (`votes.md`)

**Frontmatter (authoritative):**

```yaml
---
status: contributing
quorum_rule: simple_majority   # simple_majority | unanimous | supermajority | human_only
session_mode: council           # council | rehearsal
blind_round_closed: false       # true after blind merged to discussion.md
distinct_underlying_models_attested: false  # human sets true when ≥2 distinct backends used — §4.5
lock:
  holder: ""                    # agent name or "human" — who may edit discussion.md / drafts now
  acquired_at: ""               # ISO 8601 recommended
  ttl_hours: 24                 # lock expires ttl_hours after acquired_at; omit = default 24
registered_agents:
  - name: Agent A
    model: gpt-5                # REQUIRED non-empty — see §4.5
    participation: pending      # pending | contributed | declined | refused | truncated | skipped
  - name: Agent B
    model: claude-opus-4
    participation: pending
---
```

**Body:** Start with `## Phase Transition Log`, then **each motion as its own `### Motion: …`** section (sibling headings — “under” means *in the same file in document order after* the log heading, not necessarily nested list items).

```markdown
## Phase Transition Log

### Motion: Proceed to Synthesizing

| Agent | Vote | Note |
|---|---|---|
| Agent A | YES | |
| Agent B | YES | |

**Result:** Motion passed (2/2 — simple majority)
**Confirmed by human:** [ ]
```

---

## 8. Synthesizer behavior (`synthesizer.md` only) *(implements SPEC-core §2 synthesis location)*

The synthesizer reads `context.md`, **`discussion.md` (and `discussion-r*.md` if used)**, **`votes.md`**, and this **`synthesizer.md`** instructions file.

**Writes output under `## Council Synthesis` in this file (`synthesizer.md`).**  
**Does not write synthesis into `discussion.md`.**

### Must include

- **Agreement Map**, **Conflict Map**, **Open Questions**, **Candidate Options** (same spirit as prior templates)
- **Evidence anchors:** For each bullet in Agreement / Conflict maps, include **at least one short quoted excerpt** from `discussion.md` (or line-referenced: “Under `### Agent: X`, Round 1 …”) so mis-attribution is easier to catch.
- **Calibration hints (not mechanical truth):** Under **`### Calibration Flags`**, note agents whose **HIGH** confidence appears **thinly grounded** — e.g. no reference to anything verifiable from `context.md`, cited artifacts, or explicit stated assumptions. Principled domain reasoning may be sound without a citation; artifact citations do not guarantee correctness. Prefer flagging **missing explicit assumptions** when stakes are high. Optional **synthesis auditor** model may review (pattern in `docs/anti-sycophancy.md`).
- **`### Incomplete Council`** if participation incomplete (§5b) — child of `## Council Synthesis`.

### Must not

- Pick a single winning option as “the answer”
- Average away disagreement
- Hide dissent
- Write `the council recommends X` unless the human explicitly asked for a decision mode

### Synthesis collapse checks

Before finalizing, the synthesizer should check:

- Did I preserve minority positions?
- Did I turn disagreement into vague consensus?
- Did I imply a recommendation?
- Did I attribute every substantive claim?
- Did I include evidence quotes?

### Optional quality layer

A **second model** may act as **synthesis auditor**: read raw `discussion.md` + **`## Council Synthesis`** and verify excerpts match positions (documented as optional pattern in `docs/anti-sycophancy.md`).

### Incomplete synthesis

If synthesis cannot be completed, keep everything under **`## Council Synthesis`**: set **`### Synthesis Confidence`** to **`INCOMPLETE`** and explain what is missing (missing agents, truncated outputs, etc.) in that subsection or **`### Incomplete Council`**. Do **not** add a separate top-level **`## Synthesis Status`** heading — one escape hatch avoids redundant shapes.

---

## 9. Coordinator role

The coordinator:

1. Runs the opening interview (see `coordinator.md`)
2. **Challenges vague roles** — rejects one-word labels without mission; requires explicit **optimize for / defer to / out of scope** for each agent
3. Writes `context.md`, scaffolds `discussion.md` and **`drafts/`** when blind round is enabled
4. Initializes **`votes.md`** with `session_mode`, **`model:` filled**, `participation`, **`lock:`**
5. Instructs the human on blind workflow (§6)

---

## 10. YAML frontmatter policy

| File | Frontmatter |
|---|---|
| `agents/[name].md` | YES |
| `votes.md` | YES — includes `status`, `session_mode`, agents + **`model:` required** |
| `context.md`, `discussion.md`, `synthesizer.md`, `coordinator.md` | NO for protocol layers; human-readable body |

---

## 11. Customization vs compliance *(interpret SPEC-core §2)*

You may rename agents freely and add agents. You **cannot** claim council.md v0.2 compliance if you move synthesis into `discussion.md` or duplicate phase state outside `votes.md` frontmatter.

## 11b. Compatible tooling

Tools may scaffold, validate, summarize, compact, or render sessions.

Tools must not:

- hide phase state outside `votes.md`
- silently expose blind drafts
- replace `discussion.md` as source of truth
- synthesize into `discussion.md`
- make the human decision
- make compact briefs authoritative

Runtime compatibility belongs in docs and operational guidance, not the compliance core, unless the canonical session files themselves change.

---

## 12. Operational assumptions and lock semantics

**Serial human editing:** The protocol assumes **one writer at a time** for `discussion.md` / `drafts/` unless using branches/git merge.

**Lock (`votes.md` → `lock:`):**

- **`holder`:** who may edit `discussion.md` / `drafts/` now (agent role name or `"human"`).
- **`acquired_at`:** ISO 8601 timestamp when the lock was taken (recommended).
- **`ttl_hours`:** defaults to **24** if omitted. The lock **expires** `ttl_hours` after `acquired_at` (if `acquired_at` is set).
- **After expiry:** any human may clear `holder` / `acquired_at` or take the lock — stale locks must not block the session indefinitely.
- **No timeout without `acquired_at`:** if only `holder` is set, treat the lock as **advisory** until the human reconciles manually.

There is no distributed lock server — behavior is **documentation + human discipline**.

---

## 13. What this is not

- Not a framework with a runtime
- Not a substitute for human judgment
- Not guaranteed truth — structured disagreement and audit hooks reduce blind spots; they do not eliminate them

---

## Versioning *(SPEC-rules)*

This document is **council.md SPEC-rules v0.2**. It may receive **non-breaking** clarifications without bumping **SPEC-core**, until **SPEC-core §2** itself changes.

**Toward v0.3 (consolidation release — planned):** collapse `votes.md` frontmatter where feasible; **remove** tooling tolerance for the deprecated `### Agent: … — Round 2` heading pattern (**§5c**). Until then, `validate --strict` may flag that pattern per **`cli/README.md`**.

---

*council.md is MIT licensed. Fork it, adapt it, run it.*
