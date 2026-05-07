# Anti-Sycophancy Patterns

Sycophancy is the single most dangerous failure mode in a model council.
It happens when agents stop reasoning independently and start optimizing to agree with each other.

When a council sycophants, you get false consensus — the appearance of agreement without the substance. This is worse than a single model answer because it feels more authoritative.

This document describes the mechanisms built into council.md to prevent it, and how to apply them.

---

## Why sycophancy happens in multi-model councils

When multiple AI models deliberate on the same question, several dynamics push toward false consensus:

1. **Anchoring**: The first model to respond frames the question. All subsequent models unconsciously (or explicitly) respond to that frame rather than forming their own.
2. **Social pressure simulation**: Models trained on human feedback have learned that agreement is rewarded. When they see an authoritative-sounding prior contribution, they tend to validate it.
3. **Role diffusion**: When agent roles are not crisp, agents default to "helpful assistant" mode — which means supporting whatever was said before.
4. **Synthesis pressure**: If agents know a synthesizer will aggregate their views, some models will "pre-synthesize" and write vague, hedged positions that accommodate all prior views.

---

## Mechanism 1: Blind first round (default)

**What it is:** Each agent writes their contribution without reading other agents' contributions first.

**Why it works:** Prevents anchoring entirely. If Agent A has not read Agent B's position, they cannot defer to it.

**How to run it (normative):**
- Use **`drafts/[slug].md`** per agent (same basename as `agents/[slug].md`) so you never paste full `discussion.md` during blind.
- Each agent gets `context.md` + `agents/[name].md` + **only** their `drafts/[name].md`.
- After all drafts are written, **merge** into `discussion.md` and set `blind_round_closed: true` in `votes.md` frontmatter.
- **Then** optional round 2 with full `discussion.md`.

See **SPEC-rules §6** and `drafts/README.md`.

**When to skip it:**
- When you have only 2 agents and want them to have a real back-and-forth
- When you are running an explicit debate format where sequencing is intentional

The blind round is the default. Skipping it should be a deliberate choice, not an oversight.

---

## Mechanism 2: Required counterpoints section

**What it is:** Every agent contribution includes a **`#### Counterpoints`** section where the agent must explicitly respond to any prior position that contradicts theirs (or mark blind as specified in **SPEC-rules**).

**Why it works:** Makes disagreement structurally visible. In **non-blind** rounds, an agent cannot simply echo a prior position without engaging the tradeoff.

**The rule (process-enforceable):**
- In **blind round 1:** write `No prior contributions read — blind round.` (or merge from `drafts/` first, then run round 2).
- In **round 2+:** respond to specific claims you disagree with — name the claim and why.
- Vague agreement (“Sounds good”) without engaging substance is weak contribution — coordinators should reject it on revision.

**Do not rely on unverifiable rules** like “what you would have thought before reading others” — use blind **`drafts/`** instead (SPEC-rules §6).

---

## Mechanism 2b: Coordinator role stress-test

The coordinator interview **rejects vague roles** and requires explicit **optimize for / defer to / out of scope** per agent (see `templates/coordinator.md`). ---

## Mechanism 3: Confidence gate

**What it is:** Every agent must declare a confidence level (HIGH / MEDIUM / LOW) and explain it. LOW confidence requires naming specifically what is missing.

**Why it works:** Prevents agents from confidently asserting positions they are actually uncertain about. Models tend to present uncertain conclusions with the same rhetorical confidence as certain ones. This gate makes uncertainty visible.

**The rule:**
- HIGH: You have sufficient information to reason well about this question
- MEDIUM: You have reasonable information but one or more important gaps
- LOW: You do not have sufficient information to make a well-reasoned contribution on this point. Name the gap specifically. Do not speculate.

**If an agent writes LOW confidence:** The synthesizer must flag this in the relevant sections of the synthesis. LOW confidence contributions should not be cited as supporting evidence for a recommendation.

---

## Mechanism 4: Role precision in agent files

**What it is:** Each agent's role file defines precisely what the agent optimizes for, what it does not do, and what it should defer to other agents on.

**Why it works:** Role confusion is the primary cause of role diffusion. When an agent does not have a clear lane, it expands into a general assistant that agrees with everything.

**Principles for writing agent roles:**
- Define what the agent optimizes for: "You optimize for long-term strategic leverage, not immediate delivery speed."
- Define what the agent does NOT do: "Do not propose implementation details. Defer to the Operator on execution specifics."
- Make the agent's lens explicit: "You see every proposal through the lens of what could go wrong."
- Remind the agent that challenge is its job: "Disagreement is not a failure. Hiding disagreement is."

---

## Mechanism 5: Synthesizer anti-averaging + evidence anchors

**What it is:** The synthesizer output lives in **`synthesizer.md`** under **`## Council Synthesis`** (not in `discussion.md`). It must preserve disagreements, require **quoted excerpts** (or heading pointers) for Agreement/Conflict items, and run **calibration** on HIGH confidence (**SPEC-rules §8**).

**Why it works:** Prompt-only “don’t average” is weak; **evidence anchors** make mis-attribution easier to catch. A **second model** can audit synthesis against `discussion.md` (optional).

**What good synthesis looks like:**
Not: "Agents generally support a hybrid approach with some caution about execution risk."
But: "Strategist supports Option C on strategic grounds. Operator supports Option C but warns the founder cannot run sales + product simultaneously past 30 days. Risk Analyst accepts Option C only with pre-defined kill criteria. Challenger questions whether the team is building a business or a bridge round."

---

## Mechanism 6: Agent role mandate to challenge

**What it is:** Every agent file instructs agents to defend their lane and engage contradiction — without relying on **unverifiable** “what you thought before reading X” rules.

**Standard language (process-based):**

```markdown
## Anti-sycophancy rules
- In blind rounds, use drafts/ — do not read peers until merged (SPEC-rules §6)
- In non-blind rounds, use ## Counterpoints to name claims you dispute
- Challenge any position that contradicts yours
- Disagreement is not a failure. Hiding disagreement is.
```

---

## What to watch for

Signs that sycophancy has entered your council:

- Multiple agents writing nearly identical positions with different wording
- Every agent's Counterpoints section is empty or writes "No significant disagreements"
- The synthesizer produces a vague recommendation without clear disagreement attribution
- The synthesis reads like it was written by a single model
- One agent changed their position significantly between round 1 and round 2 without new information

If you see these, consider:
1. Re-running the blind first round if it was skipped
2. Asking agents to specifically argue the strongest case against the consensus position
3. Adding a Challenger role if one is not present
4. Re-running the council with a more precisely scoped question

---

## The bottom line

The goal of a council is not agreement — it is honest mapping.
A council that ends in sharp disagreement but maps that disagreement clearly has done its job.
A council that ends in apparent consensus but buried the real conflict has failed.

Design every council to surface disagreement. Then let the human decide.
