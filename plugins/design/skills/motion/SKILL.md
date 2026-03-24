---
name: motion
description: "Use when working on animation or motion design — principles (Emil Kowalski), Framer Motion API, DialKit/Storyboard critique, animation code review, component patterns, performance ('jank', 'drop frames', 'GPU'), morphing icons ('SVG path morphing'), sound synthesis ('AudioContext'), or container height animation."
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /motion — Animation Knowledge Router

## Dispatch Logic

### Principles / Philosophy
Triggers: "principles", "how do I think about animation", "animation philosophy",
          "Emil Kowalski", "taste", "beauty is leverage", "unseen details",
          "should this animate", "when to animate", "frequency"
-> Read `$CLAUDE_SKILL_DIR/principles.md` AND `$CLAUDE_SKILL_DIR/components.md`

### Framer Motion API
Triggers: "framer", "framer motion", "motion/react", specific API questions
          (useAnimation, AnimatePresence, useSpring, useTransform, etc.)
-> Read `$CLAUDE_SKILL_DIR/framer.md`

### Animation Code Review (Emil's Before/After/Why format)
Required output: Before/After/Why table per finding.
Triggers: "review this animation", "review this animation code", "animation before/after",
          "what's wrong with this animation", "what's wrong with this motion",
          "fix this animation", "critique this animation code", "animate this right"
Note: Generic "review", "code review", "UI review" are handled by ui-design skill — only animation-scoped phrases trigger this file.
-> Read `$CLAUDE_SKILL_DIR/review.md`

### Critique / DialKit / Storyboard / Sonner / Stagger / Debug
Triggers: "critique", "review this animation quality", "DialKit", "storyboard",
          "tune", "tweak", "timing", "Josh Puckett", "3 pillars",
          "sonner", "stagger", "cascading", "debug animation", "slow motion test",
          "frame by frame", "review my work"
-> Read `$CLAUDE_SKILL_DIR/craft.md`

### Component Patterns / CSS Techniques
Triggers: "button press", "button feel", "button scale", "scale(0)", "popover",
          "popover animation", "origin-aware", "tooltip delay", "tooltip timing",
          "radix", "clip-path", "hold to delete", "image reveal", "tabs animation",
          "hover state", "active state", "blur transition", "@starting-style",
          "CSS transition", "CSS keyframe", "CSS transform", "translateY percent",
          "3D transform", "preserve-3d"
-> Read `$CLAUDE_SKILL_DIR/components.md`

### Gesture / Drag Interactions
Triggers: "drag", "swipe", "swipe to dismiss", "drag dismiss", "gesture", "velocity",
          "drawer", "bottom sheet", "touch", "friction", "pointer capture",
          "multi-touch", "pan", "momentum", "damping"
-> Read `$CLAUDE_SKILL_DIR/gestures.md`

### Performance / Accessibility
Triggers: "performance", "GPU", "hardware acceleration", "jank", "drop frames",
          "layout thrashing", "WAAPI", "prefers-reduced-motion", "reduced motion",
          "accessibility", "main thread", "CSS variable animation", "CSS variable inheritance",
          "framer motion slow", "off main thread", "hover media query"
-> Read `$CLAUDE_SKILL_DIR/performance.md`

### Morphing Icons
Triggers: "SVG path morphing", "hamburger to close", "hamburger menu animation", "3-line icon",
          "icon morph", "nav icon animation", "close icon animation"
-> Read `$CLAUDE_SKILL_DIR/components.md` (morphing section)

### Sound Synthesis (Web Audio API)
Triggers: "audio", "sound", "Web Audio API", "AudioContext", "oscillator",
          "sound synthesis", "click sound", "notification sound", "beep",
          "AudioContext suspended", "exponential ramp", "gain node"
-> Read `$CLAUDE_SKILL_DIR/audio.md`

### Container / Height Animation
Triggers: "animate height", "expand collapse", "accordion animation", "dynamic height",
          "ResizeObserver animation", "auto height", "measuring element", "two-div pattern"
-> Read `$CLAUDE_SKILL_DIR/components.md`

### Full Implementation
Triggers: "implement animation for X", "build animation", "add motion to"
-> Chain: `$CLAUDE_SKILL_DIR/principles.md` [philosophy] -> `$CLAUDE_SKILL_DIR/framer.md` [API] -> `$CLAUDE_SKILL_DIR/components.md` [patterns] (craft.md on explicit critique; gestures/performance/audio on demand)
