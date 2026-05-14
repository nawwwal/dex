# Blade Interaction Quality

Use this file when a prompt sounds like `make it feel better`, `add a transition`, `polish the card`, `the hover feels off`, `numbers jump`, `icons feel misaligned`, `modal/dropdown opens badly`, or `animation feels janky`.

This file is a Blade translation layer for polish and animation guidance. Do not implement the original generic CSS/Framer recipe. Implement the Blade shape below.

## Non-negotiable rule

For every polish or animation ask, do exactly this:

```text
1. Pick the row below that matches the visible UI object.
2. Call the MCP docs listed in the row.
3. Implement the Blade shape listed in the row.
4. If the exact knob is missing, use the Blade fallback listed in the row.
5. Verify the proof listed in the row.
```

Do not invent props. Do not add Framer Motion unless MCP explicitly documents it for the chosen Blade component or pattern. Do not add local CSS transitions, keyframes, timers, `transition: all`, `will-change`, hover media queries, or CSS selectors against Blade internals.

## Deterministic recipes

| User ask | MCP docs to query | Implement with Blade | If exact craft knob is missing | Proof |
| --- | --- | --- | --- | --- |
| Button press feel, click compress, tactile button | `Button,IconButton,Scale` | Use `Button` or `IconButton` as the control. Use `Scale variant="scale-down"` only around a DOM-capable Blade boundary when the control itself does not already give enough feedback. | Keep Blade's default control feedback. Do not tune custom `scale(0.96)` or add active CSS. | Click/tap does not move layout, control remains focusable, no ref warning. |
| Hover card feels flat | `Card,Elevate,AnimateInteractions,Scale` | Keep `Card` as surface. Prefer `Elevate motionTriggers={['hover','focus']}` coordinated by `AnimateInteractions`. Use `Scale` only for small isolated cards where the fixed preset fits. | Use `Elevate` only. Do not tune scale intensity locally. | Hover and keyboard focus both show feedback; carousel/grid width stays stable. |
| Hover reveals child actions | `AnimateInteractions,Fade,Move,Card,Button,IconButton` | Wrap parent with `AnimateInteractions motionTriggers={['hover','focus']}`. Children use `Fade` or `Move` with `motionTriggers={['on-animate-interactions']}`. Actions are `Button`/`IconButton`. | Keep actions always visible or use only `Fade`. Do not write `.parent:hover .child`. | Child reveal works on focus as well as hover; hidden actions are not tabbable unexpectedly. |
| Entering content, loading-to-content reveal | `Fade,Move,Skeleton,Spinner,EmptyState` | Use `Skeleton`/`Spinner` for loading state, `EmptyState` for no data, and `Fade` or `Move` for the content reveal. | Use instant replacement after Blade loading state. Do not add opacity CSS. | Loading, empty, and loaded states are distinct and screen does not jump. |
| Repeated items should enter in order | `Stagger,Fade,Move,ListView,Table,Card` | Use `Stagger` around repeated `Fade`/`Move` children only when sequence teaches order. For data tables/lists, prefer `ListView`/`Table` without decorative entrance. | Skip stagger. Do not create delay ladders. | Sequence does not slow first usable interaction. |
| Page, route, step, or side-by-side transition | `CreationView,DetailedView,ListView,Settings,Fade,Move,Slide,Morph` | Use the Blade pattern if the page shape matches. Use `Fade`/`Move` for content entry, `Slide` for edge-sourced surfaces, `Morph` for one same object across states. | Use instant route/content change. Do not add route-level Framer Motion or CSS page slides. | Source/destination meaning is clear; focus lands on the new view. |
| Modal, drawer, panel, bottom sheet opens badly | `Modal,Drawer,BottomSheet,Slide,Fade` | Use `Modal`, `Drawer`, or `BottomSheet` as owner. Let Blade own backdrop, focus trap, escape, outside click, and surface motion. | Choose the closest Blade overlay. Do not wrap the overlay with custom motion. | Open/close, escape, focus return, and scroll lock work. |
| Dropdown/menu opens badly | `Menu,Dropdown,Popover,Tooltip,ActionList` | Use `Menu` for action/account menus, `Dropdown` for selection/input dropdowns, `Popover` for rich contextual content, `Tooltip` for short non-interactive help. | Change component choice. Do not recreate floating positioning or origin motion. | Keyboard open/close, outside click, and placement work. |
| Icon swap, icon feels off, clickable icon polish | `Button,IconButton,Link,AvailableIcons,Fade,Scale` | If clickable, use `IconButton`, `Button icon`, or `Link icon`. If visual-only swap is needed, keep the control owner and use Blade icon props or a Blade `Fade`/`Scale` child only if MCP supports the composition. | Swap the Blade icon instantly. Do not add blur/scale icon choreography. | Icon has accessible label when icon-only; hit target and focus ring are Blade-owned. |
| Notification dot, unread count, status pill | `Counter,Badge,Indicator,IconButton,Tooltip,Popover,Fade,Scale` | Use `Counter value max color emphasis size` for counts, `Badge` for text metadata, `Indicator accessibilityLabel color emphasis size` for status dots. Anchor near a Blade control with `Box` layout only. | Use static `Counter`/`Badge`/`Indicator`. Do not animate the dot manually. | Screen reader label exists for dot-only state; trigger remains Blade control. |
| Number jumps, KPI amount feels unstable | `Amount,Counter,Text,Heading,Table,ListView` | Use `Amount value currency suffix type size weight` for money, `Counter` for compact counts, `Text`/`Heading` for labels. Prefer stable Blade formatting over animated digits. | Keep update instant. Do not build digit pop-in animation. | Value does not cause row/card layout shift; currency/affix formatting is correct. |
| Text swap, label state change | `Text,Heading,Fade,Move,Badge,Alert,Toast` | If the state is feedback, use `Badge`, `Alert`, or `Toast`. If it is content, use `Text`/`Heading`; use `Fade`/`Move` only for meaningful state transition. | Replace instantly. Do not build text-swap CSS. | State is readable immediately and does not obscure previous/next content. |
| Surface feels boxy, border/radius/shadow off | `Card,Box,Elevate,Modal,Popover,Alert` | Use semantic surface first: `Card`, `Modal`, `Popover`, `Alert`, overlay, or pattern. Use `Box` for layout inside/around the owner. Use Blade radius/elevation tokens. | Pick a simpler Blade surface. Do not write custom border radius or box shadow. | Primary surface is not a `Box` pretending to be a component. |
| Image edge feels dirty or image needs depth | `Card,Box,Preview,LightBox,Elevate` | Put image inside the relevant Blade surface, use Blade radius/overflow/elevation, or `Preview`/`LightBox` when preview semantics apply. | Leave the image plain inside Blade layout. Do not add local image outline CSS. | Image clipping matches surface radius and does not fight theme. |
| Hit area too small | `Button,IconButton,Link,Tooltip,Popover` | Promote the target to `Button`, `IconButton`, or `Link`. For non-interactive trigger icons, use `TooltipInteractiveWrapper` or `PopoverInteractiveWrapper` when MCP docs require it. | Increase Blade control size or spacing. Do not add invisible pseudo-element hit areas. | Target is keyboard reachable and adjacent hit areas do not overlap. |
| Typography wrapping feels bad | `Text,Heading,Display,Box` | Use the right Blade typography component and size. Fix layout width, copy length, or hierarchy with Blade props. | Adjust copy/layout. Do not add local `text-wrap` or font-size hacks. | Heading/body text fits at desktop and mobile widths. |
| Frequent dashboard interaction feels over-animated | `Button,IconButton,Table,ListView,Elevate,Fade` | Remove decorative motion. Use Blade control state, selected state, feedback color, `Elevate`, or instant update. | Skip motion. Do not add “delight” animation to high-frequency work. | Task can be repeated quickly without waiting for animation. |

## Blade snippets

Use snippets as shape, not as a substitute for MCP. Query MCP first in the target app root.

### Parent hover/focus reveals child actions

```tsx
<AnimateInteractions motionTriggers={['hover', 'focus']}>
  <Card>
    <CardBody>
      <Box display="flex" flexDirection="column" gap="spacing.4">
        <Text>...</Text>
        <Fade motionTriggers={['on-animate-interactions']}>
          <Box display="flex" justifyContent="flex-end" gap="spacing.3">
            <Button variant="secondary" size="small">Details</Button>
            <Button size="small">Pay</Button>
          </Box>
        </Fade>
      </Box>
    </CardBody>
  </Card>
</AnimateInteractions>
```

### Stable money and counts

```tsx
<Box display="flex" alignItems="center" gap="spacing.3">
  <Amount value={12345.67} currency="INR" type="heading" size="large" suffix="humanize" />
  <Counter value={8} max={99} color="primary" emphasis="subtle" size="medium" />
</Box>
```

### Status dot or badge

```tsx
<Box display="flex" alignItems="center" gap="spacing.2">
  <Indicator accessibilityLabel="Payouts enabled" color="positive" size="medium" />
  <Badge color="positive" emphasis="subtle" size="small">Enabled</Badge>
</Box>
```

### Icon-only action

```tsx
<IconButton
  icon={RefreshIcon}
  accessibilityLabel="Refresh settlements"
  size="medium"
  onClick={handleRefresh}
/>
```

## Limitation log

If the requested craft detail is impossible in Blade, write this in your work notes and final summary:

```text
Blade docs checked: <exact MCP topics/components>
Requested detail: <exact scale/duration/easing/blur/layout animation/etc.>
Blade limitation: <prop or composition not exposed>
Blade-native fallback used: <closest Blade primitive/pattern/token or skipped effect>
Not used: custom CSS, undocumented Framer wrappers, timers, keyframes, Blade internals styling
Runtime proof: <browser observation or blocker>
```

This log is required for missing motion intensity, duration, easing, blur, digit animation, card resize tweening, icon choreography, or overlay origin animation.
