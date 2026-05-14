# Blade MCP Workflow

Blade MCP is exact-name lookup. The skill's job is to convert product language into component names before calling MCP.

Use `surface-taxonomy.md` for the source-truth ladder. Short version: installed app version and MCP own API truth; public Storybook/index helps with vocabulary and examples; local app source is fallback evidence, not design-system proof. Use `interaction-quality.md` when MCP proves an API exists but product fit is still questionable.

## Call shape

Every Blade MCP lookup must include the consumer app root:

```text
get_blade_component_docs({
  currentProjectRootDirectory: "<absolute consumer app root>",
  componentsList: "Button,Card,Modal",
  clientName: "cursor"
})

get_blade_pattern_docs({
  currentProjectRootDirectory: "<absolute consumer app root>",
  patternsList: "Dashboard,ListView",
  clientName: "cursor"
})

get_blade_general_docs({
  currentProjectRootDirectory: "<absolute consumer app root>",
  topicsList: "AvailableIcons,ChartColorSystem",
  clientName: "cursor"
})
```

If MCP is unavailable, unauthorized, or times out, do not claim Blade API truth. You may inspect `package.json`, local imports, and existing code to understand the installed version and local usage, but final notes must say `MCP unavailable; API unverified`.

## Root selection

Always pass the consumer app root as `currentProjectRootDirectory`.

Correct:

```text
/Users/aditya.nawal/projects/test-dashboard
```

Wrong:

```text
/Users/aditya.nawal/projects/dex
.
/
```

If `get_blade_component_docs` returns a project setup error such as missing Cursor rules, re-check that the root is the app being edited. Do not treat that as proof Blade lacks the component.

Stop after one root correction attempt. Classify the result instead of looping:

| Result | Meaning | Next action |
| --- | --- | --- |
| `root/setup failure` | MCP cannot read the consumer app setup. | Verify `package.json`, cursor rules, and app root; then fall back to existing code patterns plus source inspection. |
| `component not found` | Exact component name was unavailable. | Return to `component-selection.md` for one alternate candidate set. |
| `docs constraint found` | MCP returned allowed props/children/triggers. | Implement within those constraints; do not keep searching for a prop that is absent. |

After one alternate candidate set, stop and write a rejection log with the exact names checked. Do not keep guessing aliases.

## Lookup sequence

1. For page architecture, call `get_blade_pattern_docs` before components.
2. For specific UI surfaces, map product phrase to candidate names from `component-selection.md`.
3. Call `get_blade_component_docs` with the candidate list.
4. Read the docs for structure, not just prop names:
   - allowed children and slot components
   - deprecated or trap-prone props
   - trigger names and controlled-vs-uncontrolled behavior
   - examples that reveal required wrappers/providers
5. Use the minimal component variant that satisfies the interaction.
6. If docs reveal a constraint, follow it even when TypeScript accepts broader children.

## Required lookup examples

| Task language | MCP call |
| --- | --- |
| Dashboard shell with nav | Verify pattern name first; then component docs for `TopNav,SideNav,Tabs,Menu,Avatar` |
| Profile/account menu | Component docs for `Menu,Avatar,ActionList,Dropdown`; prefer `Menu` for actions |
| Test mode banner | Component docs for `Alert` |
| Setup accordion or step flow | Component docs for `StepGroup,Accordion,ProgressBar` |
| Payment overview cards | Component docs for `Card,Amount,Badge,Skeleton,EmptyState` |
| Card carousel with hover/press feedback | Component docs for `Carousel,CarouselItem,Card,AnimateInteractions,Elevate,Scale` |
| Payment split chart | Component docs for `DonutChart` and general docs for `ChartColorSystem` |
| Motion primitives | Component docs for `AnimateInteractions,Fade,Move,Slide,Scale,Morph,Stagger,Elevate` |
| Branded success/loading animation | Verify pattern name first; then component docs for `RazorSense,RazorSenseGradient` |

## MCP interpretation rules

- If MCP shows a prop that conflicts with product fit, treat it as available API, not automatically the best choice. Prefer an implementation that declares ownership and can be verified.
- If a component has strict child slots, mirror that structure exactly. Do not bypass slot constraints with fragments or arbitrary children unless MCP explicitly allows them.
- If product quality depends on a value MCP does not expose, do not invent a Blade prop and do not recreate the component with custom CSS or undocumented Framer wrappers. Use the nearest Blade-native behavior and record the limitation.
- If MCP fails with project setup errors from the Dex repo, switch to the consumer app root before concluding a component is missing.
- If public Storybook/index does not expose a name, treat it as a vocabulary warning, not proof Blade lacks the capability. Check MCP against the installed consumer app and record exact names tried.
- Do not add arbitrary Framer Motion, CSS transition, timer, or keyframe wrappers. If MCP docs for a Blade-owned component explicitly require `framer-motion` or `AnimatePresence`, treat that as a documented dependency for that component only, and keep the Blade component/pattern as the semantic owner.

## Limitation log

When the exact request cannot be expressed in Blade, record:

```text
Blade candidate checked: Alert
Limitation: required visual treatment is not expressible with Alert props
Blade-native fallback: Alert with closest supported color/emphasis/actions
Not used: custom surface, Blade internals styling, undocumented motion wrapper
Follow-up risk: verify hierarchy and action clarity in browser
```

Do not write broad custom CSS against `data-testid`, Blade internal DOM, nested `button`, or `[role='button']` selectors. That is a drift signal, not a stable API.
