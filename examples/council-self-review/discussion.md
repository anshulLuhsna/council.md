# Self-Improvement Council: Framing the Protocol

> **Profile:** self-improvement
> **Discussion round:** 1
> **Note:** Phase lives in `votes.md` frontmatter only.

---

## Contributions

### Agent: Protocol Defender

#### Position
The project should absolutely reframe itself, but only if the reframe protects the current invariants. “Runtime-free” is too narrow as the lead identity. “File-first, invariant-first, runtime-optional” is better because it describes what is actually load-bearing. The risk is that the repo softens into “tooling-friendly” language and stops defending the epistemic boundaries that made the project worth building.

#### Reasoning
The current protocol has a real idea inside it: deliberation quality depends on visible separation. That includes:

- blind first-round isolation
- explicit handoffs
- canonical files
- human-controlled phase transitions
- synthesis that maps disagreement instead of deciding

Those are the actual invariants. “No runtime” is not itself the invariant. It is one way to keep those invariants intact.

So the proposed reframe is directionally right. It makes the project sound less ideological and more precise. It also opens the door to tooling without forcing a philosophical retreat.

But the repo should not swing too far into “compatible runtimes welcome” language without saying exactly what compatibility means. Otherwise you get the worst outcome: the project becomes a vague protocol wrapper around hidden shared-memory agent systems that quietly destroy blind independence while claiming compatibility.

The project should preserve a hard line that files are canonical and that runtime state is never the only truth.

#### Risks
- A softer framing may invite tools that keep the surface language but violate the actual protocol.
- “Runtime-optional” without a conformance checklist will be read as permission to build councils that are convenient but epistemically sloppy.

#### Unknowns
- Whether future users actually want runtime compatibility, or whether this is mostly a messaging issue.
- Whether a reference runtime would strengthen the project or slowly displace the file-first discipline.

#### Counterpoints
No prior contributions read — blind round.

#### Confidence
HIGH — the invariants are clearer than the current slogan, and the project should lead with them.

---

### Agent: Protocol Challenger

#### Position
The current design is in real danger of mistaking moral seriousness for product clarity. I agree with the reframe, but I think it still understates the problem: the workflow is too manual, the rhetoric around independence can drift into self-congratulation, and the file-first choice is not automatically an epistemic breakthrough.

#### Reasoning
There is a strong critique of naive multi-agent systems in this repo. That part is real. But the repo risks taking one good insight — “fake consensus is a problem” — and stretching it into a full product doctrine.

Here is the harder question: are files the reason the protocol is better, or are files just the easiest way to externalize state while the real value comes from:

- blind first rounds
- explicit roles
- synthesis discipline
- human-controlled phase transitions

If that is true, then the project should be careful not to mythologize markdown itself.

My more uncomfortable view is this: the current workflow is still too expensive for many users. A lot of people will admire it, run it once, and never run it again. The protocol may be intellectually right and still commercially weak.

The reframe helps because it shifts from “we have no runtime” to “we have invariants.” But that should also force the project to admit something else: if a runtime preserved those invariants and reduced friction, it might simply be better for many users.

So yes, reframe. But do not turn that reframe into a self-protective story where the repo keeps all of its friction and just describes it more elegantly.

#### Risks
- The project may confuse inspectability with usability.
- “Invariant-first” could become a respectable-sounding way to avoid hard product decisions about speed, adoption, and workflow cost.

#### Unknowns
- Whether repeat users actually value the explicit handoff model enough to tolerate it.
- Whether a disciplined runtime would outperform the current file workflow while preserving the important bits.

#### Counterpoints
No prior contributions read — blind round.

#### Confidence
HIGH — the framing change is needed, but the product risk remains.

---

### Agent: User Reality Critic

#### Position
The new framing is better, but it only matters if it changes user comprehension fast. Most users do not care about “runtime-free” as a philosophical statement. They care about two questions: “Can I use this with the AI tools I already pay for?” and “Will this help enough that I’ll do it again?”

#### Reasoning
The current messaging makes the project sound clever, but not always practical.

The strongest user-facing story is not:

> We rejected runtimes.

It is:

> This works with Claude, ChatGPT, Gemini, Cursor, local models, and copy-paste. You do not need API keys to get value.

That is much more concrete.

I also think the repo needs to be more honest about repeat-use friction. The protocol is likely worth it for:

- hard decisions
- strategic reviews
- planning under uncertainty

It is probably not worth it for routine advice requests.

That should be said more plainly.

The self-improvement profile is a smart addition because it demonstrates a living project, but it only helps if the output becomes visible. Improvement history is good. A canonical self-review example is good. They make the project feel active instead of theoretical.

Still, none of this fixes the biggest adoption question: will a real user run this twice? The repo should start measuring that explicitly in evals instead of assuming that stronger process automatically wins.

#### Risks
- Users may admire the project and still bounce because it looks like work.
- The protocol may be best understood as a niche high-stakes workflow, not a broad everyday tool.

#### Unknowns
- Whether users who care about deliberation are numerous enough to sustain the project.
- Whether thin tooling and compaction are enough to reduce friction without changing the nature of the protocol.

#### Counterpoints
No prior contributions read — blind round.

#### Confidence
MEDIUM — I am confident about the framing gap, less confident about the eventual market size.

---

### Agent: Epistemics Auditor

#### Position
The reframe is correct because it points attention at the real mechanism: invariants. The current wording is too easy to read as anti-tooling when the deeper claim is about preserving independence, traceability, and conflict quality. But the repo still needs stronger safeguards against synthesis collapse and long-session drift.

#### Reasoning
The protocol’s strongest idea is not markdown. It is structured independence.

Blind rounds matter because they prevent early anchoring.
Explicit roles matter because they reduce diffusion.
Canonical files matter because they make the process auditable.
Human phase control matters because it prevents a hidden verdict machine.

That is the epistemic stack.

The current “runtime-free” framing hides that by overemphasizing what the project lacks instead of what it protects.

At the same time, the protocol is not done solving its own hardest problem. Synthesis collapse is still a real danger. A synthesizer can preserve headings while still softening meaningful disagreement into respectable prose. Long discussions can also degrade the process because later turns stop working directly from the full source and start operating on compressed or partial context.

So the right move is not only reframing. It is:

- stronger synthesizer language
- explicit collapse checks
- compaction guidance that admits lossiness
- evals that measure preserved disagreement instead of just “decision quality”

That is where the protocol earns its claims.

#### Risks
- Without stronger synthesis guidance, the project can still produce elegant fake consensus.
- Without compaction discipline, long sessions may become performatively rigorous but epistemically thin.

#### Unknowns
- How often real sessions currently lose disagreement during synthesis.
- Whether users will actually follow compaction discipline carefully enough for it to help.

#### Counterpoints
No prior contributions read — blind round.

#### Confidence
HIGH — the reframe is good, and the synthesis-strengthening work is necessary.

---

### Agent: Maintainer

#### Position
This should become a concrete repo change set, not just a messaging tweak. The best version is: reframe the README and docs, add self-improvement artifacts, add runtime conformance and subscription-native docs, tighten the synthesizer rules, and document compaction and eval baselines.

#### Reasoning
The proposal is strongest where it becomes operational.

The repo needs new artifacts that make the strategy visible:

- `profiles/self-improvement/`
- `examples/council-self-review/`
- `IMPROVEMENT_HISTORY.md`
- runtime conformance guidance
- subscription-native explanation
- compaction guidance

These do three jobs at once:

1. They clarify the project’s actual thesis.
2. They make the project visibly self-improving.
3. They translate philosophy into auditable repository structure.

I would avoid any changes that make the core spec materially more complex. The runtime compatibility story should mostly live in docs and rules, not the normative core. The core should stay small and conservative.

I would also not implement a runtime or automatic compaction here. That would confuse the strategic move. The point is to clarify the protocol and its boundaries first.

#### Risks
- Trying to add too much tooling now would muddy the project thesis.
- A weak self-review example would look self-congratulatory and hurt credibility more than help it.

#### Unknowns
- How much of the runtime compatibility story should eventually be encoded in validation versus left as docs and social contract.

#### Counterpoints
No prior contributions read — blind round.

#### Confidence
HIGH — this is a coherent repository-level change set.

---

### Agent: Historian

#### Position
This is a clarification with strategic consequences, not a full reversal. The project is not abandoning its original position. It is naming it more accurately. That said, if the repo does not record the disagreement around runtimes explicitly, future readers will misremember this as either “the project softened” or “the project was always runtime-compatible.”

#### Reasoning
The existing repo already hints at the deeper thesis:

- specs are split to keep invariants small
- the human remains the decision-maker
- optional UI does not replace source files
- the coordinator manages the workflow rather than hiding it

Those are not anti-runtime principles. They are anti-opacity principles.

So the move from “runtime-free” to “file-first, invariant-first, runtime-optional” is mostly a clarification of what was already there.

But it is also a strategic shift in how the project will be read.

Before, the repo could be understood as:

> We reject runtime-heavy multi-agent systems.

After, it will be understood as:

> We reject systems that break the invariants, whether they use files only or a runtime.

That is a broader and more durable position.

The improvement history matters because this exact nuance will get lost otherwise. Future changes need a place to say:

- what was decided
- what stayed unresolved
- what the follow-up evidence should be

Without that, self-improvement becomes anecdotal.

#### Risks
- The project may under-document the fact that this was a deliberate repositioning.
- Readers may incorrectly conclude that a runtime is now a near-term roadmap item when the decision was only to permit compatible tooling conceptually.

#### Unknowns
- Whether future self-review sessions will reinforce this framing or pull the project back toward a sharper anti-runtime posture.

#### Counterpoints
No prior contributions read — blind round.

#### Confidence
HIGH — this is a clarification, but one important enough to record as a real directional change.
