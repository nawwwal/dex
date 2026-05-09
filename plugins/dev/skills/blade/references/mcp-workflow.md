# Blade MCP Workflow

Blade MCP is exact-name lookup. The skill's job is to convert product language into component names before calling MCP.

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

## Lookup sequence

1. For page architecture, call `get_blade_pattern_docs` before components.
2. For specific UI surfaces, map product phrase to candidate names from `component-selection.md`.
3. Call `get_blade_component_docs` with the candidate list.
4. Use the minimal component variant that satisfies the interaction.
5. If docs reveal a constraint, follow it even when TypeScript accepts broader children.

## Required lookup examples

| Task language | MCP call |
| --- | --- |
| Dashboard shell with nav | `get_blade_pattern_docs("Dashboard")`, then `get_blade_component_docs("TopNav,SideNav,Menu,Avatar")` |
| Profile/account menu | `get_blade_component_docs("Menu,Avatar,ActionList,Dropdown")` and prefer `Menu` for actions |
| Test mode banner | `get_blade_component_docs("Alert")` |
| Setup accordion or step flow | `get_blade_component_docs("StepGroup,Accordion,ProgressBar")` |
| Payment overview cards | `get_blade_component_docs("Card,Amount,Badge,Skeleton,EmptyState")` |
| Payment split chart | `get_blade_component_docs("DonutChart")` and `get_blade_general_docs("ChartColorSystem")` |

## Rejection log

When custom UI remains, record:

```text
Blade candidate checked: Alert
Rejected because: required visual treatment is not expressible with Alert props
Custom surface kept: one wrapper div for layout only; content/actions still use Blade
Follow-up risk: CSS must use tokens and must not style Blade internals
```

Do not write broad custom CSS against `data-testid`, Blade internal DOM, nested `button`, or `[role='button']` selectors. That is a drift signal, not a stable API.
