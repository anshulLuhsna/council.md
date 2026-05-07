# How council.md Works

## The core idea

A council is a structured conversation between multiple AI models about a hard question.
You ask several models independently, let them challenge each other, and have a final model map where they agree, where they disagree, and what you still need to figure out.

You make the decision. The council informs it.

The protocol runs entirely through files. No API keys. No shared runtime. Just markdown.

---

## The files

Every council session uses:

```
your-council/
  coordinator.md    ← opening interview, scaffolding, turn order
  context.md        ← problem, constraints, success criteria
  discussion.md     ← agent contributions only (no synthesis here)
  votes.md          ← YAML `status:` + motions + votes + lock + session_mode
  synthesizer.md    ← synthesizer role + ## Council Synthesis + ## Human Decision
  agents/
    [name].md       ← role + output format
  drafts/           ← optional but recommended for blind rounds (see SPEC-rules §6)
```

The **authoritative phase** is **`status:` in `votes.md` YAML frontmatter** — nowhere else.

See **SPEC-core §2** for what must stay stable for spec compliance.

---

## The phases

```
open → contributing → synthesizing → decided → archived
```

| Phase | What happens |
|---|---|
| `open` | Coordinator finished setup |
| `contributing` | Agents write to `discussion.md` (or `drafts/` before merge) |
| `synthesizing` | Deliberation closed; synthesizer fills **`## Council Synthesis`** in **`synthesizer.md`** |
| `decided` | Human filled **`## Human Decision`** in **`synthesizer.md`** |
| `archived` | Session closed |

**Operational rule:** only **one writer at a time** to `discussion.md` / `drafts/` — use `votes.md` **`lock:`** and serial editing (SPEC-rules §12). No automatic merge — humans coordinate.

---

## Step-by-step flow

### Step 1: Coordinator

Open `coordinator.md`. The coordinator stress-tests roles (optimize / defer / out of scope), writes `context.md`, scaffolds `discussion.md`, **`drafts/`** (if blind), and **`votes.md`** with **`model:`** (required), **`session_mode`**, **`participation`**, **`blind_round_closed`**, **`lock:`**.

### Step 2: Blind round (default)

**Do not** paste full `discussion.md` into each model — other agents’ stubs leak context.

Use **`drafts/[slug].md`** (same basename as `agents/[slug].md`). Give the model **only** `context.md` + agent role + that draft.

Merge completed drafts into `discussion.md`. Set **`blind_round_closed: true`** in `votes.md` frontmatter.

### Step 3: Round 2 (optional)

Use **`#### Round 1` / `#### Round 2`** inside the same `### Agent:` block — **SPEC-rules §5c**.

### Step 4: Voting (after blind is closed if blind was used)

**You cannot vote on “proceed to synthesizing” in a way that assumes shared deliberation context until blind contributions are merged** — see **SPEC-rules §4.1**.

Record motions under **`## Phase Transition Log`** in `votes.md`. When passing, set **`status: synthesizing`**.

**`session_mode: rehearsal`:** same model / hats — votes are **advisory**; human confirms every transition explicitly.

### Step 5: Synthesizer

Give the synthesizer `context.md` + `discussion.md` (+ `discussion-r2.md` if split) + `votes.md` + `synthesizer.md`.

The synthesizer writes output under **`## Council Synthesis`** in **`synthesizer.md` only** — **not** in `discussion.md`.

### Step 6: Decide

Human writes **`## Human Decision`** in **`synthesizer.md`**. Update **`status:`** to `decided`, then `archived`.

### Step 7: Reopen (if needed)

If new contributions are required after synthesis started, follow **SPEC-rules §4.3** — reopen to `contributing`, do not silently append while `synthesizing`.

---

## What the synthesizer does (and does not do)

Cartography, not judgment — with **evidence anchors** (quotes / heading pointers) per **SPEC-rules §8**.

Optional: a **second model** as synthesis auditor (see `docs/anti-sycophancy.md`).

---

## Session modes and models

- **`session_mode: council`** — distinct models intended; quorum applies when **≥2 distinct `model:` strings** among contributed agents (SPEC-rules §4.5).
- **`session_mode: rehearsal`** — single-model role-play; votes advisory.

Every agent entry in `votes.md` **must** have a non-empty **`model:`** string for audit.

---

## Customizing your council

Roles and agent counts are flexible. **Normative file layout and synthesis location are not** — see **SPEC-core §2** and **`docs/customization.md`**.
