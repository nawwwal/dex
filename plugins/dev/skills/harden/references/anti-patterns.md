# Anti-Patterns

Scan for interface debt and AI-slop patterns. Output severity-ranked file or area findings.

## Route Out First

- Razorpay Blade token/component violations: route to `blade`.
- Animation easing/timing problems: route to `web-animation-design`.

## Critical

| Pattern | Detection | Fix |
|---|---|---|
| Glassmorphism as primary surface | `backdrop-filter: blur`, translucent panels carrying core content | Use solid surfaces with clear elevation or borders |
| Gradient text | `background-clip: text`, transparent text fill | Use readable solid text color |
| Bounce or elastic easing | `cubic-bezier` values above 1, bounce springs, novelty motion | Use restrained ease-out or route to motion skill |
| Missing empty state | Component renders nothing when data is empty | Add a designed empty state with next action |
| Autoplay with sound | `autoplay` without `muted` | Mute by default or remove autoplay |

## High

| Pattern | Detection | Fix |
|---|---|---|
| AI-slop loading copy | "magic", "robots", "pixels", vague jokes in operational UI | Replace with specific system status |
| Cards on cards | Nested framed cards/elevation inside framed surfaces | Flatten to one container level |
| Placeholder production copy | "Lorem ipsum", "Sample", "Test data" | Replace with real content or mark as mock-only |
| Too many accents | Three or more competing action/accent colors | Reduce to semantic roles |
| Equal visual weight | Everything same size, color, or emphasis | Establish primary, secondary, and tertiary hierarchy |

## Medium

| Pattern | Detection | Fix |
|---|---|---|
| Everything centered | Center alignment used for dense forms/tables/lists | Use leading alignment for scanning |
| Arbitrary fixed widths | `width: 800px` without responsive constraint | Use `max-width`, `minmax`, or container-relative sizing |
| Low contrast secondary text | Gray text on colored or dark surfaces | Increase contrast or change surface |
| Monotonous card grid | Repeated cards with no hierarchy or grouping | Add grouping, sorting, or priority treatment |

## Output

```text
## Anti-patterns: {target}

### Critical
- [file:line] - [pattern] - [why it breaks] - Fix: [specific change]

### High
- ...

### Medium
- ...
```
