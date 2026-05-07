# drafts/

Per-agent **blind round** drafts live here so you never paste full `discussion.md` (with other agents’ text) into a model.

## Naming

For each agent file `agents/foo.md`, create **`drafts/foo.md`** (same basename).

## Workflow

1. Coordinator scaffolds empty `drafts/[slug].md` with the same heading structure as the stub in `discussion.md`.
2. When running **Agent foo blind**, give the model **only**: `context.md` + `agents/foo.md` + `drafts/foo.md` (empty template).
3. When the draft is complete, **merge** the body into `discussion.md` under `### Agent: Foo`, then delete or archive the draft.

See **SPEC-rules §6**.
