# Enrich Mode

Goal: Enrich existing issues with context from any source.

Usage: `/devrev enrich` (auto-search Slack) or `/devrev enrich <URL|doc-name|keyword>`

Parse $ARGUMENTS rest as source hint.

## Phase 1 — Parallel fetchers

**A (Fetcher):** `list_issues(owned_by=[$USER_DON], state=["open","in_progress"])`
Return JSON: `[{iss_id, title, body_excerpt (first 200 chars)}]`

**B (Fetcher):** Fetch source based on hint:
- If URL: `WebFetch` or appropriate MCP read tool
- If doc name: `Google_Drive__search_files(<doc_name>)` then `Google_Drive__read_file_content(<id>)`
- If keyword (default): `slack_search_public_and_private("<keyword> after:<7d>")`
- Return source as structured snippets (one per relevant chunk, with source link)

## Phase 2 — Analyzer agent (sequential, after Phase 1)

**C (Analyzer):** Given (A's issues + B's snippets):
- Match snippets to issues by keyword overlap or explicit ISS-ID mention
- For each match, return:
  ```
  ISS-XXXX: matched on <keyword/ISS mention>
  Append to body:
  > <snippet text>
  > Source: <link>
  ```
- If no match: "no match for <snippet summary>"
- Max 10 matches, 200 words total

Note: PM PRDs (Track A issues with `[J*-S*]` codes) are valid read targets here for context. But DO NOT update PM-owned issues — only append to `$USER_DON`-owned issues.

## Phase 3 — Apply

Show diffs to user. On confirm: parallel `update_issue` calls.
Body appends only, never overwrites.
Use `## Context Update <date>` section header in the body.
