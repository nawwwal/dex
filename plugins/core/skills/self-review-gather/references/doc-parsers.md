# Competency Doc Sources

## v1: Static Curated PD Summaries (current approach)

v1 uses curated PD-specific competency summaries that live in the skill's `references/competencies/parsed/` directory. These are the source of truth for competency framing during evidence collection.

**Files:**
- `parsed/culture.md` — Razorpay culture/values, Level 2 behaviors for each of the 6 values
- `parsed/technical.md` — IC Product Design Competency Framework, PD II (L2) behaviors for all competency areas
- `parsed/career-framework.md` — PD career framework, Impact and Leadership sections for PD II

These files are manually curated and updated. They do not require Google Doc access or browser automation.

**When to refresh:** If Razorpay updates the competency framework, manually copy the relevant PD II sections into the parsed files. Do not re-use the engineering-level content from the Career Framework 3.0 (that document covers SDE roles, not design roles).

## v2: Live Refresh via Google Workspace MCP (future)

A future version will support fetching the competency docs via the Google Workspace MCP (`get_doc_content`) and parsing the PD-specific sections. This is deferred because:

1. The existing curated summaries in `parsed/` are accurate for the current review cycle
2. Google Workspace MCP availability is not guaranteed in all environments
3. Parsing the docs reliably requires knowing the exact heading structure, which may change

The previous JavaScript browser parsers (using `evaluate_script` against Google Docs pages) have been removed. They relied on Chrome DevTools MCP and fragile DOM extraction.
