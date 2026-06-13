# Dex Skill Rehaul Design Spec

**Date:** 2026-06-13  
**Scope:** council overhaul, communicate removal, media-tools merge, playground quality, diverge loosening

---

## 1. Council Real-Life Use Cases

Council is a multi-agent investigation engine. It must serve domains beyond code review.

| Domain | Example prompt | Mode | Goal |
|--------|---------------|------|------|
| Design critique | "Council this onboarding flow — UX, copy, visual hierarchy" | opinion | risks |
| Product strategy | "Should we ship AI recommendations or fix onboarding first?" | opinion | decision |
| Visual direction | "Review this brand direction before we diverge" | opinion | findings |
| Competitive research | "How do others handle payment failure UX?" | research | findings |
| Design system | "Audit our modal patterns across products" | system | risks |
| Handoff friction | "Why does design→eng handoff keep breaking?" | workflow | actions |
| Content/legal | "Review this KYC copy for risk surfaces" | opinion | risks |
| Architecture | "Map blast radius of changing the auth module" | code | findings |

### Skill boundaries

| Request | Route to |
|---------|----------|
| Find the crux / weak joint | `crux` |
| Generate design alternatives | `diverge` |
| Implement or build | dev skills |
| Single copy rewrite | `content-design` |
| Interactive artifact | `playground` |

---

## 2. Dynamic Lens Composition

Replace the fixed persona table in opinion mode with a **lens composer** that derives lenses per investigation.

### Inputs to lens composer

- `domain` — design, product, engineering, research, workflow, compliance
- `stakes` — what breaks if wrong (user trust, revenue, security, timeline)
- `decision_shape` — binary, prioritization, audit, open exploration
- `evidence_available` — fixtures, code, web sources, user opinion only
- `cost_bearer` — who pays for being wrong (user, eng, business, legal)

### Archetypes (composable, not fixed roles)

| Archetype | Focuses on | Natural skepticism |
|-----------|-----------|-------------------|
| skeptic | Hidden assumptions, failure modes | "obviously fine" claims |
| operator | Day-to-day execution, runbooks | Untestable abstractions |
| user_advocate | User job, cognitive load, recovery | Developer-centric defaults |
| craft_quality | Visual/copy/interaction craft | Decorative polish without mechanics |
| cost_complexity | Scope, timeline, maintenance | Scope creep, yak shaving |
| risk_compliance | Legal, security, regulatory surfaces | "We'll fix later" |
| evidence_mapper | Source quality, triangulation | Single-source certainty |

### Domain overlays

**Design:** `visual_hierarchy`, `copy_tone`, `state_coverage`  
**Research:** `source_quality`, `negative_space`  
**Workflow:** `handoff_owner`, `repeat_churn`  
**Product:** `adoption_risk`, `ROI`, `scope_fit`

### Hard rules

1. Always include at least one skeptic lens (may be devil's advocate or pre-mortem).
2. No two lenses share the same expertise area.
3. Each lens gets a one-line rationale: "chosen because [reason from inputs]."
4. Permanent lenses remain: core mapper, dependency/blast radius, devil's advocate, blind-spot.
5. Synthesis report adds `## Lens Rationale` listing derived lenses and why.

### Debate format (binary decisions)

1. Spawn advocate-for-A and advocate-for-B lenses.
2. Each steel-mans the opposing view before arguing.
3. Each states what evidence would change their mind.
4. Parent synthesizes agreement, crux of disagreement, and recommendation.

---

## 3. Deterministic vs Non-Deterministic Taxonomy

| Layer | Deterministic | Non-deterministic |
|-------|--------------|-------------------|
| Routing | mode/skill trigger, negative controls | ambiguous prompt feel |
| Structure | synthesis headings, artifact contract | persuasiveness of disagreement |
| Scripts | generate.py, Optimo CLI, validators | image aesthetic fit |
| Grounding | fixture refs, must_not inventing | visual language tied to topic |
| Quality | banned patterns (purple gradient, fake metrics) | playground craft, diverge novelty |

**Rule:** Every overhauled skill gets `scripts/validate_<skill>_skill.py` plus `evals/exhaustive-suite.json` with `deterministic_checks` on every case. Creative quality uses `judge_rubric` scored by eval runners.

---

## 4. Playground Root Causes and Fixes

### Problems

1. Evals check keywords, not rendered HTML quality.
2. Contract forces single interaction model; output feels generic.
3. No exhaustive suite; no HTML slop validator.
4. Tension with diverge: playground evals forbid multi-concept unless user asks.

### Fixes

| Change | Purpose |
|--------|---------|
| `build` mode | Single polished artifact (default) |
| `sketch` mode | Fast iteration; 2–3 variants when user asks for exploration |
| `assets/templates/` | Scaffold per interaction model, not blank page |
| `validate_playground_html.py` | Ban purple gradients, Inter defaults, fake metrics, lorem |
| Pre-build checklist | Visual grammar extraction before styling |
| Exhaustive suite | 35–40 cases including visual-quality judge rubric |
| Route `imagegen` → `tools:media-tools` | Unified media skill |

---

## 5. Diverge Loosening

### Depth tiers

| Tier | When | Output |
|------|------|--------|
| fast (default) | brainstorm, alternatives | 3–5 directions, minimal sections |
| explore | "show me options", early ideation | 5–8 directions; optional playground sketch companion |
| deep | explicit deep/layered/handoff | full layered framework |

### Changes

- Rename mental model: compact → fast.
- Reduce mandatory sections in fast mode.
- Keep copy guardrails only on risk surfaces (payments, deletes, secrets, permissions).
- Add explore-mode eval cases; relax brittle `must_not` checks that block legitimate directions.
- Maintain 47/47 regression on existing suite.

---

## 6. Tools Merge: media-tools

Merge `generate-image` + `media-optimizer` into `media-tools`. Keep `mymind`, `codex`, `html-presentation` separate.

| Operation | Freedom | Surface |
|-----------|---------|---------|
| Image generate/edit | Low | `scripts/generate.py` with pinned model IDs |
| Compress/convert/resize | Low | `npx optimo@0.0.24` pinned |
| Prompt crafting | High | SKILL.md natural-language path |
| Format choice | Medium | decision tree in SKILL.md |

---

## 7. Communicate Removal

Delete `plugins/core/skills/communicate/`. Skill was 24 lines, hardcoded Slack ID, no evals, depended on user-side `memory/voice.md`. Not worth maintaining in dex core.

Update: core plugin manifests, README, CLAUDE.md, AGENTS.md.

---

## 8. Eval Pass Rate Targets

| Skill | Deterministic | Judge rubric |
|-------|--------------|--------------|
| council (post-redesign) | ≥90% | ≥80% |
| playground (post-redesign) | ≥95% | ≥75% |
| diverge (post-loosen) | 100% (no regression) | maintain |
| media-tools | ≥95% | N/A |

---

## 9. Release Plan

| Plugin | Bump | Changes |
|--------|------|---------|
| core | minor | council overhaul, communicate removal |
| tools | minor | media-tools merge |
| design | patch | playground + diverge |
