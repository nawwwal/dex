# Component Selection

Use this map before querying Blade MCP. It translates product language into Blade vocabulary so agents do not treat Blade as a parts bin. Every component name here is a candidate, not a contract; MCP confirms props, slots, triggers, and examples.

For the general ownership model, read `surface-taxonomy.md`. For fit, polish, and transition judgement, read `interaction-quality.md`. This file is only a candidate map for common high-risk product phrases.

## Blade-only replacement recipes

| Drift signal | Blade route | Do not keep |
| --- | --- | --- |
| Custom banner, strip, notice, warning box | `Alert` | Colored `Box` plus icon/text/actions as the owner. |
| CSS card, tile, metric panel, summary surface | `Card` | Hand-built padding, border, radius, title, and action chrome. |
| Clickable row, icon-only div, fake link | `Button`, `IconButton`, `Link`, `Menu`, `ActionList` | `div`/`span` with `onClick` and manual focus styling. |
| CSS hover reveal or parent-child hover selector | `AnimateInteractions` with `Fade`, `Move`, `Scale`, or `Elevate` | `.parent:hover .child`, duplicated hover state, hover without focus. |
| Framer/CSS transition around Blade UI | Blade motion primitive or documented MCP dependency | Undocumented wrappers, timers, keyframes, transition classes. |
| Custom data table/list/filter row | `ListView`, `Table`, `QuickFilter`, `Pagination`, `SearchInput` | Repeated rows and manual dividers. |
| CSS chart or fake donut/line/bar graphic | Blade chart components | Decorative placeholders for meaningful data. |

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
| Metric panel, summary tile, overview card, activation panel | `Card`, `CardHeader`, `CardBody`, `CardFooter` | The surface has title/body/actions/border/elevation. Use `Box` inside `CardBody` for layout, decorative strips, absolute layers, and custom content that Card slots do not accept. | `Box` with padding, border, radius, shadow, title, and action as the primary surface. Arbitrary JSX directly inside `Card`, `CardHeader`, or `CardFooter`. |
| Carousel of cards, feature rail, horizontally browsed cards | `Carousel`, `CarouselItem`, `Card` | The user moves through related cards horizontally. Set width with `carouselItemWidth`; keep each item as `CarouselItem > Card`; use `visibleItems=\"autofit\"` for multiple cards or `visibleItems={1}` + `snapAlign=\"center\"` for peek. | A single over-wide card that reads like a banner, custom scroll containers, or scaling the carousel item so width changes during hover. |
| Payment method split, donut visualization, charts | `DonutChart`, `BarChart`, `LineChart`, `AreaChart` | Data visualization is meaningful, even in empty/loading states. | CSS placeholder charts. |
| List, transactions, tabular data, filters | `ListView` pattern, `Table`, `QuickFilter`, `Pagination`, `SearchInput` | Data is structured, filterable, sortable, or paginated. | Custom tables or repeated rows with manual dividers. |
| Empty, no data, unavailable state | `EmptyState`, `Skeleton`, `Spinner` | The page has no data, is loading, or cannot show data. | Plain text placeholders or zeros as empty states. |
| Tooltip nudge, short explanation, guided discovery | `Tooltip`, `SpotlightPopoverTour`, `Popover` | The user needs contextual help or a guided reveal. | Custom absolute-positioned bubbles. |
| Forms, labels, hints, validation | `FormGroup` pattern, `InputGroup`, `TextInput`, `SelectInput`, `PasswordInput`, `PhoneNumberInput`, `DatePicker`, `TimePicker`, `Checkbox`, `Radio`, `Switch`, `TextArea` | The user provides input or reviews validation. Let MCP-confirmed input props own labels, help, and errors; do not fetch label/hint/error as standalone component docs unless MCP lists them. | Native inputs or manually assembled label/error markup. |
| Tabs, segmented navigation, page sections | `Tabs` | The user switches peer views or top-level product areas. If MCP pattern examples mention TabNav, fetch `Tabs` component docs for the current public component contract. | Button groups pretending to be tabs. |
| Toast, transient success/error | `Toast` | Feedback is temporary and follows an action. | Alert for short-lived action confirmation. |
| Fade in/out, route surface appearing, loading-to-content reveal | `Fade`, sometimes `Move` | The content should appear without changing spatial meaning. Use `Move` when a slight y-position shift helps establish arrival. | CSS opacity classes, ad hoc `transition: opacity`, wrapping every child in Framer Motion. |
| Drawer-like screen/page shift, full-panel entrance, mobile bottom entry | `Slide`, existing `Drawer`, `Modal`, `BottomSheet` first | The surface enters from an edge or from outside the viewport. Prefer semantic overlay components when the interaction is actually an overlay. | Translating fixed-position divs, CSS keyframes for panels Blade already owns. |
| Hover/focus/tap feedback on cards or clickable blocks | `AnimateInteractions`, `Elevate`, `Scale`, `Move`, `Fade` | A parent interaction should reveal, lift, scale, or move child affordances. Include focus when hover is used. Use `Scale` only when its fixed intensity is acceptable for the element size. | `Card shouldScaleOnHover` as the default. Hover-only CSS, clickable `Box` without focus behavior, styling Blade internals. |
| Sequential reveal of repeated cards, rows, or setup steps | `Stagger` with `Fade` or `Move` children | Sibling items should enter one after another to show order or progressive disclosure. | Manually increasing CSS delays on repeated elements. |
| Shared element or layout continuity between two states | `Morph` | The same conceptual object changes size, position, or component form across state. Use with matching `layoutId` and any MCP-documented dependency such as `AnimatePresence`. | Morphing unrelated objects or using it to hide ordinary conditional rendering. |
| Branded success, loading, or hero animation | `SparkAnimation` pattern, `RazorSense`, `RazorSenseGradient` | The moment benefits from Blade's WebGL brand treatment and assets can be preloaded before mount. | Heavy custom canvas/WebGL work, unpreloaded animated backgrounds, decorative motion in dense dashboard workflows. |

## Operating rule

If a `Box` or CSS class owns title, body, border, padding, radius, icon, status color, action, active state, or interaction, stop and map it to a semantic Blade component before continuing.

## Boundary model

Use this model before reaching for any layout primitive or local wrapper:

| Boundary | Owner | Layout primitives may do | Layout primitives must not do |
| --- | --- | --- | --- |
| Surface | Blade component or pattern that represents the visible unit | Layout inside that semantic component; decorative layers that do not replace the owner; wrappers for dimensions/ref composition. | Replace a semantic surface with border/radius/elevation/padding and hand-built title/action semantics. |
| Layout | `Box` and local layout wrappers | Flex/grid, spacing, positioning, width constraints, overflow, layering. | Become the user-facing component when Blade has a matching semantic primitive. |
| Interaction | Blade controls, navigation, disclosure, overlay, selection, and motion primitives | Arrange controls or wrap a missing parameter locally. | Own click, hover, focus, selection, disclosure, active route, or overlay behavior when Blade has a primitive for it. |
| Data display | Blade table, list, chart, amount, badge, empty/loading components | Compose cells, panels, and chart containers. | Rebuild tables, chart legends, metric semantics, status labels, or loading/empty states manually. |
| Feedback | Blade alert, toast, validation, progress, skeleton, spinner, or empty state | Position feedback in the surrounding layout. | Use colored containers or loose text as the primary feedback pattern. |
| Motion | Blade motion primitive or pattern | Provide stable dimensions and DOM/ref boundaries around Blade motion. | Rebuild Blade motion with CSS classes, timers, Framer wrappers, or custom transforms. |
