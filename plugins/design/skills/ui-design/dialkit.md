# DialKit Integration

Live-tuning panel for React prototypes and animations. Renders sliders for numeric design and animation values with localStorage persistence.

## Setup

```tsx
import { DialKitPanel } from 'dialkit';
```

## Standard Controls

### For Prototypes (spacing, visual values)
```tsx
<DialKitPanel
  storageKey="ui-design-[feature]-tuning"
  controls={[
    { label: 'Gap', key: 'gap', min: 4, max: 64, step: 4, default: 16 },
    { label: 'Padding', key: 'padding', min: 8, max: 48, step: 4, default: 16 },
    { label: 'Border Radius', key: 'radius', min: 0, max: 24, step: 2, default: 8 },
  ]}
/>
```

### For Animations (motion parameters)
```tsx
<DialKitPanel
  storageKey="ui-design-[feature]-motion"
  controls={[
    { label: 'Stiffness', key: 'stiffness', min: 100, max: 600, step: 10, default: 300 },
    { label: 'Damping', key: 'damping', min: 15, max: 40, step: 1, default: 30 },
    { label: 'Delay (ms)', key: 'delay', min: 0, max: 500, step: 25, default: 0 },
    { label: 'Duration (ms)', key: 'duration', min: 100, max: 600, step: 25, default: 300 },
  ]}
/>
```

## localStorage Persistence

DialKit persists slider values to `localStorage` under `storageKey`. Use a descriptive key per feature: `ui-design-payment-card-tuning`, `ui-design-onboarding-motion`.
