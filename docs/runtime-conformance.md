# Runtime Conformance

`council.md` is file-first, invariant-first, and runtime-optional.

This project does **not** require a runtime. It also does **not** ban runtimes.

A runtime is compatible only if it preserves the protocol invariants and emits the same auditable session files.

## Canonical rule

The canonical session record is the markdown session folder:

- `context.md`
- `discussion.md`
- `votes.md`
- `synthesizer.md`
- `agents/*.md`

Optional files such as `drafts/`, briefs, or `summary.html` may exist, but they do not replace the canonical record.

## Compatible runtime requirements

A compatible runtime must:

- preserve markdown session files as the canonical source of truth
- emit normal `context.md`, `discussion.md`, `votes.md`, `synthesizer.md`, `agents/*.md`
- preserve blind first-round isolation
- keep first-round prompt construction visible or exportable
- log cross-agent information flow
- require explicit human confirmation for phase transitions
- keep `votes.md` authoritative for phase state
- write synthesis only to `synthesizer.md`
- keep summary UI non-authoritative
- export a complete session folder without database-only dependencies

## Non-compatible runtime behavior

These behaviors are not `council.md`-compatible:

- hidden shared memory during blind round
- agents seeing each other before blind drafts are complete
- one-click autonomous council with no human phase gates
- synthesis that silently picks a winner by default
- state stored only in a database with no canonical session export
- no inspectable prompt trace or visibility into what each agent saw
- generated summary with no underlying discussion files

## Runtime Compatibility Checklist

A runtime is `council.md`-compatible only if:

- [ ] It exports canonical session files.
- [ ] It preserves blind first-round isolation.
- [ ] It records exactly what each agent could see.
- [ ] It keeps phase state in `votes.md`.
- [ ] It requires human confirmation for phase transitions.
- [ ] It writes synthesis only to `synthesizer.md`.
- [ ] It preserves disagreement in synthesis.
- [ ] It does not make hidden decisions.
- [ ] It keeps summary UI non-authoritative.
- [ ] It can export a complete session folder at any time.

## Position

The project is not anti-runtime.

The position is:

- runtimes are useful for some workflows
- runtimes are compatible only if they preserve the invariants
- files remain canonical because deliberation needs visible boundaries

If a runtime makes the process smoother while keeping the council inspectable, it fits. If it hides coupling, hidden decisions, or blind-round leakage, it does not.
