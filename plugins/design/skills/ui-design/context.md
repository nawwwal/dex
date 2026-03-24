# Context — Project Design Context Capture

Generates `.claude/DESIGN.md` — a persistent design context file that future sessions load automatically.

## Idempotency rules

1. If `.claude/DESIGN.md` exists and content is substantively unchanged → skip write
2. Add reference to CLAUDE.md only if the string "DESIGN.md" is not already present
3. Suggest adding `.claude/DESIGN.md` to `.gitignore` — don't auto-modify gitignore

## Mode Detection

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

## Step 1: Codebase exploration

Read these files to understand the project:
- `CLAUDE.md`, `AGENTS.md`, `README.md`
- `.cursor/rules/frontend-blade-rules.mdc` (if exists)
- `package.json` (stack, design system version)
- Scan `src/` for most-used component patterns

## Step 2: Design system discovery

### Blade mode
Call Blade MCP tools:
1. `hi_blade` — confirm version and availability
2. `get_blade_pattern_docs("Dashboard,ListView,DetailedView,FormGroup,Settings,CreationView,Confirmation")` — available page patterns
3. `get_blade_general_docs("Usage")` — setup and token reference

### Generic mode
- Grep for CSS custom properties (`:root { --color-* }`)
- Grep for most-imported components to identify design system
- Read component library (shadcn, radix, mantine, custom) from package.json

## Step 3: Generate DESIGN.md

Write to `.claude/DESIGN.md`:

```markdown
# Design Context — [Project Name]
Generated: [date]

## Stack
- Framework: [Next.js 16 / React / etc.]
- Design System: Blade [version] / [other]
- Styling: Tailwind / CSS Modules / etc.

## Design System Details (Blade mode)
- Version: [x.x.x]
- Available Patterns: Dashboard, ListView, DetailedView, FormGroup, Settings, CreationView, Confirmation
- Key components: Box, Text, Heading, Button, TextInput, Amount, Table, ...

## Color Tokens (sample)
- Primary action: surface.action.background.primary.intense
- Success: feedback.positive.background
- Text primary: surface.text.gray.normal

## Spacing
- Base unit: 4px (spacing.1 = 4px, spacing.4 = 16px, spacing.6 = 24px)

## Typography
- Body: Text size="medium" (16px)
- Heading: Heading size="medium"
- Display: Display size="xlarge"

## Design Principles (derived)
1. [Derived from codebase patterns]
2. [e.g., "Data-dense tables are the primary pattern — use ListView template"]
3. [e.g., "Blade Score target: 95%+"]

## Anti-patterns to avoid
- Hardcoded hex colors (use Blade tokens)
- Hardcoded spacing (use Blade spacing props)
- Custom components where Blade has an equivalent
- [Project-specific anti-patterns from code review]
```

## Step 4: Register in CLAUDE.md

If CLAUDE.md doesn't already reference DESIGN.md, append:
```
# Read .claude/DESIGN.md before any UI work
```

## Output

```
## Design Context captured

Generated: .claude/DESIGN.md
Blade version: 12.76.0
Available patterns: Dashboard, ListView, DetailedView, FormGroup, Settings, CreationView, Confirmation

Added reference to CLAUDE.md: yes / already present

Tip: Add .claude/DESIGN.md to .gitignore if you don't want to track it.
```
