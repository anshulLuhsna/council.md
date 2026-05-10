# Contributing to council.md

Thanks for your interest. council.md is a small, opinionated protocol; contributions are welcome but the bar for changes to the protocol contract is intentionally high.

This document covers how to contribute, what tier of change you're proposing, and how to run the checks before opening a PR.

---

## Council-approved contributions

This repo uses its own protocol to review meaningful changes.

If you want to change `council.md`, the default path is:

1. Form the idea or proposed change.
2. Run a council on that change, usually with the `self-improvement` profile.
3. Preserve the session files.
4. Open a PR only if the proposal survives the council review.

The goal is not ceremony for its own sake. The goal is to make major changes auditable, stress-tested, and visibly shaped by structured disagreement before they land.

### When council approval is expected

Council approval is expected for:
- protocol changes
- spec or rules changes
- template rewrites
- coordinator or synthesizer behavior changes
- anti-sycophancy changes
- validator behavior changes
- new profiles
- major docs reframing
- new examples intended to set project direction

You usually do **not** need a full council session for:
- typo fixes
- broken links
- small wording clarifications
- narrow bug fixes that do not change protocol behavior
- small internal refactors with no user-facing effect

When in doubt, run the council anyway. For this repo, that is a feature, not overhead.

### What “survives the council” means

A proposal is ready for a PR when the council has produced:
- a clear question under review
- real disagreement or explicit convergence
- a synthesis that preserves conflicts and unknowns
- a human decision on whether to proceed
- concrete acceptability conditions for merging the change

The council does not merge code. The council makes the change legible enough for a maintainer to judge whether the PR should exist at all.

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

0. **Run a council review for meaningful changes.**

   For repo-shaping changes, create a session with `profiles/self-improvement/` or an equivalent compatible council.

   Your PR should link or include:
   - the council session path
   - the question reviewed
   - the human decision
   - disagreements preserved
   - the acceptability conditions the change had to satisfy

   A good short PR note looks like:

   ```text
   Council review: examples/council-self-review/
   Question: Should council.md reframe itself from runtime-free to file-first, invariant-first, runtime-optional?
   Decision: Proceed with reframing; preserve canonical files and human-controlled phase gates.
   Disagreements preserved: Whether a reference runtime should exist later; whether file-first is an epistemic mechanism or primarily a portability choice.
   Acceptability conditions: No change to normative core file layout; no wording that implies runtimes are bad; no wording that makes the council the decision-maker.
   ```

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

5. **If your PR depends on council approval, make the PR easy to audit.**
   - State the session path near the top of the PR.
   - State whether the change fully satisfies the council's acceptability conditions.
   - Call out any unresolved disagreement that still remains after implementation.
   - If the implementation intentionally departs from the council outcome, say so plainly.

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
