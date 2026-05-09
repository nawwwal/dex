# Output Media

Use this when the user specifies code, Paper, or Figma.

## Code

Default medium. Choose the smallest faithful code surface:

- React route/page when the source is a React app, real components are needed, or motion uses a JavaScript motion library.
- Self-contained HTML/SVG when the source is static, CSS-only, or a faithful standalone recreation is feasible.

For React output, ask for the target route/path before writing files.

## Paper

Use Paper MCP when available. If Paper MCP is unavailable in the session, fall back to code and explicitly say Paper MCP was unavailable.

Do not call HTML output "Paper". Paper means the actual Paper tool surface.

## Figma

Use `figma:figma-use` before every `use_figma` call.

Figma output should create editable frames/objects, not flattened images, unless the user explicitly asks for an image import. Use native Figma annotations where available:

- Create or reuse annotation categories through `figma.annotations`.
- Set node `annotations` for implementation notes, state notes, measurements, and accessibility notes.
- Add visible comment pins/callout labels for review discussion.

Do not claim native Figma comment threads were created unless the available MCP exposes a comment-thread API.
