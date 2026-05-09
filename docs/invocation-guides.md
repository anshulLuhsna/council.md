# Invocation Guides

How to run a council.md session in each major AI interface.

The protocol is the same regardless of which model or interface you use. What changes is how you load files into context. This guide covers the most common setups.

---

## The general pattern

For every agent turn:

1. Copy the files the agent needs (**during blind round:** usually `context.md` + `agents/[name].md` + **`drafts/[name].md`** — **not** full `discussion.md`; see **SPEC-rules §6**).
2. Paste into your AI interface.
3. Ask the agent to fill in their section.
4. Merge into `discussion.md` (or paste under the correct `### Agent:` stub).

For the **synthesizer**: paste `context.md` + full `discussion.md` (+ round splits if any) + `votes.md` + `synthesizer.md`, and instruct it to fill **`## Council Synthesis`** **inside `synthesizer.md` only** — never put synthesis in `discussion.md`. If you want the optional UI, have it also fill `## Summary UI Data` in the same file.

---

## File upload limit (5-file rule)

Most web interfaces (ChatGPT, Claude, Gemini) allow **up to 5 file attachments** per turn. Every council turn fits within that limit.

### Agent turn (blind round — recommended)

| # | File | Why |
|---|------|-----|
| 1 | `agents/[name].md` | The agent's role, mission, constraints, and output format |
| 2 | `context.md` | The question and constraints — the only shared anchor |
| 3 | `drafts/[name].md` | The agent's **own empty draft stub** — they write here (not discussion.md) |

3 files. Intentionally small — **no other agent's text is visible** during blind.

**Instruction to add (paste at the end):**
> "You are [Agent Name]. Your role is defined in the first file. Fill in your draft using the format shown. Do not read any other agent's section."

---

### Agent turn (non-blind / round 2)

| # | File | Why |
|---|------|-----|
| 1 | `agents/[name].md` | Role |
| 2 | `context.md` | Shared anchor |
| 3 | `discussion.md` | Full deliberation so far — agent may read others for Round 2 |

3 files. Add a 4th if needed (e.g. a supporting artifact the agent should review).

---

### Synthesizer turn

| # | File | Why |
|---|------|-----|
| 1 | `synthesizer.md` | Output instructions + where to write (`## Council Synthesis`) |
| 2 | `context.md` | Shared anchor |
| 3 | `discussion.md` | All contributions |
| 4 | `votes.md` | Participation / session mode / attestation |
| (5) | `discussion-r1.md` | Only if there was a round rollover |

4–5 files. All synthesis output goes **inside `synthesizer.md`**, not back into discussion.

**Instruction to add:**
> "You are the council synthesizer. Fill in `## Council Synthesis` in the synthesizer.md file above. Do not put any synthesis in discussion.md. If the template includes `## Summary UI Data`, fill that too so the session can generate `summary.html`."

---

### Coordinator turn (setup only — one time)

| # | File | Why |
|---|------|-----|
| 1 | `coordinator.md` | Interview + scaffolding instructions |

1 file. The coordinator writes `context.md` and stubs for the other files; you apply those locally.

---

### What to do if a file is too long

If `discussion.md` is very long (many agents, multiple rounds), it may approach an interface's paste limit. Options:

1. **Upload as a file** instead of pasting — most interfaces handle uploaded files better than pasted text.
2. **Use `discussion-r1.md` rollover** (see SPEC-rules §6b) — freeze the old discussion, start fresh.
3. **For the synthesizer only:** tell the model which round file to treat as canonical; it reads both.

---

## Claude (Web — claude.ai)

**Best for:** Long-context synthesis, nuanced reasoning, following structured markdown instructions reliably.

**How to load files:**

Option 1 — File upload *(recommended)*:
1. Open a new conversation.
2. Use the attachment button to upload the files for your turn — see the [5-file tables](#file-upload-limit-5-file-rule) above for exactly which files to include.
3. Add the instruction at the end of your message.

Option 2 — Paste directly:
1. Paste each file's content in order (role file first, then context, then draft or discussion).
2. Follow with the instruction.

**Tips:**
- Claude follows structured markdown sections very reliably. Use the exact heading format from the template.
- **Blind rounds:** upload only the 3-file blind set — never attach full `discussion.md` until the blind is closed.
- Start a fresh conversation for each agent to prevent context bleed between roles.

---

## Claude Code (VS Code / Cursor)

**Best for:** Running councils directly inside a codebase, keeping council files in your project, using the agent context window for large files.

**How to load files:**

Option 1 — Reference files directly (no upload needed):
```
Read `council/context.md` and `council/agents/strategist.md`. You are the Strategist. Fill in your section in `council/discussion.md`.
```

Option 2 — `@file` syntax:
```
@council/context.md @council/agents/strategist.md @council/drafts/strategist.md — fill in your blind draft
```

The 5-file limit **does not apply** here — Claude Code reads files directly from your project.

**Tips:**
- Run `council validate` before starting a session to confirm files are properly formatted.
- Claude Code's system prompt may include project context — useful for councils on technical decisions.
- For blind rounds: reference only `drafts/[slug].md` — **not** the full `discussion.md`.

---

## ChatGPT (Web — chatgpt.com)

**Best for:** GPT-5 reasoning, wide general knowledge, fast responses.

**How to load files:**

Option 1 — File upload *(recommended)*:
1. Open a new conversation.
2. Use the paperclip button to upload the files for your turn — see the [5-file tables](#file-upload-limit-5-file-rule) above for exactly which files to include.
3. Add the instruction at the end.

Option 2 — Paste directly:
1. Paste file contents in order: role file first, then context, then draft or discussion.
2. Add the instruction at the end.

**Tips:**
- GPT-5 follows structured markdown reliably but may add conversational preamble. Suppress with: *"Output only the filled-in agent section. No preamble."*
- Start a fresh conversation for each agent. GPT in a long conversation may start blending agent perspectives.
- Custom GPTs: configure the agent's role file as the system prompt so each agent turn is one message instead of three.

---

## Gemini (Web — gemini.google.com)

**Best for:** Long context windows, strong reasoning on technical topics, cross-referencing large documents.

**How to load files:**

1. Open a new conversation.
2. Use the attachment button to upload the files for your turn — see the [5-file tables](#file-upload-limit-5-file-rule) above.
3. Add the instruction.

**Tips:**
- Gemini Advanced (1M token context window) can handle very long discussion files reliably — the synthesizer turn works especially well here.
- Gemini may format its responses differently from the expected markdown structure. Add: *"Use exactly the heading structure defined in the role file's output format section."*
- For large councils (5+ agents with long contributions), Gemini's long context is particularly useful for the synthesis step.

---

## Local models (Ollama, LM Studio, etc.)

**Best for:** Full data privacy, no API costs, running councils on sensitive data.

**Compatible models:** Any model with a 16k+ context window. Recommended: Llama 3.3 70B, Qwen 2.5 72B, Mistral Large, DeepSeek R1 (for reasoning-heavy roles).

**How to load files in Ollama:**

Using the CLI:
```bash
ollama run llama3.3:70b "$(cat council/agents/strategist.md council/context.md council/discussion.md)"
```

Using Open WebUI (if installed):
1. Open a new conversation
2. Paste file contents directly
3. Follow with the instruction

**Tips:**
- Smaller local models (7B, 13B) may not follow structured markdown output reliably. Test with a simple prompt before running a full council.
- For councils on sensitive data, local models are the only option that guarantees data stays on your machine.
- 70B+ models at 4-bit quantization generally follow the protocol format reliably. Smaller models may need simplified role files.
- The synthesizer step is the most demanding — use your strongest available model for synthesis.

---

## API access (for advanced users)

If you have API access to any provider, you can run council turns programmatically — but this is optional tooling, not the protocol.

The council.md CLI (`cli/council.sh` and `cli/council.py`) does not make API calls. It scaffolds and validates only.

For programmatic council runs, you can pipe file contents to any API endpoint. The protocol structure maps directly to a single API call per agent:
- System prompt: agent role file contents
- User message: context.md + discussion.md (with prior contributions for round 2)

---

## Which model for which role?

There is no required mapping. Use what you have. Some patterns that work well:

| Role | Model characteristics that help |
|---|---|
| Strategist | Long-context, strong reasoning, good at second-order thinking |
| Operator | Practical knowledge, specific domain expertise |
| Risk Analyst | Conservative reasoning, strong at identifying gaps and failure modes |
| Challenger | Models that push back well — often frontier models with instruction-following |
| Synthesizer | Long-context, strong at comparison and structured output |
| Coordinator | Any capable model — this is mostly instruction-following and formatting |

If you are using one model for all roles: Claude Opus, GPT-5, and Gemini 2.5 Pro all handle multi-role councils well when run in separate conversations.
