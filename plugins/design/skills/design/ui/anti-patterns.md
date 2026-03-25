# Anti-Patterns — Detection Audit

Scan for AI slop, design debt, and Blade violations. Output severity-ranked file:line findings.

## Mode Detection

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

## Anti-pattern library (all modes)

### Critical — fix before shipping

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Glassmorphism | `backdrop-filter: blur`, semi-transparent backgrounds used as primary surfaces | Use solid surface colors |
| Gradient text | `background-clip: text`, `webkit-text-fill-color: transparent` | Use solid color text |
| Bounce/elastic easing | `cubic-bezier` with values > 1, `easeInBounce`, `spring-bounce` | Use ease-out for entrances/exits. Full easing guidance → /design motion (principles) |
| No empty state | Component renders nothing when data is empty | Add designed empty state |
| Autoplaying media with sound | `autoplay` without `muted` | Add `muted` or remove autoplay |

### High — should fix

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Cyan/purple gradient | `#00BFFF`, `#8B00FF`, similar hex values in gradients | Remove or replace with brand color |
| AI-slop loading copy | "herding pixels", "teaching robots to dance", "magic is happening" | Replace with clear, specific copy |
| Cards on cards | `Card` > `Card`, `elevation` > `elevation` nested styling | Flatten to 1 level |
| Generic placeholder copy | "Lorem ipsum", "Sample text", "Test data" in production paths | Replace with real content |
| Multiple accent colors | 3+ distinct hex values used as accent/interactive colors | Reduce to 1–2 |
| Equal visual weight | Every element same size/weight, no hierarchy | Establish clear scale |

### Medium — design debt

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Inter overuse | Only Inter font, no variation, used at every weight 100-900 | Consider pairing or using weight intentionally |
| Monotonous card grid | All cards same size, equal gap, no hierarchy | Vary size or add feature card |
| Everything centered | `text-align: center` on everything, `align-items: center` everywhere | Use leading alignment for scannable layouts |
| Fixed width on containers | `width: 800px` instead of `max-width` | Replace with max-width + 100% |
| Gray text on colored background | Low contrast secondary text on brand surfaces | Check contrast, adjust color |

---

## Blade-specific anti-patterns (Blade mode only)

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Hardcoded hex colors | Any `#` color value not in Blade token | Replace with Blade semantic color token |
| Hardcoded px spacing | `padding: 16px`, `margin: 8px` etc. | Replace with Blade spacing props |
| Raw `<div>` for text | `<div>` or `<p>` containing body copy | Replace with `<Text>` |
| Raw `<h1>-<h6>` | Heading elements without Blade Heading component | Replace with `<Heading>` |
| Custom `<input>` | Raw `<input type="text">` instead of TextInput | Replace with Blade TextInput/TextArea/etc |
| Wrong Amount formatting | Hardcoded `₹` or manual `toLocaleString` for currency | Use `<Amount>` component |
| Import from wrong path | Wrong: `import { Button } from '@razorpay/blade'` | Fix: change to `from '@razorpay/blade/components'` |

---

## Output

```
## Anti-patterns: {TARGET}

### Critical
- [file:line] — GLASSMORPHISM — backdrop-filter: blur(10px) on Card — Remove or replace with solid surface.action.background.primary.subtle

### High
- [file:line] — AI-SLOP COPY — "Sit tight while we work our magic" — Replace with "Processing your payment..."
- [file:line] — HARDCODED HEX — color: #0066CC — Replace with color="interactive.text.primary.normal" (Blade)

### Medium
- [file:line] — EQUAL WEIGHT — all 5 actions same visual weight, no primary CTA

### Passed
- Typography: uses correct scale, no Inter overuse
- Spacing: consistent token usage (Blade mode)
```
