# Skill Tests: polish

## Category: Encoded Preference

## True Positives — Spec Path (should trigger, ask A/B or short-circuit)
1. `/polish plans/feature-spec.md` → Spec path, A/B question (no intent signal)
2. "challenge this plan" (spec in context) → Mode A directly, no A/B prompt, no apply offered
3. "rewrite this PRD" (spec in context) → Mode B directly, no A/B prompt, apply offered
4. "polish this PRD" → Spec path, A/B question
5. "SIMPLER AND DUMBER" + spec in context → Mode A directly

## True Positives — Prose Path (should trigger)
1. `/polish this email` + pasted text → Prose path, cleaned prose + summary
2. `/polish README.md` → Prose path (no spec markers), Elements of Style pass
3. "tighten this Slack message" (message in context) → Prose path

## True Negatives (should NOT trigger or should redirect)
1. `/polish src/foo.ts` → Immediate redirect: "For code use /simplify"
2. Explicit `/polish my UI` → Redirect to /ui-design
3. Pasted TypeScript block → Code gate → redirect to /simplify
4. Pasted JSON-only block → Code gate → redirect to /simplify
5. "refine the code" → Code gate → redirect to /simplify
6. "tighten this" (no referent in context) → Ask: "What should I polish — spec or prose?"

## Edge Cases
1. `/polish nonexistent.md` + pasted prose → Note missing file; process pasted text
2. `/polish a.md b.md` (spec + prose) → Sequential; pause per spec for A/B if no intent; apply list excludes Mode A
3. `/polish a.md src/foo.ts` → foo.ts redirected, a.md previewed
4. Mode A + "apply" → "Challenge output is analysis only — nothing to apply"
5. "apply" with no preview → "Apply what? Nothing previewed yet."
6. "polish the intro of spec.md" → Section-only spec path; skill resolves section; preview; apply with hash revalidation
7. File changed before apply → "File changed since preview — re-preview required."
8. Prose doc with YAML frontmatter, fenced code, markdown table → all preserved verbatim
9. voice.md missing → Neutral clarity pass, no error shown
10. PRD beginning with `---` frontmatter + prose body → classified as spec, NOT redirected as code

## Quality Bar
- Good: detects input type correctly, routes to right path, previews before editing, asks A/B for specs without intent signal, preserves all code/frontmatter/tables verbatim
- Poor: edits files without preview, processes code instead of redirecting, applies Mode A results
