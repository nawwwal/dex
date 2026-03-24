# Gesture & Drag Interactions

## Momentum-Based Dismissal

Don't require dragging past a threshold. Calculate velocity: `Math.abs(dragDistance) / elapsedTime`. If velocity exceeds ~0.11, dismiss regardless of distance. A quick flick should be enough.

```js
const timeTaken = new Date().getTime() - dragStartTime.current.getTime(); // ms
const velocity = Math.abs(swipeAmount) / timeTaken; // px/ms — threshold 0.11 = ~110px/s

if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) {
  dismiss();
}
```

## Damping at Boundaries

When a user drags past the natural boundary (e.g., dragging a drawer up when already at top), apply damping. The more they drag, the less the element moves. Things in real life don't suddenly stop; they slow down first.

## Pointer Capture for Drag

Once dragging starts, set the element to capture all pointer events. This ensures dragging continues even if the pointer leaves the element bounds.

```js
element.setPointerCapture(event.pointerId);
```

## Multi-Touch Guard

Ignore additional touch points after the initial drag begins. Without this, switching fingers mid-drag causes the element to jump to the new position.

```js
function onPress(event) {
  if (isDragging) return;
  // Start drag...
}
```

## Friction Instead of Hard Stops

Instead of preventing upward drag entirely, allow it with increasing friction. It feels more natural than hitting an invisible wall.

```js
// Apply damping: resistance increases as user drags further past boundary
const overDrag = Math.max(0, currentY - maxY);
const dampedY = maxY + (overDrag * 0.3); // 30% of input = 70% resistance
element.style.transform = `translateY(${dampedY}px)`;
```

## Asymmetric Enter/Exit Timing

Pressing should be slow when it needs to be deliberate (hold-to-delete: 2s linear), but release should always be snappy (200ms ease-out). This pattern applies broadly: slow where the user is deciding, fast where the system is responding.

```css
/* Release: fast */
.overlay {
  transition: clip-path 200ms ease-out;
}

/* Press: slow and deliberate */
.button:active .overlay {
  transition: clip-path 2s linear;
}
```
