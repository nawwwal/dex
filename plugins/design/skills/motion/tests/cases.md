# Skill Tests: motion

## Category: Capability Uplift (monitor for model obsolescence)

## True Positives
1. "how should I think about animation in interfaces?" → principles.md, Emil Kowalski framework
2. "what's the framer motion API for AnimatePresence?" → framer.md, correct import + example
3. "critique this animation: [code]" → craft.md, Josh Puckett 3-pillar evaluation
4. "add entrance animation to this card" → chains principles → framer → craft (DialKit)
5. "storyboard an animation sequence" → craft.md, Storyboard DSL output
6. "how do I make a button feel responsive?" → components.md, scale(0.97) on :active pattern
7. "my popover is scaling from the wrong place" → components.md, popover origin-aware scaling
8. "implement swipe to dismiss for a toast" → gestures.md, velocity-based dismissal
9. "my Framer Motion animation is dropping frames on page load" → performance.md, hardware accel caveat
10. "review this animation code: transition: all 300ms" → review.md, Before/After/Why table output

## True Negatives
1. "how does motion planning work?" → Robotics/AI, not UI animation
2. "animate this SVG path" → General coding, may use motion but not necessarily /motion skill
3. "what motion sickness does VR cause?" → Medical topic

## Edge Cases
1. "motion principles for someone new to animation" → principles.md
2. "is this animation too slow?" → craft.md critique
3. "framer motion v11 breaking change" → framer.md (check if current with package rename)

11. "how do I animate an SVG hamburger icon to an X?" → components.md, morphing icons section
12. "how do I add a confirmation sound for a payment?" → audio.md, sound synthesis (then audio-feedback.md for behavioral guidance)
13. "my accordion doesn't know its own height, how do I animate it?" → components.md, container height animation section

## Retirement Monitoring
Capability uplift skill. If the model knows motion/react API, Emil Kowalski principles + component patterns, gesture interactions, performance rules, morphing icons, and sound synthesis without this skill, consider retiring.
