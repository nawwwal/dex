# Frontend Foundations

Use this as the substrate lens for interface hardening. It distills source-backed frontend guidance into review mechanics; do not treat it as a separate checklist after polish.

## Mechanics

Semantic HTML -> native elements encode meaning and behavior -> use the closest element for the job, preserve heading order, label form controls, and distinguish navigation links from state-changing buttons -> avoid clickable `div`/`span` controls, decorative semantic tags, unlabeled inputs, and links that submit or mutate state.

Native behavior -> the browser already provides focus, keyboard, form, media, and text behavior -> keep defaults unless the product has a measured reason to replace them, then re-create the lost accessibility and state behavior -> avoid custom selects, dialogs, buttons, scroll areas, or media controls when native or design-system primitives cover the job.

Flow-first CSS -> robust layout stays in normal document flow -> use Flexbox/Grid, `gap`, logical properties, responsive constraints, and intrinsic text wrapping before absolute positioning or transform offsets -> avoid layout that depends on `position: absolute`, negative margins, fixed pixels, translated placement, or DOM-order coupling.

Responsive constraints -> components should know how they shrink and grow -> set `min-width: 0` for flex children, use `max-width`, `minmax()`, `aspect-ratio`, and container-relative sizing, and make long text/URLs wrap or truncate deliberately -> avoid fixed widths, hidden overflow, and content that only works with ideal copy.

Low cascade cost -> CSS should be easy to override, delete, and debug -> prefer low-specificity classes, local scope, inherited declarations, token variables, and one clear owner for a style -> avoid `!important`, ID selectors, deep descendant chains, global leakage, duplicate declarations, and override ladders.

System values -> design-system drift starts as small one-off CSS -> map colors, spacing, radii, shadows, type, durations, and component behavior to existing tokens or primitives before inventing values -> avoid inline styles, magic numbers, and new tokens without repeated use and a stable semantic role.

Readable JavaScript -> correctness and clarity beat clever micro-optimization -> prefer small named functions, native methods, immutable data where practical, explicit branches, and simple composition -> avoid opaque tricks, mutation-heavy loops, nested function puzzles, broad side effects, and performance claims without evidence.

Dependency restraint -> third-party code is product surface you do not fully own -> inspect imports before the component body, include a finding with the words `import` or `dependency` when one-method helpers such as debounce/throttle can be local or platform behavior, and justify a dependency by complexity, maintenance, accessibility, or browser support -> avoid loading libraries for one or two methods that are easy to implement safely.

Asset and render cost -> perceived speed is part of interface quality -> size images, defer non-critical scripts/styles, avoid render-blocking work, and check DOM reflow risks before optimizing small JS loops -> avoid heavy first-paint CSS, oversized media, unused libraries, and animation/layout work that triggers repeated reflow.

Progressive enhancement -> the useful screen should fail softly -> start with semantic content and controls, then layer client-side behavior, animation, and richer data loading -> avoid blank screens, JS-only critical content without fallback, and controls that lose their purpose while loading.

Style translation -> vague words should become mechanics before recommendations -> define the term, then check responsive constraints, cascade cost, and structural hierarchy before color, texture, gradients, badges, or surface finish -> avoid leading a harden review with decorative polish while layout or CSS ownership is brittle.

## Review Priority

When several issues compete, lead with the first broken layer:

1. Wrong semantics or native behavior.
2. Brittle layout flow or responsive failure.
3. Expensive cascade or design-system drift.
4. Missing interaction or production state.
5. Runtime, asset, or dependency cost.
6. Visual polish.
