---
name: polish
description: Use when the user explicitly asks to polish, tighten, or refine a spec, plan, PRD, email, Slack draft, or other written document. Does NOT handle code or config — redirects to /simplify. Generic verbs only trigger when a written document or message is the established referent in context.
allowed-tools: Bash, Read, Edit, Grep, Glob
---

# Polish — Written-Artifact Quality Pass

Quality pass for specs, plans, PRDs, emails, and Slack messages.
Code and config are never processed here — redirect to /simplify.

## Step 1: Input Detection

Run in this precedence order:

1. **Explicit file path in `$ARGUMENTS`** — check code denylist first. If code/config: redirect immediately. If file doesn't exist: report error; if pasted content is also in the prompt, fall back to it and note the missing file.
2. **Pasted or quoted block** — run code detection gate, then classify
3. **Conversation referent** ("this spec", "the plan above", "my email") — run code gate, classify
4. **No clear referent** → ask: "What should I polish — a spec/plan, or a message/email/doc?"

Generic verbs ("tighten this", "refine this") only trigger when a document or message is the established referent in context. Otherwise ask.

**Explicit `/polish my UI`**: redirect to /ui-design.

## Code/Config Denylist

**Extensions:** `.ts` `.tsx` `.js` `.jsx` `.py` `.go` `.rs` `.rb` `.java` `.cs` `.cpp` `.c` `.h` `.sh` `.bash` `.zsh` `.css` `.scss` `.sass` `.sql` `.graphql` `.json` `.yaml` `.yml` `.toml` `.xml` `.lock`

**Filenames:** `Dockerfile` `Makefile` `Gemfile` `Rakefile` `package.json` `tsconfig.json`

**Extensionless files:** sniff first line — if it starts with `#!/`, `<?`, or `package ` → redirect to /simplify.

## Code Detection Gate (for pasted/non-file inputs)

Before classifying pasted or quoted content, sniff for code signals:
- Fenced code block with a language tag (` ```ts `, ` ```python `, ` ```bash `, etc.)
- The **entire input** is a bare JSON object or YAML-only block (no surrounding prose). A PRD that begins with `---` frontmatter but has prose after it is NOT code — classify normally.
- Import/require/package patterns (`import `, `from `, `require(`, `package main`)
- Shebang pattern (`#!/`)
- High brace/semicolon density (>15% of non-whitespace chars) with no prose paragraphs

If code signals detected → redirect: "This looks like code. Use /simplify for code cleanup."

A prose or spec doc that *contains* fenced code blocks or YAML frontmatter is classified as prose/spec — the embedded code is preserved verbatim (see Preservation rule below).

## Content Classification

- **Spec/plan/PRD**: `.md` explicitly named spec/plan/PRD/design-doc, or clear structural headings (Goals, Requirements, Acceptance Criteria, Architecture)
- **Prose**: emails, Slack drafts, plain text, `.md` without spec markers (e.g. README)
- **Ambiguous**: ask one clarifying question

## Preservation Rule (applies everywhere)

Never rewrite fenced code blocks, inline code, YAML frontmatter, JSON blocks, or markdown tables. Treat them as inert. Preserve verbatim regardless of path.

## Output and Edit Semantics

| Input type | Mode | Default output | "apply" behavior |
|---|---|---|---|
| Explicit file path | Mode B (rewrite) | Preview in chat | Edit only changed sections |
| Explicit file path | Mode A (challenge) | Challenge list | "apply" has no meaning — say so |
| Section selector | Mode B | Preview section only | Revalidate file hash → edit if unchanged |
| Section selector | Mode A | Challenge list for section | "apply" has no meaning |
| Pasted text | Either | Inline output | — |
| Conversation referent (not a file) | Either | Inline output | — |

**Section resolution**: read the file; resolve sections by heading text or line range. Supported selectors: "the intro", "the section called X", "lines 10–30", "the first section". If ambiguous, ask one disambiguation question — never ask the user to paste the section.

**Section drift protection**: capture the resolved anchor + file mtime/hash at preview time. On "apply", revalidate — if file changed, refuse: "File changed since preview — re-preview required."

**Multi-file batches** (`/polish a.md b.md`): process sequentially. Skip code/config files with a redirect note. For each spec file without a clear intent signal, pause and ask Mode A/B before proceeding to the next file. After all Mode B previews, offer: "Apply to [list], apply all, or none?" Mode A results are never part of apply batches.

**"apply" with no prior preview**: "Apply what? Nothing has been previewed yet."

## Spec Path — Dual Mode

**Intent short-circuit — if the user's prompt already signals intent, skip the A/B question:**
- "challenge this plan", "tear down this spec", "what can we cut", "SIMPLER AND DUMBER" → Mode A
- "rewrite this PRD", "tighten the language", "clean up this spec" → Mode B

**Otherwise ask:**
> "For specs: (A) challenge it — SIMPLER AND DUMBER lens, what to cut; or (B) rewrite — tighten language and structure. Which?"

### Mode A — Challenge (analysis only, never edits files)

1. Re-read the spec
2. Apply the lens: "How can we make this SIMPLER AND DUMBER while still achieving our goals?"
3. Surface:
   - Steps that can be cut without losing the goal
   - Over-engineered solutions (solving a future problem, not the present one)
   - Baked-in assumptions that should be questioned
   - Over-specified goals
4. Output: annotated challenge list
5. Offer: "Want a /council multi-agent challenge round on top of this?"

### Mode B — Rewrite

1. Tighten language, remove redundancy, sharpen structure
2. Apply Elements of Style: active voice, specific language, omit needless words
3. Preserve fenced code, frontmatter, tables, JSON blocks verbatim
4. Output: rewritten spec + change summary; previewable and applyable

## Prose Path — Elements of Style Pass

1. Apply Strunk rules: omit needless words, active voice, positive form, specific language
2. Preserve fenced code, inline code, tables, frontmatter verbatim
3. Voice.md lookup: `~/.claude/memory/voice.md` (Claude Code runtime). If present, load and match tone. If missing, apply neutral clarity pass silently.
4. Output: polished prose + 1-sentence summary of changes

## What NOT to Do

- Never process code files — redirect to /simplify
- Never overwrite a file without an explicit "apply" from the user
- Never ask the user to paste a section when the file path is known — resolve it yourself
- Never include Mode A results in apply batches
- Never touch fenced code, frontmatter, tables, or JSON blocks
