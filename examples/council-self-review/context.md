# Council Context — Self-Improvement Review

## Question
Should `council.md` keep describing itself primarily as runtime-free, or should it reframe itself as file-first, invariant-first, runtime-optional?

## Area Under Review
Product strategy, protocol framing, docs language, and future tooling boundaries.

## Current Behavior
The repo currently emphasizes that `council.md` has no API keys, no shared runtime, and no orchestration code. That framing is useful, but it risks making the project sound anti-runtime instead of protocol-first.

The actual product behavior is more nuanced:

- files are canonical
- blind rounds are protected
- phase transitions are explicit and human-controlled
- summary UI is non-authoritative
- tooling is acceptable when it preserves invariants
- the protocol works with subscriptions and copy-paste, not just APIs

## Proposed Change
Reframe the project from “runtime-free” as the main identity to:

> file-first, invariant-first, runtime-optional

Keep “runtime-free” as a capability:

> You can run this with no runtime.

Add clearer documentation for:

- subscription-native use
- runtime conformance
- self-improvement profile
- compaction guidance for long sessions
- stronger synthesizer anti-collapse rules

## Invariants That Must Not Break
- blind first round stays independent
- agents do not see each other before blind drafts are complete
- each agent keeps a clear role and lane
- phase transitions stay explicit and human-controlled
- `votes.md` remains authoritative for phase state
- `discussion.md` contains agent contributions only
- `synthesizer.md` contains synthesis and human decision
- synthesizer maps disagreement rather than deciding
- summary UI remains non-authoritative
- markdown/session files remain inspectable and portable

## Prior Related Decisions
- The repo already split SPEC-core and SPEC-rules to keep invariants small and auditable
- The project has consistently treated the human as decision-maker
- The project already added optional `summary.html` while preserving markdown as source of truth

## Evidence Needed
- clearer README framing that does not imply runtimes are always bad
- docs that explain why subscription-native copy-paste is a feature
- docs that allow compatible tooling without weakening the protocol
- stronger synthesis language against fake consensus
- an example showing `council.md` can improve itself

## Background
The current framing is effective as a contrast against agent frameworks, but it may also undersell the real thesis.

The deeper thesis is not “no runtime forever.” It is:

- files are canonical
- deliberation needs visible boundaries
- tooling must preserve invariants
- people should be able to use the AI access they already have

There is tension here.

If the project stays too attached to “runtime-free,” it may sound ideological and unnecessarily narrow.

If it relaxes too far, it may lose the sharpness that makes the protocol interesting in the first place.

## Deadline or Urgency
Now. This framing affects onboarding, blog positioning, future tooling decisions, and how outside readers understand the project.
