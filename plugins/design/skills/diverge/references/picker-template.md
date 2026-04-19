# Diverge Picker Template

Vite + React app template for the divergence prototype. Renders a concept picker with per-concept prototype scenes and DialKit tuning controls.

## Vite Scaffolding

Create the project directory and files in this order:

### 1. package.json
```json
{
  "name": "diverge-prototype",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^6.0.0"
  }
}
```

### 2. vite.config.js
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: { port: 5199, open: false }
})
```

### 3. index.html (at project root)
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Diverge Prototype</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

### 4. src/main.jsx
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

### 5. src/styles.css
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-font-smoothing: antialiased; }
body {
  font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
  background: #0a0a1a; color: #e2e8f0;
  min-height: 100vh;
}
input[type="range"] { width: 100%; accent-color: #8b5cf6; }
button { font-family: inherit; }
```

### 6. File structure
```
diverge-[problem-slug]/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── main.jsx
    ├── App.jsx           ← DivergePicker root (below)
    ├── styles.css
    ├── concepts/
    │   ├── index.js      ← re-exports all concepts as array
    │   ├── concept-1.jsx
    │   ├── concept-2.jsx
    │   └── ...
    └── components/
        ├── ConceptNav.jsx
        ├── ConceptMeta.jsx
        └── DialKitPanel.jsx
```

After writing all files: `cd diverge-[slug] && npm install && npm run dev`

## Architecture

```
App.jsx (DivergePicker root)
├── ConceptNav          — segmented control / tabs to switch concepts
├── ConceptScene        — renders the prototype scene for the active concept
├── ConceptDialKit      — per-concept tuning controls (unique to each concept's mechanic)
└── ConceptMeta         — name, premise, mechanic, tradeoff (collapsible)
```

## Concept File Format

Each file in `src/concepts/` exports a single object:

```jsx
// src/concepts/ghost-agent.jsx
const GhostAgentScene = ({ values }) => {
  // Prototype scene that responds to DialKit values
  return <div>...</div>;
};

const concept = {
  id: "ghost-agent",
  name: "Ghost Agent",
  premise: "The best interface is one you never see.",
  mechanic: "Background agent that acts silently, surfaces only on anomalies.",
  sacrifices: "User has no visibility into what's happening. Trust required.",
  axes: ["agency:agent-driven", "surface:off-screen", "density:minimal"],
  controls: [
    { label: "Autonomy Level", key: "autonomy", min: 0, max: 100, step: 5, default: 80, unit: "%" },
    { label: "Surface Threshold", key: "threshold", min: 1, max: 10, step: 1, default: 7, unit: "/10" },
    { label: "Explanation Depth", key: "explain", min: 0, max: 5, step: 1, default: 2, unit: "levels" },
  ],
  Scene: GhostAgentScene,
};

export default concept;
```

```jsx
// src/concepts/index.js
import ghostAgent from './ghost-agent';
import arcade from './arcade';
// ...
export default [ghostAgent, arcade, /* ... */];
```

## Component Templates (adapt, do not copy verbatim)

```jsx
// src/App.jsx
import { useState, useCallback, useMemo } from "react";
import CONCEPTS from "./concepts";
import ConceptNav from "./components/ConceptNav";
import ConceptMeta from "./components/ConceptMeta";
import DialKitPanel from "./components/DialKitPanel";

// ═══════════════════════════════════════════════════════
// ROOT COMPONENT
// ═══════════════════════════════════════════════════════

export default function DivergePicker() {
  const [activeId, setActiveId] = useState(CONCEPTS[0].id);
  const [metaOpen, setMetaOpen] = useState(true);

  // Per-concept dial values — keyed by concept id
  const [allValues, setAllValues] = useState(() => {
    const init = {};
    CONCEPTS.forEach((c) => {
      init[c.id] = {};
      c.controls.forEach((ctrl) => { init[c.id][ctrl.key] = ctrl.default; });
    });
    return init;
  });

  const activeConcept = useMemo(
    () => CONCEPTS.find((c) => c.id === activeId),
    [activeId]
  );

  const handleDialChange = useCallback((key, value) => {
    setAllValues((prev) => ({
      ...prev,
      [activeId]: { ...prev[activeId], [key]: value },
    }));
  }, [activeId]);

  const ActiveScene = activeConcept.Scene;

  return (
    <div style={{
      minHeight: "100vh", background: "#0a0a1a", color: "#e2e8f0",
      fontFamily: "system-ui, -apple-system, sans-serif",
      display: "flex", flexDirection: "column",
    }}>
      {/* Header */}
      <div style={{ padding: "20px 24px 12px" }}>
        <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase",
          letterSpacing: "0.12em", color: "#8b5cf6", marginBottom: 4 }}>
          DIVERGE
        </div>
        <div style={{ fontSize: 20, fontWeight: 700 }}>
          {/* Replace with problem statement */}
          Problem Statement Here
        </div>
      </div>

      {/* Concept Picker */}
      <div style={{ padding: "0 16px 12px" }}>
        <ConceptNav concepts={CONCEPTS} activeId={activeId} onSelect={setActiveId} />
      </div>

      {/* Concept Meta */}
      <div style={{ padding: "0 16px 12px" }}>
        <ConceptMeta
          concept={activeConcept}
          isOpen={metaOpen}
          onToggle={() => setMetaOpen(!metaOpen)}
        />
      </div>

      {/* Prototype Scene */}
      <div style={{
        flex: 1, margin: "0 16px", background: "#12122a",
        borderRadius: 12, border: "1px solid #1e1e3f",
        minHeight: 300, overflow: "auto",
      }}>
        <ActiveScene values={allValues[activeId]} />
      </div>

      {/* DialKit Controls */}
      <div style={{ padding: 16 }}>
        <DialKitPanel
          controls={activeConcept.controls}
          values={allValues[activeId]}
          onChange={handleDialChange}
        />
      </div>
    </div>
  );
}
```

## Component Files

### src/components/DialKitPanel.jsx
```jsx
export default function DialKitPanel({ controls, values, onChange }) {
  return (
    <div style={{
      display: "flex", flexDirection: "column", gap: 12,
      padding: 16, background: "#1a1a2e", borderRadius: 12,
    }}>
      <div style={{ fontSize: 11, fontWeight: 600, textTransform: "uppercase",
        letterSpacing: "0.08em", color: "#7f8c9b", marginBottom: 4 }}>
        Tuning Controls
      </div>
      {controls.map((ctrl) => (
        <div key={ctrl.key} style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, color: "#c4cdd5" }}>
            <span>{ctrl.label}</span>
            <span style={{ fontVariantNumeric: "tabular-nums", color: "#8b5cf6" }}>
              {values[ctrl.key]}{ctrl.unit || ""}
            </span>
          </div>
          <input
            type="range"
            min={ctrl.min} max={ctrl.max} step={ctrl.step}
            value={values[ctrl.key]}
            onChange={(e) => onChange(ctrl.key, Number(e.target.value))}
          />
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, color: "#4a5568" }}>
            <span>{ctrl.min}{ctrl.unit || ""}</span>
            <span>{ctrl.max}{ctrl.unit || ""}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
```

### src/components/ConceptNav.jsx
```jsx
export default function ConceptNav({ concepts, activeId, onSelect }) {
  return (
    <div style={{
      display: "flex", gap: 2, padding: 3, background: "#0f0f23",
      borderRadius: 10, overflow: "hidden",
    }}>
      {concepts.map((c) => (
        <button
          key={c.id}
          onClick={() => onSelect(c.id)}
          style={{
            flex: 1, padding: "10px 8px", border: "none", cursor: "pointer",
            borderRadius: 8, fontSize: 12, fontWeight: 600,
            transition: "all 0.2s ease",
            background: activeId === c.id ? "#8b5cf6" : "transparent",
            color: activeId === c.id ? "#fff" : "#7f8c9b",
          }}
        >
          {c.name}
        </button>
      ))}
    </div>
  );
}
```

### src/components/ConceptMeta.jsx
```jsx
export default function ConceptMeta({ concept, isOpen, onToggle }) {
  return (
    <div style={{
      background: "#12122a", borderRadius: 10, overflow: "hidden",
      border: "1px solid #1e1e3f",
    }}>
      <button onClick={onToggle} style={{
        width: "100%", padding: "12px 16px", border: "none", cursor: "pointer",
        background: "transparent", display: "flex", justifyContent: "space-between",
        alignItems: "center", color: "#c4cdd5",
      }}>
        <span style={{ fontSize: 13, fontWeight: 600 }}>{concept.premise}</span>
        <span style={{ fontSize: 18, transform: isOpen ? "rotate(180deg)" : "rotate(0)", transition: "0.2s" }}>▾</span>
      </button>
      {isOpen && (
        <div style={{ padding: "0 16px 16px", fontSize: 12, lineHeight: 1.6, color: "#8892a0" }}>
          <div><strong style={{ color: "#a78bfa" }}>Mechanic:</strong> {concept.mechanic}</div>
          <div><strong style={{ color: "#f87171" }}>Sacrifices:</strong> {concept.sacrifices}</div>
          <div style={{ display: "flex", gap: 4, flexWrap: "wrap", marginTop: 8 }}>
            {concept.axes.map((a) => (
              <span key={a} style={{
                padding: "2px 8px", background: "#1e1e3f", borderRadius: 4, fontSize: 10, color: "#7f8c9b",
              }}>{a}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## DialKit Control Design Guide

Controls must reflect the concept's *mechanism*. Generic spacing/padding controls are banned in the diverge picker. Every slider should change the prototype's *behavior*.

### Control Libraries by Concept Type

**Agent-driven concepts:**
- Autonomy level (0-100%) — how much the agent does without asking
- Intervention frequency (1-20/day) — how often the agent surfaces
- Confidence threshold (0-100%) — minimum confidence before agent acts
- Explanation depth (0-5) — how much the agent explains its reasoning
- Aggressiveness (0-100%) — how proactively the agent suggests

**Game-like concepts:**
- Difficulty (1-10) — challenge level
- Reward frequency (1-20) — how often positive feedback appears
- Time pressure (0-120s) — countdown duration, 0 = none
- Streak sensitivity (1-7 days) — how quickly streaks break
- Progress visibility (0-100%) — how visible progress indicators are

**Ritual / habit concepts:**
- Session length (1-30 min) — ideal session duration
- Reminder cadence (1-48 hrs) — hours between prompts
- Reflection depth (1-5) — how much reflection is asked for
- Flexibility (0-100%) — how forgiving of missed sessions
- Social visibility (0-100%) — how much others see your activity

**Minimal / ambient concepts:**
- Information density (1-10) — how much is shown at once
- Update frequency (1-60 min) — how often display refreshes
- Salience threshold (0-100%) — how important something must be to appear
- Fade delay (1-30s) — how long info persists before fading
- Urgency escalation (1-5) — steps before notification upgrades

**Power tool / cockpit concepts:**
- Information density (1-10) — data per screen
- Shortcut depth (1-5 levels) — keyboard shortcut layers
- Batch size (1-100) — items processed at once
- Undo depth (1-50) — how many actions can be undone
- Customization level (0-100%) — how much the user can reconfigure

**Collaborative / social concepts:**
- Visibility radius (1-100 people) — who sees your actions
- Contribution threshold (0-100%) — minimum effort to participate
- Consensus requirement (1-100%) — agreement needed for group decisions
- Notification granularity (1-5) — detail level of social notifications
- Anonymity level (0-100%) — how identifiable participants are

**Inversion / prevention concepts:**
- Strictness (0-100%) — how aggressively guardrails enforce
- Warning lead time (0-48 hrs) — how far ahead warnings appear
- Override friction (1-10) — how hard it is to override guardrails
- Learning rate (0-100%) — how fast the system adapts to your patterns
- False positive tolerance (0-100%) — sensitivity vs specificity

### Naming Conventions

- Use descriptive human labels: "Autonomy Level" not "param_a"
- Include units where meaningful: "% ", "/day", "min", "items", "levels"
- Default should represent the concept's sweet spot — the value that best demonstrates the concept
- Min/max should represent the meaningful range, not arbitrary bounds

## Output File Naming

`diverge-[problem-slug].jsx`

Example: `diverge-expense-tracking.jsx`, `diverge-onboarding-trust.jsx`

## Scene Implementation Notes

Each concept's Scene component should be a **functional mockup**, not a wireframe. It should:

1. Respond to DialKit values in real-time (the whole point of the picker)
2. Visualize the concept's core mechanic, not just describe it
3. Use placeholder/mock data that makes the concept feel real
4. Be self-contained (no external dependencies beyond React and standard libs)

Scenes can use:
- Inline styles (preferred for portability)
- SVG for simple illustrations
- CSS animations for interaction feel
- Mock data arrays for realistic content

Scenes should NOT:
- Require external APIs
- Use localStorage (use React state via parent)
- Import external component libraries (keep self-contained)
- Be layout-only wireframes with lorem ipsum
