# council.md Glossary

This page defines common council.md output terms in plain language.

The short version: the council does not decide for you. It gives you a map of the decision terrain so you can decide with fewer hidden assumptions.

---

## Core synthesis terms

### Agreement

An **agreement** is a point where multiple agents independently converge.

It does **not** mean everyone voted yes, and it does **not** mean the point is automatically true. It means the synthesizer found repeated support across agent contributions.

Good agreements include evidence, usually a short quote from `discussion.md`.

Example:

> Several agents agree that the MVP should avoid accounts and team features.

Why it matters: agreements show what is probably stable enough to build around or treat as a strong assumption.

---

### Conflict

A **conflict** is a real disagreement between agents.

Conflicts are not failures. They are the main reason to run a council. A good conflict map preserves the disagreement instead of blending it into a vague compromise.

A useful conflict names:

- each side's position
- which agents hold each side
- what is at stake
- what evidence or decision would resolve it

Example:

> Builder thinks the live visual map should be cut from v0. Reviewer thinks some visual artifact may improve trust.

Why it matters: conflicts show where the human decision is actually being made.

---

### Open question

An **open question** is a gap that would materially change the decision if answered.

Open questions should not be generic curiosity. They should point to missing information the human can either answer, test, or accept as uncertainty.

Example:

> Can a fast model reliably identify load-bearing assumptions under the latency budget?

Why it matters: open questions identify the next piece of evidence you need before committing.

---

### Candidate option

A **candidate option** is one possible path implied by the council.

The synthesizer may list candidate options, but it must not pick a winner. Each option should include tradeoffs, preconditions, and which agents support or oppose it.

Example:

> Option A: build the narrow v0 and test it with real users. Option B: pre-test the prompt before building voice infrastructure.

Why it matters: candidate options turn abstract disagreement into concrete choices.

---

### Kill risk

A **kill risk** is a risk serious enough that, if it turns out to be true, it could kill the project, product, decision, or strategy.

It is intentionally stronger than "concern" or "consideration." The phrase asks:

> What could make this not worth doing?

Kill risks should be few, specific, and ranked when possible. For high-stakes reviews, they should include a verdict:

- **fatal** — if true, the path is probably not worth pursuing as stated
- **manageable** — serious, but there is a credible mitigation
- **unknown** — important enough to test, but the council does not know yet

Example:

> If Arbityr's fast live model cannot find real load-bearing assumptions, the core product fails.

Why it matters: kill risks force the council to separate existential threats from ordinary execution friction.

---

### Calibration flag

A **calibration flag** notes when an agent's confidence may be too high for the evidence it gave.

This is not a claim that the agent is wrong. It is a warning that the human should not overweight that contribution without more grounding.

Example:

> Agent claimed HIGH confidence but did not cite assumptions, constraints, or evidence.

Why it matters: calibration flags help prevent confident-sounding but weakly supported advice from dominating the decision.

---

### Synthesis confidence

**Synthesis confidence** describes the completeness of the synthesis, not whether the final answer is correct.

Use:

- **COMPLETE** — all expected contributions are in, and the synthesizer can map the major agreements, conflicts, and unknowns
- **PARTIAL** — the map is useful, but important uncertainty remains
- **INCOMPLETE** — missing or truncated inputs prevent a reliable synthesis

Why it matters: this tells the human how much to trust the council map before deciding.

---

## Agent contribution terms

### Position

The agent's main stance in direct language.

### Reasoning

The argument behind the position.

### Risks

What could go wrong with the agent's preferred path and with alternatives.

### Unknowns

Specific missing information that would change the agent's answer.

### Counterpoints

Where the agent responds to contradicting views. In a blind round, this should usually say:

> No prior contributions read — blind round.

### Confidence

The agent's own confidence label: **HIGH**, **MEDIUM**, or **LOW**, plus one sentence explaining why.

LOW confidence should name the missing information.

---

## Presentation terms

### Plain-language summary

A non-authoritative explanation of the synthesis for humans who do not want to read the full markdown first.

It may appear in an optional `summary.html` or similar artifact. It must not replace `synthesizer.md`.

### Summary UI

An optional static page, usually named `summary.html`, that presents the synthesis as a guided briefing.

It can include agent summary cards, agreements, conflicts, kill risks, candidate options, open questions, and a reflection prompt.

The summary UI is generated after synthesis. It reads from `synthesizer.md` as the primary source and may use `discussion.md` for short quotes or attribution. It does not read model chats directly.

### Summarizer

The **summarizer** is the model or human step that turns `synthesizer.md` into plain-language UI data for `summary.html`.

The summarizer is not a new council agent. It does not vote, decide, or add new reasoning. Its job is to translate and structure the official synthesis for easier reading.

The summarizer may:

- simplify language
- shorten agent positions
- group content into UI sections
- preserve short evidence quotes

The summarizer must not:

- invent new risks
- invent new options
- hide conflicts
- create fake consensus
- recommend a winner unless the synthesis explicitly records an agent's position as such
- change the human decision record

### Source of truth

The canonical record is always the markdown session files:

- `discussion.md` for agent contributions
- `synthesizer.md` for council synthesis and the human decision
- `votes.md` for phase and participation state

If an optional UI or summary conflicts with the markdown, the markdown wins.
