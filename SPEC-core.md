# council.md — SPEC-core (compliance contract) v0.2

> The **smallest** rule set that defines **council.md–compatible**. Operational detail lives in **[SPEC-rules.md](SPEC-rules.md)**.

---

## 1. What this is

**council.md** is a markdown-based protocol for running a structured council of AI models on a hard decision, review, or planning problem. Each model reads shared files, contributes its independent perspective, and stops. A synthesizer maps agreement, disagreement, and open terrain. The human decides.

The protocol is:

- **Markdown-first** — every file is human-readable and editable  
- **Provider-agnostic** — Claude, ChatGPT, Gemini, local models, or any mix  
- **File-first and runnable without a runtime** — no API keys, shared runtime, or orchestration code are required  
- **Human-in-the-loop by design** — the human controls every phase transition  

---

## 2. Normative core

Forks are encouraged. Custom roles and agent counts are encouraged. For a session to claim **spec compliance with council.md v0.2**, these **MUST** stay stable:

| MUST NOT change | Why |
|---|---|
| Filenames: `coordinator.md`, `context.md`, `discussion.md`, `votes.md`, `synthesizer.md`, `agents/*.md` | Interop and tooling |
| Phase **names** and **order** in `votes.md` frontmatter `status:` | Lifecycle semantics |
| Agent contributions under `### Agent:` in `discussion.md`; subsections use **`####`** (`#### Position`, etc.) — never **`##`** under an agent block | Parsing and synthesis anchors |
| **`votes.md` phase is authoritative only in YAML frontmatter** (`status:`) — not duplicated in narrative-only headings that contradict YAML | Single source of truth |
| **Council synthesis output only under `## Council Synthesis` in `synthesizer.md`** | Avoids split-brain outputs |
| **`## Human Decision` only in `synthesizer.md`** | Decision record location |
| Motions and vote tables **after** `## Phase Transition Log` as **`### Motion: …`** sections (same file, document order after the log heading) | Separation from deliberation |

Everything else — role names, number of agents, optional `drafts/`, optional round rollover files — is **customization**, not a separate protocol. Conventions for those are in **SPEC-rules**.

---

## 3. Authoritative text vs tools (CLI)

**The contract is your markdown files + SPEC-core (+ SPEC-rules where cited), not a program.** A session can be fully compliant without running the reference CLI (`cli/council.py`).

- **`council validate`** (default) — best-effort checks; **warnings** are common for work-in-progress sessions. Many warnings correspond to guidance in **SPEC-rules** (operational hygiene), not always §2 violations.
- **`council validate --strict`** — intended for CI: promotes **detectable violations of §2** (and closely related heading/layout checks) to **errors**. Not an exhaustive mechanical proof of §2 — see **`cli/README.md`**.

---

## 4. Core files

Every council session uses:

| File | Purpose |
|---|---|
| `coordinator.md` | Interview, scaffolding, turn order |
| `context.md` | Problem, constraints, success criteria |
| `discussion.md` | **Agent contributions only** — **no synthesis** |
| `votes.md` | Phase (`status:`), voting, session metadata |
| `synthesizer.md` | **`## Council Synthesis`** + **`## Human Decision`** |
| `agents/[name].md` | Role definition and contribution shape |

Optional **`drafts/`** and optional **`discussion-r*.md`** rollover files are allowed; semantics in **SPEC-rules**.

---

## 5. Lifecycle

Phases — exact strings for `status:` in `votes.md` frontmatter:

```
open → contributing → synthesizing → decided → archived
```

| Phase | Meaning |
|---|---|
| `open` | Coordinator finished setup; context and stubs exist |
| `contributing` | Agents may append to `discussion.md` (or `drafts/` during blind) |
| `synthesizing` | Deliberation closed; synthesizer writes **`## Council Synthesis`** in **`synthesizer.md` only** |
| `decided` | Human recorded decision under **`## Human Decision`** in **`synthesizer.md`** |
| `archived` | Session closed |

Only **`status:`** in **`votes.md` YAML** is authoritative for the current phase.

---

## 6. Minimum model audit fields (`votes.md`)

**Compliance requires:**

1. Each registered agent has a **non-empty `model:`** string (self-declared audit label).  
2. **`session_mode:`** is either **`council`** or **`rehearsal`** (see **SPEC-rules §4.4** for meaning).  
3. **`distinct_underlying_models_attested`** — boolean; honest self-report when **`session_mode: council`** and you claim distinct backends were used. **Not cryptographically verifiable** — see **SPEC-rules §4.5**.

Quorum and voting implications of `model:` / attestation are spelled out in **SPEC-rules §4–5**.

---

## Versioning

**SPEC-core** version bumps only when **§2** (normative core) or **§5–6** contract elements change in a breaking way. Operational edits live in **SPEC-rules** unless they force forks to change files — then **SPEC-core** must move too (see **SPEC-rules** versioning note).

---

*council.md is MIT licensed. Fork it, adapt it, run it.*
