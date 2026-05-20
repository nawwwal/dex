---
name: wrap
description: "Use when the user explicitly invokes /wrap or asks to wrap up, close out, checkpoint, finalize, or commit a coding session: summarize how the work started, what problem appeared, how it was fixed, what changed, what was verified, what remains, create meaningful micro-commits from the current diff, and run the portent skill when a durable knowledge-base handoff is needed. For coding-session recap-only requests, summarize but ask before committing."
---

# Wrap

End the current work session with a grounded recap, clean commit history, and a durable Portent record when the work is worth carrying forward.

`/wrap` means the user has authorized direct commit creation for the current task. Treat "close out this session", "checkpoint and commit", and "finalize the work" as wrap intent only when the user is talking about coding-session work. If this skill loads for a coding-session recap-only request without explicit commit intent, produce the recap and ask before committing. It does not mean push, deploy, release, or history rewrite unless the user explicitly asked for those.

## Evidence

Build the recap from source-of-truth evidence in this order:

1. Active conversation context.
2. `git status --branch --short`.
3. `git diff --stat`.
4. Focused diffs for changed files.
5. Recent commits.
6. Test, build, lint, or runtime output from this session.
7. Session transcripts only when active context is insufficient.

Do not invent chronology. If the evidence cannot prove how something started or was fixed, say what is unknown.

## Workflow

1. Inspect the current repo state before staging anything.
   - Run `git status --branch --short`.
   - Run `git diff --stat`.
   - Check staged changes separately with `git diff --cached --stat`.

2. Protect existing work.
   - Treat a dirty worktree as normal.
   - Keep unrelated local files, editor artifacts, and other users' changes unstaged.
   - If existing staged changes do not match the current task, stop and ask before unstaging or mixing them into commits.

3. Run pre-commit hygiene checks on changed files.
   - Search for newly introduced `TODO`, `FIXME`, placeholder text, and dead comments.
   - Check for hardcoded secrets, API keys, tokens, passwords, or credentials.
   - Check dependency manifests when package imports or dependency files changed.
   - In Dex, check README and release-doc drift when plugin topology, skill inventory, manifests, marketplace metadata, or user-facing behavior changed.

4. Design commit boundaries from the real diff.
   - Group by actual concern: feature, tests, docs, copy, config, release/runtime, or verification support.
   - Keep a large file in one commit if it is one cohesive change.
   - Do not split just to make the history look busy.
   - Do not sweep unrelated files into a commit because they are already dirty.

5. Create meaningful micro-commits.
   - If the diff is empty, do not create an empty commit.
   - Stage by exact path or hunk.
   - Use readable conventional messages tied to the concern, such as `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, or `chore:`.
   - Prefer the smallest commit sequence that makes review easier.
   - If verification exposes a small issue in the most recent commit, fix it and amend that commit instead of leaving a known-bad checkpoint.

6. Verify after committing.
   - Run the repo-appropriate checks when the change touched executable code, configs, docs gates, manifests, or tests.
   - If no meaningful check exists, say so.
   - Push, deploy, release, or create a PR only if the user explicitly requested it.

7. Run `portent` when the session deserves a durable handoff.
   - Run the existing `portent` skill after commits and verification when the session produced durable decisions, multi-step fixes, meaningful commits, unresolved next steps, or context worth preserving.
   - Do not run `portent` for empty diffs, trivial no-op recaps, or one-line throwaway tasks.
   - Let `portent` remain the canonical Tolaria/Portent writer; do not duplicate its object-writing rules here.

## Recap Format

Return this structure at the end:

```markdown
## Started With
[original goal in one or two concrete sentences]

## Problem Faced
[main blocker, bug, ambiguity, or drift]

## Fixes Made
[specific changes, grouped by concern]

## Decisions
[important choices and tradeoffs]

## Verification
[checks run and their result]

## Current State
[clean/dirty worktree state and intentionally remaining files]

## Next Steps
[only real follow-ups or "None"]

## Commits Created
[commit hashes and messages, or "None"]

## Knowledge Record
[Portent object/path or "Not needed: <reason>"]
```

Keep the final recap concise. The user needs the state of the work, not a transcript replay.
