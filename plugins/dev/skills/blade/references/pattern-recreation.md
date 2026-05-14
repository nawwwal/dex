# Blade Pattern Recreation

Use this when the user asks to recreate a known Blade pattern exactly in one prompt: `Dashboard`, `ListView`, `CreationView`, `DetailedView`, `FormGroup`, `Settings`, `Confirmation`, or `SparkAnimation`.

This is a low-freedom workflow. Do not design a Blade-ish equivalent. Instantiate the Blade pattern contract from MCP, fill product data, and preserve the pattern's structural owners.

If the prompt names or implies one of these patterns, this file wins over `component-selection.md`.

## Required workflow

Follow these steps in order. Do not implement until the source packet and pattern lock exist.

```text
1. Identify exact pattern name from the table below.
2. Fetch source packet:
   - `get_blade_pattern_docs` for the exact pattern, with `currentProjectRootDirectory`
   - `get_blade_component_docs` for the required component docs from the table, with `currentProjectRootDirectory`
   - `get_blade_general_docs` for listed general docs such as `AvailableIcons`, with `currentProjectRootDirectory`
3. Write the Pattern Lock in your notes.
4. Implement by preserving the required structure and Blade owners.
5. Replace only product data, copy, route handlers, API state, and safe empty/loading/error variants.
6. Validate with browser proof and a pattern parity checklist.
```

## Pattern lock

Write this before code changes:

```text
Pattern: <exact Blade pattern>
Source packet: <pattern docs + component docs fetched>
Required structure: <regions/slots/sections from MCP examples>
Required Blade owners: <patterns/components that own behavior and surface>
Allowed variation: product copy, data, routes, callbacks, loading/empty/error states
Forbidden variation: custom layout model, custom surface, custom motion, replacing Blade owners
Validation target: <route/story/harness and viewport list>
```

If you cannot fill the `Required structure` from MCP, stop and fetch narrower docs. Do not infer the pattern from memory.

Component docs names must be valid MCP component names. If a pattern example mentions an internal or legacy name such as `TabNav`, fetch the public component docs name that MCP accepts, such as `Tabs`, and record the correction. Icons are not component docs; fetch `AvailableIcons` through general docs.

## Known pattern table

| User asks for | Pattern docs | Component docs to fetch after pattern docs | General docs when needed | Preserve exactly | Allowed variation |
| --- | --- | --- | --- | --- | --- |
| Dashboard shell, app chrome, merchant dashboard | `Dashboard` | `TopNav,SideNav,Tabs,Menu,Avatar,SearchInput,Badge,Indicator,Switch,Box,Text,Heading,Button,Link,Tooltip` | `AvailableIcons` | TopNav region, SideNav region, route workspace, active route state, product/account menu ownership. | nav labels, route paths, icons, account data, workspace contents. |
| Data list, transactions list, filterable table | `ListView` | `ListView,Table,QuickFilter,Dropdown,ActionList,Counter,Badge,Button,IconButton,Code,Amount,Box,SearchInput,ButtonGroup,Tooltip,Pagination` | `AvailableIcons` when row or filter actions need icons | ListView wrapper, filter region, quick filters, search, dropdown filters, table structure, pagination and row action ownership. | columns, rows, filter values, status labels, actions, empty/loading/error data. |
| Creation flow, object setup, guided form creation | `CreationView` | `Card,Button,StepGroup,ProgressBar,TextInput,SelectInput,Checkbox,Radio,Switch,Box,Heading,Text,Alert,Toast` | `AvailableIcons` when the docs use icons | creation shell, primary form flow, validation region, preview/summary region when provided by docs, step/progress ownership. | form fields, validation messages, preview data, submit handlers, success/error copy. |
| Detail drawer, transaction/user/entity detail | `DetailedView` | `Drawer,Card,InfoGroup,Amount,Badge,Button,IconButton,Table,Box,Heading,Text,Link,Tooltip` | `AvailableIcons` when actions need icons | drawer/detail container, header/title area, grouped facts, action hierarchy, responsive detail behavior. | entity fields, values, action callbacks, loading/error states. |
| Form layout, grouped inputs, validation | `FormGroup` | `InputGroup,TextInput,SelectInput,PasswordInput,PhoneNumberInput,DatePicker,TimePicker,Checkbox,Radio,Switch,TextArea,Button,Alert,Box,Text,Heading` | none by default | label/help/error ownership, grouped field spacing, required/disabled/validation states, submit action hierarchy. | field names, options, validation rules, submit/cancel callbacks. |
| Settings overview or detail page | `Settings` | `Card,SideNav,TopNav,Button,IconButton,Link,Switch,Box,Heading,Text,SearchInput,Menu,Avatar` | `AvailableIcons` | overview/detail split, settings card grid or settings detail sections, back navigation, setting row layout, switch/edit action ownership. | setting categories, labels, descriptions, route paths, values, callbacks. |
| Destructive/important confirmation | `Confirmation` | `Modal,BottomSheet,Box,Button,Text` | `AvailableIcons` | desktop `Modal`, mobile `BottomSheet`, title/description/icon or image area, primary/secondary action hierarchy, loading state for async confirm. | action text, consequence copy, icon/image, loading handler, positive/neutral/negative type. |
| Branded success/loading moment | `SparkAnimation` | `RazorSense,RazorSenseGradient,Box,Button,Heading,Text` | none by default | asset preload before mount, RazorSense background, RazorSenseGradient foreground, white-filled SVG mask, branded moment scope. | preset, icon/logo shape, success/loading copy, primary action. |

## Pattern parity checklist

Before marking complete, check:

```text
Pattern docs matched: <yes/no + exact pattern>
Component docs matched: <yes/no + component list>
Structure preserved: <regions/slots/sections retained>
Blade owners preserved: <no custom owner for surface/interaction/motion>
Data-only substitutions: <copy/data/routes/callbacks changed only>
Responsive behavior: <desktop + narrow/mobile checked or blocker>
Accessibility behavior: <focus, keyboard, labels checked or blocker>
Runtime proof: <browser route/screenshot/snapshot/diff or auth blocker>
```

## Failure rules

- If the prompt names or implies a known Blade pattern, do not start with `component-selection.md`; start here.
- If MCP docs include code examples, preserve their structural hierarchy before adapting names and data.
- If a pattern uses strict component slots, mirror the slots exactly. Do not insert arbitrary children into slots unless MCP permits it.
- If the app's installed Blade version lacks the pattern or a required component, record a limitation and use the nearest Blade-supported pattern. Do not create a custom clone.
- If auth blocks runtime proof, use `agent-browser.md` fallback wording and state that pattern parity is source-verified but runtime incomplete.
- If a component docs lookup fails, correct the name through MCP once and record the exact rejected name. Do not silently swap in an unverified alias.

## One-prompt output contract

When the user asks to recreate a known pattern in one prompt, the final response must include:

```text
Pattern recreated: <name>
MCP source packet: <pattern + component docs checked>
Blade owners used: <main owners>
Variations applied: <data/copy/routes/callbacks only>
Browser proof: <route/screenshot/diff/focus/responsive proof or blocker>
Blade gate: <score/audit/gate result or not run>
Static/tests: <typecheck/unit/source checks or not run>
Unverified: <none or exact runtime/API gap>
Limitations: <none or exact Blade limitation>
```
