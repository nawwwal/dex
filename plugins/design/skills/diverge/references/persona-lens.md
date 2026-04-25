# Persona & Context Lens Library

Select **1 extreme user** and optionally **1 context** per diverge session. Apply after selecting axes and provocation techniques. Each lens must produce at least 1 concept that would not have existed without the lens.

**Application rule:** Don't just imagine the existing concept "for this user." Ask: **"What fundamentally different MECHANISM would serve this user?"** If the mechanism doesn't change, the lens didn't work. Try harder.

---

## Extreme users

For the user's problem, consider what the solution looks like for:

| Persona | Key question | Design implication |
|---------|-------------|--------------------|
| Power user (50x/day) | What if speed-to-action was the ONLY metric? | Keyboard-driven, batch operations, zero confirmation dialogs, muscle memory |
| Once-ever user | What if the user will never learn the interface? | Self-evident, no training, progressive disclosure eliminated, just do it for them |
| Crisis user | What if the user is panicking and has 10 seconds? | Triage mode, binary choices, big targets, no exploration, one path forward |
| Skeptic / hater | What if the user actively resists this entire category? | Invisible integration, zero commitment, prove value before asking anything |
| Accessibility-first | What if the user cannot see the screen? | Voice, haptic, sonification, spatial audio, screen-reader-native architecture |
| Low-bandwidth / shared device | What if connectivity is 2G and the device is shared? | Offline-first, SMS-compatible, tiny payloads, session-less, privacy-aware |
| Expert who finds existing tools insulting | What if the user knows more than the tool? | Exposes raw data, scriptable, no guardrails, respects expertise, gets out of the way |
| Child (10 years old) | What if usable with zero training? | Direct manipulation, immediate feedback, no text-heavy UI, forgiving, explorable |

Select **1 extreme user** (or 2 if the problem is broad enough). For each, redesign the core interaction from scratch.

---

## Different time budgets

How does the solution change when the time budget is radically different?

| Time budget | Design implication |
|-------------|-------------------|
| 2 seconds | Must be glanceable or pre-decided. No interaction, just information or confirmation. |
| 30 seconds | One action, one confirmation. Everything non-essential is hidden or inferred. |
| 5 minutes | Focused session with clear beginning and end. Optimized for a single task completion. |
| 30 minutes | Deep work mode. Distraction-proof. Rich controls. Rewards sustained attention. |
| Used once ever | Entire value must be delivered in one session. No onboarding investment. Disposable. |
| Used daily for 10 years | Must never become annoying. Must evolve with the user. Invisible when not needed. |

Select **1-2 time budgets** that differ from the problem's assumed usage pattern and design for them.

---

## Different contexts

Where is the user when they encounter this problem?

| Context | Constraint it introduces |
|---------|------------------------|
| Walking / on the move | One-handed, glanceable, no precision taps, audio OK if brief |
| In a meeting (covert use) | Silent, minimal visual footprint, quick-dismiss, no attention-grabbing animations |
| Driving | Voice-only, zero visual attention, must be stateless per utterance, safety-critical |
| Cooking / hands dirty | Voice or very large touch targets, no swiping, tolerant of messy input |
| Late at night, exhausted | Minimum cognitive load, maximum forgiveness, dark mode, calming, no complex decisions |
| In public, visible screen | Privacy-sensitive, no embarrassing content, discreet, professional appearance |
| Commuting on public transit | Spotty connectivity, one-handed, frequent interruptions, small screen likely |
| At a desk with dual monitors | Full keyboard + mouse, deep focus possible, high information density acceptable |

Select **1 context** that contrasts with the problem's default context assumption. Design for the constraint it introduces.

---

## Combining lenses

The strongest concepts often come from combining an extreme user with a context:

- **Crisis user + Walking** = "What if someone needs to resolve this urgent problem while running between meetings?"
- **Expert + Late at night** = "What if a power user needs to handle this when they're too tired for complex interfaces?"
- **Child + In public** = "What if the simplest possible interaction needs to work without drawing attention?"
- **Once-ever user + Driving** = "What if someone encounters this problem for the first time while driving?"

Pick one combination if it produces a more specific, interesting constraint than either lens alone.
