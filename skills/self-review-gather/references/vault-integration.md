# Vault Integration Reference

## Canonical Paths (absolute — never relative)

| File | Purpose |
|------|---------|
| `~/.claude/memory/goals.md` | Competency weights, current ratings, Evidence Log sections |
| `~/.claude/career/case.md` | Existing evidence entries (dedup source) |
| `~/.claude/career/gaps.md` | Named competency gaps (collection targeting) |
| `~/.claude/memory/nawal-through-others.md` | Third-person signals (supporting framing) |
| `~/.claude/memory/decisions.md` | Decision log with Evidence Log sections |
| `~/.claude/log/` | Session journals (YYYY-MM-DD-*.md) |
| `~/.claude/state/self-review-gather/runtime.json` | Runtime state (capabilities, privacy scope, review period) |
| `~/.claude/state/self-review-gather/case-candidates.md` | Collection output (user reviews and copies to case.md) |

---

## QMD Queries (one per competency)

Run via `qmd_query` with collections: `log`, `memory`, `learn`, `work`, `career`.

| Competency | QMD Query | Weight |
|------------|-----------|--------|
| UX Design | `"crafted designed prototype user flow iteration hallway testing edge case coverage"` | 35% |
| UI Design | `"Blade Score design system component contribution handoff micro-interaction transition"` | 25% |
| Communication & Collaboration | `"stakeholder presentation alignment MoM design decision buy-in forum"` | 15% |
| Product Thinking | `"problem definition data-driven metrics research user insights OKR prioritization"` | 10% |
| Ownership & Delivery | `"shipped delivered owned end-to-end product area backlog planning"` | 10% |
| Leadership | `"mentorship feedback buddying team onboarding AI literacy tooling team building"` | 5% |

---

## Dedup Rules

**Primary key** (preferred when an artifact URL is present):
```
sha256(normalize(artifact_url))
```

**Secondary key** (when no artifact URL available):
```
sha256(normalize(workstream) + normalize(date_bucket) + normalize(first_8_words_of_entry))
```

**Normalization**: lowercase, strip trailing slashes, collapse whitespace, remove query params from URLs.

**Dedup check order**:
1. Check primary key against `career/case.md` entry URLs — skip if already present
2. Check secondary key against `career/case.md` text — skip if match confidence > 0.8
3. Check against already-found candidates within this collect run — merge if same key

**Cross-source merge**: If vault + DevRev or vault + Slack surface the same achievement (same artifact URL or same dedup key), merge into a single candidate with multiple source refs. Do not generate two candidates for the same achievement.

---

## Case.md Entry Format

Entries in `career/case.md` follow this structure (for reference during dedup):

```
N. [Action verb] [what was done] [outcome/artifact] [stakeholders] [DevRev/Figma/Slack link]
```

When scanning for dedup, extract:
- Embedded URLs (Figma, GitHub, DevRev, Slack)
- Workstream (infer from surrounding context heading)
- Date (from session log filename or DevRev creation date)

---

## Using nawal-through-others.md

Signals from `memory/nawal-through-others.md` are third-person observations about the user's work. Use them as **supporting framing** for existing candidates:

- If a candidate matches a third-person signal (same project, same timeframe), add the signal as corroboration in the candidate's source description
- Do NOT use third-person signals as standalone evidence — they are not authored by the user
- Signals are especially useful for Leadership and Communication competencies where external validation strengthens the entry

---

## Session Log Mining

Session logs in `~/.claude/log/YYYY-MM-DD-*.md` contain Evidence Log sections with competency claims. These are high-quality signals because they were written immediately after the work.

When mining session logs:
- Filter by date range from `runtime.json.reviewPeriod`
- Look for sections titled `## Evidence Log`, `### Week of YYYY-MM-DD`, or competency-tagged entries
- Extract entries with `[solid]` or `[evolving]` confidence markers as strong candidates
- Cross-reference against DevRev issue IDs and Figma links embedded in entries for dedup

---

## Prohibited Vocabulary

These terms indicate engineering-role content has leaked into competency docs or candidate text. Fail hard if found in `references/competencies/parsed/`:

- "Senior Software Engineer" / "Software Engineer"
- "Engineering Excellence"
- "SDE", "SSDE", "SDE-2"
- "system design"
- "code quality"
- "codebase" (in competency context)
- "tech debt"
- "RCA"
- "production systems"

**Allowed** in candidate text from actual Slack/DevRev/vault content (where engineering discussions are legitimate): filter only from competency reference docs.

---

## Redaction Policy (unified, all sources)

Before writing any text to `case-candidates.md`:

1. **Customer/merchant names**: replace with "a merchant" or "a partner"
2. **Commercial figures** (revenue amounts, transaction values): replace with "[amount]"
3. **Private channel names**: replace with "[private channel]"
4. **Confidential issue numbers** (internal only): generalize to "an internal issue"
5. **PII** (email addresses, phone numbers): remove

Preserve: Razorpay team member handles (@Varghese, @Kamlesh), public product names (Agent Studio, SG PayNow), public GitHub/Figma/DevRev links, Blade component names.
