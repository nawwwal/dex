# Audio Feedback — When and Whether to Use Sound

Design decisions about audio in UI. For Web Audio API implementation (AudioContext, oscillators, gain nodes) → `/design motion` (audio)

## Every Sound Needs a Visual Equivalent

Users may have audio disabled, be in a quiet environment, or have hearing impairments. Every sound that carries information must have a visible companion: animation, icon change, toast, badge, or status text.

## Provide a Disable Toggle

Always give users control over audio feedback. A mute icon in app settings or a persistent notification preference is the minimum:

```
Settings → Notifications → Sound effects: [toggle]
```

## Respect prefers-reduced-motion

When `prefers-reduced-motion` is enabled, suppress audio feedback too. Motion-sensitive users frequently have auditory sensitivity as well. Implementation → `motion/audio.md` (prefers-reduced-motion and Audio section).

## Allow Independent Volume Control

Don't tie sound feedback to system volume directly. Provide an in-app volume slider or a simple low/medium/off control.

## When Sound Is Appropriate

Use audio feedback for actions where the user is waiting for confirmation and may not be looking at the screen:

- ✅ Payment confirmed (₹1,500 sent)
- ✅ File upload complete
- ✅ Form submission successful
- ✅ Critical error that requires immediate attention (e.g., API failure during transaction)
- ✅ Timer expired

## When Sound Is NOT Appropriate

- ❌ Typing (every keystroke)
- ❌ Keyboard navigation (Tab, arrow keys)
- ❌ Hover interactions
- ❌ Decorative animations
- ❌ Context menu opening
- ❌ Page navigation or route changes
- ❌ Background data loading

## Sound Informs, Never Punishes

Sounds should feel gentle and supportive — not harsh, alarming, or punitive. Error sounds should be firm but not startling. Success sounds should be satisfying, not celebratory to the point of being disruptive.

## Sound Weight Matches Action Importance

| Action importance | Sound character |
|---|---|
| Low (info, completed background task) | Soft, short (< 200ms) |
| Medium (form submitted, upload complete) | Moderate tone, 200-400ms |
| High (payment processed, critical error) | Distinctive, 300-600ms, unique from other sounds |

## Sound Duration Matches Action Duration

Short interactions → short sounds. A button tap shouldn't trigger a 2-second sound. Reserve longer sounds for deliberate actions (hold-to-confirm, payment processing).

## No Sound on Hover

Hover is high-frequency and involuntary. Sound on hover is one of the most disruptive patterns in UI — never do it.

---

For implementation details: `motion/audio.md`
For prefers-reduced-motion CSS/animation implementation: `motion/performance.md`
