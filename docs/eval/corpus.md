# Decision-class corpus (starter set)

Five **architecture / platform** decision classes with **publicly known or widely discussed outcomes** — useful for *qualitative* eval (not a formal benchmark). For each, craft a `context.md` *as if the decision were live*, then run baselines and council under **the same** context. Afterward, compare model recommendations to what history suggests.

The table is the index; **each sketch below** is a compact **context stub** you can expand into a full `context.md` (constraints, metrics, team size). This stays a **scaffold**: fully worked bundles with expert-rated outcomes are still on you — see **`example-eval-bundle.md`** for the recording format.

| # | Decision | Crux (one line) | Outcome anchor (for post-hoc sense-check) |
|---|----------|-------------------|------------------------------------------|
| 1 | **Microservices vs modular monolith** (early product) | Premature distribution vs team scaling | Many teams over-split early; successful early-stage orgs often keep a modulith until boundaries are clear. |
| 2 | **“Rewrite” vs incremental strangler** | Big-bang risk vs long overlap cost | Large rewrites often ship late; strangler often preserves revenue while migrating. |
| 3 | **Build internal platform vs buy SaaS** | Control vs speed to market | Common pattern: buy for non-differentiated workflows; build where IP or latency matters. |
| 4 | **Event-driven vs request/response core** | Async complexity vs peak handling | Eventing wins when domain events are first-class; adds ops burden when not. |
| 5 | **Multi-cloud vs single-cloud deep** | Exit vs discount complexity | Most teams pick one primary region/cloud; multi-cloud is often reserved for specific regulatory or scale patterns. |

---

### 1 — Microservices vs modular monolith

**Context sketch:** Early-stage product, one team, latency-sensitive core path, unclear bounded contexts.

**Good council output surfaces:** Team topology vs deployment topology; **premature split cost**; migration path if boundaries harden later.

**Sense-check (not a score key):** Industry lore — premature microservices correlate with ops drag without clear ownership boundaries.

---

### 2 — Rewrite vs strangler

**Context sketch:** Legacy codebase blocking features; revenue depends on old stack; partial observability.

**Good council output surfaces:** Parallel-run strategy; **feature freeze vs strangler slice**; rollback and staffing risk.

**Sense-check:** Full rewrites often slip quarters; stranglers trade overlap cost for continuity.

---

### 3 — Build platform vs buy SaaS

**Context sketch:** Internal workflow (billing, HR, CRM edge) — differentiation unclear.

**Good council output surfaces:** Build **only** where there is IP or latency arbitrage; integration boundaries; vendor lock-in mitigations.

**Sense-check:** Buy non-core is common; build stories cluster around data gravity and compliance.

---

### 4 — Event-driven vs request/response

**Context sketch:** Spiky traffic; growing need for audit trails; small ops team.

**Good council output surfaces:** Operational complexity of queues/outboxes; when events are domain truths vs implementation detail.

**Sense-check:** Event meshes reward mature ops; request/response stays default for small teams until pain is explicit.

---

### 5 — Multi-cloud vs single-cloud

**Context sketch:** Growth-stage org; fear of lock-in; no regulatory mandate yet.

**Good council output surfaces:** Real exit vs theoretical exit; network and egress economics; **minimum viable portability** (e.g. containers + IaC) vs multi-active.

**Sense-check:** Most shops standardize on one primary cloud unless regulation or scale forces otherwise.

---

**How to use:** do not “grade” against the sketches as an answer key — use them to **frame** what strong analysis should *surface* (tradeoffs, preconditions, kill criteria). Record scores in **`rubric.md`** / **`example-eval-bundle.md`**.
