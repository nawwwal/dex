# Context — Project Design Context Capture

Generates `.agents/DESIGN.md`, a project design context file for future UI work.

## Idempotency rules

1. If `.agents/DESIGN.md` exists and content is substantively unchanged, skip the write.
2. Add a reference to `.agents/AGENTS.md` only if the string "DESIGN.md" is not already present.
3. Suggest adding `.agents/DESIGN.md` to `.gitignore` if the project should not track local design context. Do not auto-modify `.gitignore`.

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
2. `get_blade_pattern_docs({ currentProjectRootDirectory: "<absolute project root>", patternsList: "Dashboard,ListView,DetailedView,FormGroup,Settings,CreationView,Confirmation,SparkAnimation", clientName: "cursor" })` — available page patterns
3. `get_blade_general_docs({ currentProjectRootDirectory: "<absolute project root>", topicsList: "Usage,AvailableIcons", clientName: "cursor" })` — setup, icons, and token reference
4. For motion-heavy projects, `get_blade_component_docs({ currentProjectRootDirectory: "<absolute project root>", componentsList: "AnimateInteractions,Fade,Move,Slide,Scale,Morph,Stagger,Elevate,RazorSense,RazorSenseGradient", clientName: "cursor" })`

### Generic mode
- Grep for CSS custom properties (`:root { --color-* }`)
- Grep for most-imported components to identify design system
- Read component library (shadcn, radix, mantine, custom) from package.json

## Step 3: Generate DESIGN.md

Write to `.agents/DESIGN.md`:

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
- Pattern recreation rule: for Dashboard, ListView, CreationView, DetailedView, FormGroup, Settings, Confirmation, or SparkAnimation, use Blade pattern docs before adapting local near-match code.
- Motion rule: use Blade motion primitives and MCP-documented dependencies; do not add custom CSS transitions, keyframes, timers, or undocumented Framer wrappers.

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

## Step 4: Register in AGENTS.md

If `.agents/AGENTS.md` exists and does not already reference `DESIGN.md`, append:
```
# Read .agents/DESIGN.md before any UI work
```

## Output

```
## Design Context captured

Generated: .agents/DESIGN.md
Blade version: [detected from MCP/package.json]
Available patterns: [detected from MCP]

Added reference to .agents/AGENTS.md: yes / already present

Tip: Add .agents/DESIGN.md to .gitignore if you do not want to track it.
```
