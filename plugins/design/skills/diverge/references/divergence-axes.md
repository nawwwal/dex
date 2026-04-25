# Divergence Axes Library

## Primary Axes

Each axis represents a fundamental dimension along which two concepts can differ. Concepts that share fewer than 3 axes are **not divergent** — they are variations.

### 1. Who drives (user → system)
Who drives the action?

| From | To |
|--------|--------|
| User-driven (manual, explicit) | Agent-driven (automatic, inferred) |

Sub-positions: user initiates → user confirms → system suggests → system acts → system acts silently

### 2. Where it lives (screen → off-screen)
Where does the product live?

| From | To |
|--------|--------|
| Screen-based (dashboard, app, page) | Off-screen (notification, ambient, hardware, voice, environment) |

Sub-positions: full app → widget → notification → ambient display → no screen → physical object

### 3. When it happens (one moment → ongoing)
When does interaction happen?

| From | To |
|--------|--------|
| Single moment (transaction, one-shot) | Ongoing system (continuous, background, longitudinal) |

Sub-positions: one-shot → session → ritual → continuous background → event-driven

### 4. How info is structured (browse → filter)
How is information structured?

| From | To |
|--------|--------|
| Browse/find (explore, discover) | Filter/eliminate (narrow, reduce) |

Sub-positions: open canvas → feed → ranked list → filtered view → single recommendation → zero-UI auto-pick

### 5. How it feels (tool → toy)
What does it feel like to use?

| From | To |
|--------|--------|
| Serious professional tool | Playful mechanic / game / toy |

Sub-positions: Bloomberg terminal → Excel → consumer app → gamified → literal game → toy

### 6. How users express intent (form → invisible)
How does the user express intent?

| From | To |
|--------|--------|
| Explicit workflow (form fill, step-by-step) | Invisible defaults (system infers, user overrides) |

Sub-positions: form → wizard → conversation → direct manipulation → gesture → invisible default

### 7. Who's involved (solo → social)
Who is involved?

| From | To |
|--------|--------|
| Solo use (single user, private) | Collaborative / social (shared, multiplayer, community) |

Sub-positions: solo private → shared state → collaborative → social feed → marketplace → community-governed

### 8. Direction (help do → eliminate need)
Does it help do, or help avoid?

| From | To |
|--------|--------|
| Assistance (help user do the thing) | Inversion (eliminate the need to do the thing) |

Sub-positions: assist → accelerate → automate → delegate → prevent → eliminate the problem entirely

### 9. Density (cockpit → single thing)
How much information per unit of attention?

| From | To |
|--------|--------|
| High density (power user, data-rich) | Minimal (one thing at a time, progressive) |

Sub-positions: cockpit → dashboard → card → single metric → binary signal → no signal (absence = good)

### 10. What system behavior powers it
The mechanism that makes the product work:

- Recommendation
- Ranking
- Batching
- Auto-completion
- Delegation
- Progressive disclosure
- Constraints / guardrails
- Simulation / preview
- Social proof
- Urgency / scarcity
- Pattern matching
- Anomaly detection
- Narration / journaling
- Ritual / habit loop

### 11. Real-world reference
Which non-software domain does it borrow from?

| Domain | Implies |
|--------|---------|
| Muji | Calm, invisible, material-honest |
| Bloomberg Terminal | Dense, keyboard-driven, zero waste |
| Nintendo | Surprise, delight, progressive mastery |
| Duolingo | Streak, habit, micro-progress |
| Luxury concierge | White-glove, anticipatory, invisible labor |
| Cockpit | Mission-critical, instrumented, heads-up |
| Library | Browse, serendipity, quiet focus |
| Emergency room | Triage, severity, rapid action |
| Garden | Tend, grow, patience, seasonal rhythm |
| Air traffic control | Real-time multi-agent coordination, zero tolerance for error, radar/inference |
| Jazz ensemble | Improvisation within structure, listening, riffing on shared themes |
| Greenhouse | Controlled environment, nurturing growth, monitoring conditions, micro-climate |
| Auction house | Revealed preferences, time pressure, competitive bidding, reserve price |
| Triage nurse | Rapid assessment, ruthless prioritization, resource-constrained, severity-based |

### 12. Artificial constraint
What artificial constraint reshapes the design?

- Only one button
- No text (icon/visual only)
- Works offline first
- Designed for repeat daily use without becoming annoying
- Assumes users are impatient and distracted
- Assumes users are anxious and need reassurance
- Must feel premium without looking luxurious
- Works on a watch / in a car / eyes-free

### 13. Tone (tool → identity)
What is the product's emotional register?

| From | To |
|--------|--------|
| Functional / utilitarian (tool, no personality) | Emotionally resonant / identity-forming (users feel something, product reflects who they are) |

Sub-positions: invisible utility → reliable tool → trusted companion → identity expression → emotional mirror → ritual/sacred object

### 14. Adaptation (static → personalized)
Does the product learn and change?

| From | To |
|--------|--------|
| Static (same for everyone, every time) | Deeply personalized (learns, adapts, evolves per user) |

Sub-positions: identical for all → configurable → preference-learning → behavior-predicting → context-aware → fully autonomous adaptation

---

## Prompt Frames

Use these frames to generate specific kinds of divergence. Select 1-2 frames that match the problem space.

### Frame: Orthogonal Directions
```
Generate 10 prototype directions for [problem].
They must be orthogonal, not adjacent.
No two concepts should share the same primary interaction model.
Spread across: automation, direct manipulation, conversational, feed-based, game-like, assistant-led, invisible/background, collaborative, ritualized/habit-forming, extreme minimal.
Concepts that feel like different product species, not alternate screens from one app.
```

### Frame: Kill the Dashboard
```
Solve [problem] without using a dashboard, settings page, or standard list/detail layout.
Start from first principles: what should happen automatically, what can be inferred, what can be deferred, what might not need a screen at all.
7 prototypeable concepts.
```

### Frame: Interface Gradient (zero to full)
```
6 ways to solve [problem], ordered from least interface to most interface.
Start with zero UI → ambient UI → one-tap UI → guided flow → power-user tool → full control surface.
Conceptual range, not finish.
```

### Frame: Industry Transplant
```
Reimagine [problem] as if designed by:
• Muji • Bloomberg Terminal • Nintendo • Duolingo
• a luxury concierge • a cockpit system
Same user goal, radically different product philosophy.
Key interaction mechanic and a rough screen idea for each.
```

### Frame: Inversion
```
Users think they need help doing [task].
5 concepts that instead help them avoid mistakes, reduce choices, delegate effort, or only intervene at the highest-leverage moment.
Inversion, not assistance theater.
```

### Frame: Tradeoff Maximizer
```
8 concepts for [problem].
Each aggressively optimizes one quality at the expense of another:
speed / trust / delight / control / automation / learnability / memorability / differentiation
Make tradeoffs visible. No safe middle-ground ideas.
```

### Frame: Product Behaviors First
```
Don't start with screens. Start with system behavior.
For [problem], 8 different product behaviors, then translate each into the minimum prototype to express it.
The prototype reveals the concept, not decorates it.
```

### Frame: Mechanism-First
```
Concepts built around different mechanisms:
recommendation / ranking / batching / auto-completion / delegation / progressive disclosure / constraints / simulation / social proof / urgency
Each mechanism leads to a distinctly different prototype direction.
```

### Frame: Dangerous Ideas
```
10 high-variance concepts for [problem].
Some should feel slightly wrong, risky, or provocative.
Explicitly exploring bold directions, not only sensible ones.
Label which ones are likely brilliant vs likely terrible, and why.
```

### Frame: Unnatural Constraints
```
6 concepts for [problem], but:
- one works with only one button
- one works with almost no text
- one must feel premium without looking luxurious
- one assumes users are impatient and distracted
- one assumes users are anxious and need reassurance
- one is designed for repeat daily use without becoming annoying
```

### Frame: Extreme Users
```
Redesign [problem] for 4 radically different users:
• a power user who does this 50 times a day (speed is everything)
• a first-timer who will never learn the interface (it must be self-evident)
• a user in a crisis with 10 seconds (triage mode)
• a user who actively hates this product category (prove value before asking anything)
Each user demands a fundamentally different mechanism, not just a different skin.
See persona-lens.md for the full library.
```

### Frame: Emotion Targets
```
Design 6 concepts for [problem], each starting from a target emotion:
• Relief: "the weight is lifted"
• Mastery: "I'm getting better at this"
• Surprise: "I didn't know that was possible"
• Confidence: "I know I'm making the right choice"
• Curiosity: "I want to explore more"
• Calm: "everything is under control"
Design backward: what product makes the user feel this within 30 seconds?
See creative-provocations.md "Start from the emotion" for the full library.
```

### Frame: Eliminate the problem
```
What would make [problem] not exist?
5 concepts that eliminate the problem rather than solve it.
• 2 that remove the cause upstream
• 2 that automate around it so no human is involved
• 1 that reframes it as a symptom of something else entirely
Some may not be software. That's fine.
```

---

## Banned Patterns (detect and replace)

These indicate failure to diverge. If any concept matches, replace it.

| Pattern | Why it's banned |
|---------|----------------|
| Dashboard with cards and charts | Default SaaS grammar. Unless the concept is specifically "cockpit density," ban it. |
| List view + detail pane | The most common layout on earth. Not a concept. |
| Settings page with toggles | Configuration ≠ interaction model. |
| Wizard / stepper flow | This is a pattern, not a concept. Only allowed if the *mechanism within* the stepper is novel. |
| "Clean, modern interface" | Aesthetic, not structural. Not a concept. |
| Tab bar with 4-5 sections | Navigation ≠ concept. |
| Chat interface without novel agent behavior | Putting a chat bubble on it is not innovation. |
| Same concept with light/dark theme | Cosmetic, not structural. |
| AI chatbot that answers questions about X | Putting a chat bubble on it is not innovation. Only allowed if the conversational mechanic is genuinely novel (e.g., negotiation, Socratic method, adversarial). |
| Notification system that alerts when X | A notification is a delivery channel, not a concept. The concept is what happens after the alert. |

## Duplicate detector

Two concepts are duplicates if:
1. They solve the same sub-problem
2. Using the same core mechanic
3. With the same level of user agency
4. Differing only in visual treatment, copy, or layout

**Test:** If you could merge them into one concept by adding a toggle, they were never two concepts.
