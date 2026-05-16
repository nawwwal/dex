# Motion Handoff

Use this for transition, animation, microinteraction, timeline, scrubber, or motion-spec requests.

Motion handoffs are playgrounds. They must make time inspectable, not just describe animation in prose.

## Motion Contract

Capture each motion segment:

- Trigger: user/system event that starts it.
- Duration and delay.
- Easing curve or spring parameters.
- Animated properties: transform, opacity, layout, color, filter, height, scroll, or custom value.
- Start, midpoint, and end values.
- Interruption behavior: cancel, reverse, finish, queue, or snap.
- State relationship: what UI state changed and why.
- Reduced-motion alternative.

## Output By Medium

- Code: include a timeline scrubber, play/pause, speed control, keyframe/state markers, reduced-motion alternative, and exportable motion spec. Show current time, active segment, property values, and rendered frame.
- React app: use the app's real motion library when present.
- HTML: use CSS or Web Animations only when faithful to the source.
- Paper/Figma: show keyframes on a time ruler with annotated property deltas. These outputs are static unless the target tool provides a real interaction surface.

## Quality Gates

- Motion explains causality, feedback, continuity, or attention shift.
- Timing values are inspectable.
- Play, pause, scrub, step, and speed controls work when the output medium supports interaction.
- Keyframes and state markers are visible on the timeline.
- Reduced-motion behavior is specified.
- The export includes a motion spec with trigger, timing, easing/spring, properties, interruption behavior, and reduced-motion behavior.
- The artifact shows the whole time frame, not just before/after screenshots.
