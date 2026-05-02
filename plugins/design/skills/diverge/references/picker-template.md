# Diverge React Picker Template

Use this when the user selects a React prototype. The picker compares layered directions and lets users tune design variables that affect product, UX, UI, copy, visual system, emotion, or handoff.

## App sections

- Direction navigation
- Product model panel
- State matrix panel
- Screen anatomy panel
- Copy panel
- Layout panel
- Interaction panel
- Visual system panel
- Emotional/persuasive rationale
- Handoff panel
- Layer controls
- Prototype scene

## Concept object

Each direction exports:

```jsx
const DirectionScene = ({ values }) => {
  return <div>{/* layered prototype scene */}</div>;
};

const direction = {
  id: "agent-risk-board",
  name: "Agent-risk board",
  altitude: "Mixed",
  productBet:
    "Users should manage connector health by fixing agent-risk incidents, not by browsing connector inventory.",
  layersChanged: {
    productMechanics: "Connector-first -> agent-risk-first",
    uxStructure: "Inventory -> triage board",
    interaction: "Inspect -> diagnose and repair",
    informationHierarchy: "Risk and next action above connector details",
    copy: "State labels name impact and recovery",
    layout: "Split pane with queue and repair inspector",
    typography: "Tabular numbers for counts; terse labels",
    color: "Semantic status with non-color backup",
    motion: "State transition only when issue changes severity",
    emotionalDesign: "Relief and control",
    persuasiveBehavior: "Prompt repair only when impact is clear",
    stateHandling: "Expired auth, API down, scope changed, schema mismatch",
  },
  productModel: {
    user: "Operator",
    job: "Know which connector issue threatens which agent and fix the urgent ones.",
    objects: ["Agent", "Connector", "Workflow", "Credential", "Permission", "Issue"],
    currentDecision: "What should I fix now?",
  },
  stateMatrix: [
    {
      state: "Expired auth",
      userMeaning: "A user-owned credential must be renewed.",
      severity: "High when active agents depend on it",
      userAction: "Reconnect",
      systemAction: "Pause affected syncs and show affected agents",
      uiRepresentation: "Repair issue with reconnect CTA",
      copyRequirement: "Name affected agents and data safety",
    },
  ],
  screenAnatomy: {
    topRegion: "Blocked, at risk, degraded, healthy counts",
    primaryRegion: "Affected agents sorted by impact",
    secondaryRegion: "Connector dependency strip",
    detailRegion: "Issue cause, evidence, action path",
    persistentElements: ["Search", "Saved view", "Last checked"],
    primaryCTA: "Reconnect Slack",
    secondaryActions: ["Pause agent", "Assign owner", "Retry", "Ignore"],
    hiddenByDefault: ["Raw logs", "Provider history"],
    appearsAfterInteraction: ["Permission diff", "Schema mapping"],
  },
  copySystem: {
    pageTitle: "Agent risks",
    sectionHeading: "Needs action",
    primaryCTA: "Reconnect Slack",
    emptyState: "No connector issues are affecting agents right now.",
    loadingState: "Checking connector dependencies...",
    errorState: "We could not refresh connector status. Last checked 18 minutes ago.",
    successState: "Slack reconnected. Refund Agent can resume syncing.",
  },
  layoutExecution: {
    topology: "Queue with inspector",
    density: "Power-dense",
    responsiveBehavior: "Queue first, inspector opens as full-screen detail on mobile",
  },
  visualSystem: {
    typography: "Single-family product system with tabular numbers",
    color: "Neutral product palette with semantic status",
    motion: "Minimal severity transitions; reduced-motion equivalent uses text change",
  },
  emotionalPersuasiveRationale: {
    before: "Uncertain what is broken",
    during: "Clear control over urgent issue",
    after: "Relief that affected agents are safe",
    desiredBehavior: "Fix user-actionable issues before browsing inventory",
    ethicalBoundary: "Do not exaggerate risk to force action",
  },
  handoff: {
    stateMachine: ["healthy", "atRisk", "blocked", "recovering", "resolved"],
    events: ["connector_expired", "retry_started", "permission_approved"],
    apiNeeds: ["dependency graph", "last sync", "fixability", "owner"],
    analytics: ["issue_opened", "repair_clicked", "agent_paused"],
    accessibility: ["No color-only state", "Keyboard queue navigation"],
    localization: ["Avoid idioms in recovery copy"],
    qaCases: ["API down disables reconnect", "Scope change requires approval"],
  },
  tradeoff:
    "Less useful as a pure connector directory; stronger for reliability operations.",
  prototypeSlice:
    "One queue with three agents, three connector states, and one repair inspector.",
  controls: [
    { label: "Automation level", key: "automation", type: "range", min: 0, max: 100, step: 5, default: 40, unit: "%" },
    { label: "Confidence threshold", key: "confidence", type: "range", min: 0, max: 100, step: 5, default: 75, unit: "%" },
    { label: "Severity threshold", key: "severity", type: "range", min: 1, max: 10, step: 1, default: 7, unit: "/10" },
    { label: "Grouping mode", key: "grouping", type: "select", options: ["agent", "issue", "owner"], default: "agent" },
    { label: "Copy tone", key: "tone", type: "select", options: ["direct", "calm", "urgent", "expert"], default: "direct" },
    { label: "Layout topology", key: "layout", type: "select", options: ["queue-inspector", "matrix", "timeline"], default: "queue-inspector" },
  ],
  Scene: DirectionScene,
};

export default direction;
```

## Good controls

Product controls:

- Automation level
- Confidence threshold
- Severity threshold
- Data freshness
- Trust evidence depth
- User/system agency

UX controls:

- Density
- Disclosure depth
- Grouping mode
- Entry point
- Sort priority
- State severity

UI controls:

- Layout topology
- Hierarchy emphasis
- Copy tone
- Type strategy
- Color strategy
- Motion intensity
- Explanation depth

Bad controls:

- Random accent color
- Border radius alone
- Shadow strength alone
- Animation speed alone
- Decorative theme toggle

Unless those are the actual design question.

## Component guidance

The picker should render:

- `LayerControls`: inputs grouped by product, UX, and UI.
- `DirectionMeta`: altitude, product bet, layers changed, tradeoff.
- `ProductModelPanel`
- `StateMatrixPanel`
- `CopyPanel`
- `LayoutPanel`
- `VisualSystemPanel`
- `HandoffPanel`

Scenes must respond to controls and show real state changes, not just update descriptive text.

## Output bans

- No required reference card.
- No required delight card.
- No decorative lore.
- No fake metrics.
- No Acme/Nexus/SmartFlow names.
- No decorative-only controls.
- No dark mode by default just to look polished.
