# Contributing to council.md

Thanks for your interest. council.md is a small, opinionated protocol; contributions are welcome but the bar for changes to the protocol contract is intentionally high.

This document covers how to contribute, what tier of change you're proposing, and how to run the checks before opening a PR.

---

## What you can contribute

**Easy to land:**
- Bug fixes in the CLI (`cli/council.py`)
- Documentation improvements
- New profiles (`profiles/[name]/`) — additional starting points for session types
- New examples (`examples/[name]/`) — fully worked sessions
- Eval bundles (`docs/eval/`) — corpus entries, rubric refinements, comparison data
- Invocation guides for additional AI tools

**Medium bar — discuss in an issue first:**
- Changes to `SPEC-rules.md` (operational rules: workflows, YAML, synthesizer behavior, locks)
- Validator behavior in `cli/council.py`
- Profile coordinator rewrites
- Anti-sycophancy mechanisms

**High bar — protocol change:**
- Anything in `SPEC-core.md` §2 (the normative core)
- Filename changes to the six core files
- Phase name or order changes
- Changes to where synthesis or human decisions live

Protocol changes require a version bump (currently v0.2 → v0.3) and a migration story for existing sessions. Open an issue with the proposal before writing code.

---

## Before you open a PR

1. **Run the validator on the affected examples and profiles:**

   ```bash
   python3 cli/council.py validate examples/startup-pivot
   python3 cli/council.py validate examples/technical-architecture
   python3 cli/council.py validate profiles/decision
   python3 cli/council.py validate profiles/review
   python3 cli/council.py validate profiles/planning
   ```

   Warnings are acceptable for in-progress sessions; errors are not.

2. **If you changed anything spec-adjacent**, also run strict mode:

   ```bash
   python3 cli/council.py validate --strict examples/startup-pivot
   ```

3. **If you changed `SPEC-core.md`:**
   - Update the version reference in `SPEC-core.md`'s versioning section.
   - Update `SPEC-rules.md` cross-references if needed.
   - Note the change in the PR description with migration guidance.

4. **If you changed templates**, sync the corresponding files in:
   - `profiles/decision/`, `profiles/review/`, `profiles/planning/`
   - `examples/startup-pivot/`, `examples/technical-architecture/`

   The CLI does not auto-sync these.

---

## Style

- Markdown files are wrapped to readable widths but not hard-wrapped at a fixed column.
- Use sentence case for headings (`## How to run a session`, not `## How To Run A Session`).
- Prefer fewer bold/italic markers. Reserve emphasis for content that genuinely needs it.
- Use plain English. Write for a developer or founder reading this for the first time, not for a contributor who already knows the codebase.
- Do not add emoji unless the context already uses them.

---

## Reporting bugs

Open a GitHub issue with:
1. What you ran (CLI command, AI model, environment)
2. What you expected
3. What actually happened
4. Minimal reproduction (the smallest session folder that triggers the issue)

For protocol questions or design discussions, prefer Discussions over Issues.

---

## Reporting security issues

If you find a vulnerability in `cli/council.py` or in a supplied example, please report it privately rather than in a public issue.

---

## Forking the protocol

The MIT license permits anything. If you fork the protocol structure (filenames, phase names, normative core), please:
1. Increment the version in your fork's `SPEC-core.md`.
2. Note the fork lineage in your README.
3. Make clear that your fork is not council.md v0.2 compatible.

This keeps the ecosystem honest about which sessions interoperate.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see `LICENSE`).
