# Component Selection

Use this map before querying Blade MCP. It translates product language into Blade vocabulary so agents do not treat Blade as a parts bin.

## High-risk mappings

| Product phrase | Blade candidate | Use when | Avoid |
| --- | --- | --- | --- |
| Dashboard shell, app chrome, merchant dashboard | `Dashboard` pattern, `TopNav`, `SideNav` | The page has global navigation, account controls, and a main workspace. | Custom sidebars, custom sticky nav rows, CSS-only active states. |
| Account nav, settings nav, product nav | `SideNav`, `SideNavBody`, `SideNavFooter`, `SideNavSection`, `SideNavLink`, `SideNavItem` | Navigation persists across pages or has active route state. | `Box` rows with click handlers. |
| Profile menu, account menu, avatar menu, overflow actions | `Menu`, `MenuOverlay`, `MenuHeader`, `MenuItem`, `MenuFooter`, `Avatar` | The trigger opens actions or account options. | `Dropdown` unless the interaction is selection/input-like. |
| Test mode strip, banner, inline warning, activation notice | `Alert` | The surface communicates status, risk, notice, or next action. Use `isFullWidth` for strips. | Colored `Box` with icon and actions. |
| Setup flow, onboarding steps, progress steps | `StepGroup` first, `ProgressBar` when linear progress matters | The user must understand sequence and current step. | Custom numbered rows unless Blade cannot express the interaction. |
| Independent collapsible setup sections | `Accordion` | Sections can open independently and order is not the main mechanic. | Using accordion for a required linear flow. |
| Confirmation to switch live, delete, reset, or proceed | `Confirmation` pattern, `Modal`, `BottomSheet` on mobile | The user must explicitly approve a consequential action. | Custom overlays/backdrops. |
| Metric panel, summary tile, overview card, activation panel | `Card`, `CardHeader`, `CardBody`, `CardFooter` | The surface has title/body/actions/border/elevation. | `Box` with padding, border, radius, shadow, title, and action. |
| Payment method split, donut visualization, charts | `DonutChart`, `BarChart`, `LineChart`, `AreaChart` | Data visualization is meaningful, even in empty/loading states. | CSS placeholder charts. |
| List, transactions, tabular data, filters | `ListView` pattern, `Table`, `QuickFilter`, `Pagination`, `SearchInput` | Data is structured, filterable, sortable, or paginated. | Custom tables or repeated rows with manual dividers. |
| Empty, no data, unavailable state | `EmptyState`, `Skeleton`, `Spinner` | The page has no data, is loading, or cannot show data. | Plain text placeholders or zeros as empty states. |
| Tooltip nudge, short explanation, guided discovery | `Tooltip`, `SpotlightPopoverTour`, `Popover` | The user needs contextual help or a guided reveal. | Custom absolute-positioned bubbles. |
| Forms, labels, hints, validation | `FormGroup` pattern, `TextInput`, `SelectInput`, `Checkbox`, `Radio`, `Switch`, `FormLabel`, `FormHint`, `FormError` | The user provides input or reviews validation. | Native inputs or manually assembled label/error markup. |
| Tabs, segmented navigation, page sections | `Tabs`, `TabNav` | The user switches peer views or top-level product areas. | Button groups pretending to be tabs. |
| Toast, transient success/error | `Toast` | Feedback is temporary and follows an action. | Alert for short-lived action confirmation. |

## Operating rule

If a `Box` or CSS class owns title, body, border, padding, radius, icon, status color, action, active state, or interaction, stop and map it to a semantic Blade component before continuing.
