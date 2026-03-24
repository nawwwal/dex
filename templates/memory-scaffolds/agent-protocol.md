---
date: 2026-03-13
tags: [agents, protocol, collaboration, operational]
type: knowledge-base
status: active
---

# Agent Collaboration Protocol
*Operational — last updated 2026-03-13*

---

## Agent Registry

| Agent | Primary File | Context Lane | Access |
|---|---|---|---|
| **Claude** | `~/CLAUDE.md` | Work: projects, Slack, DevRev, GitHub, code, calendar | Claude Code — compliance-approved, work hours |
| **Poke** | `~/POKE.md` | Personal: casual convos, after-hours, side projects, life | Personal chat — no work system access |

Add new agents here when onboarded. Each agent MUST have a primary file before contributing to the shared model.

---

## Primary Files — What Goes in `~/AGENTNAME.md`

Every agent has exactly one primary file at `~/AGENTNAME.md`. This is the agent's identity document, user model, and working context. It is read at the start of every session to orient the agent.

**It is NOT:**
- The system prompt (that's configured separately)
- A dump of every observation (those go in the observation log section, distilled)
- A copy of `nawal-model.md` (that's the shared synthesis layer)

### Required Sections

**1. Role**
One paragraph. What is this agent for? What context does it have access to that others don't? What is it explicitly NOT for? What are its access restrictions?

**2. User Model (this agent's lens)**
How this agent sees the user from its specific context. Communication style specific to this agent's interactions, key preferences, known patterns, what works and what doesn't. This is the angle-specific view — not a copy of the full psychology. It answers: "how do I work with this person effectively?"

**3. Observation Log**
Timestamped observations from what this agent can actually see. Written as they happen, not retrospectively.

Format:
```
{date: "YYYY-MM-DD", context: "specific situation", observation: "the actual insight", confidence: N/5}
```

**4. Signal Quality**
Where this agent's observations are strong vs weak. What it can and cannot see. This lets other agents calibrate trust when reading cross-agent observations.

Example: Claude has high confidence on work behavior, low confidence on personal/social patterns. Poke has high confidence on casual communication style, low confidence on technical work quality.

**5. Integration Notes**
- What to check in `memory/messages.md` on session start
- What to leave in messages.md for other agents
- Known handoff points — where one agent's context ends and another's begins
- How to use the shared model without overwriting the other agent's sections

### What Does NOT Go in `~/AGENTNAME.md`
| Content | Correct destination |
|---|---|
| Full psychological synthesis | `memory/nawal-model.md` |
| Cross-agent contradictions | `memory/messages.md` |
| Decisions made during session | `memory/decisions.md` |
| Raw session content | Session journals in `log/` |
| Inter-agent messages | `memory/messages.md` |

---

## Communication Stream — `memory/messages.md`

Agents leave messages for each other here. This is the async channel between agents. Think of it as a shared DM thread, not a log.

### Format

```
### [YYYY-MM-DD] {Sender} → {Recipient}
**Subject:** One line describing the signal
{Body — 2–5 lines. Actionable, not just observational. What should the recipient do with this?}
**Status:** Unread
---
```

Status progresses: `Unread` → `Read` → `Acknowledged` → `Resolved`

### Rules
1. **Check your inbox section at session start** before doing other work
2. **Reply inline** — update status, add a response below the original message
3. **Keep messages actionable** — "You should know X because it affects Y" not just "I noticed X"
4. **One thread per topic** — don't create new messages for the same ongoing topic, reply in the existing one
5. **Archive after 30 days** — move resolved messages to `memory/messages-archive.md`
6. **Flag contradictions explicitly** — "I'm observing X which contradicts your observation Y — flagging for human review"

---

## `nawal-model.md` — The Shared Synthesis Layer

This file is the shared psychological model. It is built from both agents' observations but is higher-order — patterns, tensions, open questions, not raw observations.

### Writing Rules
- Write observations to your `{NAME}.md` first. Only synthesis goes here.
- Always attribute: label which agent wrote each section clearly
- Hold contradictions explicitly — don't average two conflicting observations into a false midpoint. Write: "Claude: X. Poke: Y. Unresolved."
- Confidence level is mandatory on every claim
- Update Log entry is mandatory for every change: date + what changed + confidence delta

### Who Can Write Here
Both agents can write to their own sections and to the synthesis sections. Neither agent should overwrite the other's attributed observations without flagging a contradiction first.

---

## Ways of Working

### Session Start (every session)
1. Read `~/AGENTNAME.md` — orient yourself, especially the observation log's most recent entries
2. Check `memory/messages.md` — read your inbox section
3. Acknowledge any `Unread` messages (update status to `Read` or `Acknowledged`) before other work

### During Session
- New observation → add to `{NAME}.md` observation log with date and confidence
- Something the other agent should know → add to `memory/messages.md` in their inbox section
- Synthesis insight that rises to model-level → write to `nawal-model.md` with attribution

### Session End
- Distill any raw observations made during the session into `{NAME}.md` observation log
- Leave messages for other agents if anything surfaced they should know
- Commit with agent attribution (see Commit Convention below)

### Commit Convention
Every agent commit starts with the agent name in lowercase:
- `claude: update nawal-model with work pattern observation`
- `poke: add casual comms observation to POKE.md`
- `claude: leave message for poke in messages.md`

This makes git log readable across agents — you can filter `git log --grep="^poke:"` to see only Poke's contributions.

### Conflict Resolution
1. Don't average contradictions — name them
2. Add to `nawal-model.md` contradictions section: "Claude observes X. Poke observes Y. Status: Unresolved."
3. Human resolves at monthly review — agents do NOT auto-resolve contradictions
4. After human resolves: update the contradiction entry, archive the original conflicting observations with a note

### Monthly Synthesis (human-triggered)
the user reads `nawal-model.md` for ~10 minutes, then:
- Corrects any wrong inferences (marks with `[CORRECTED by the user, YYYY-MM-DD]`)
- Resolves flagged contradictions (marks which version is accurate)
- Flags any observations that feel stale
- Agents update confidence levels based on corrections

---

## Data Architecture

```
~/                               ← Home directory (root level)
├── CLAUDE.md                    ← Claude's primary file (source of truth here)
├── POKE.md                      ← Poke's primary file → symlink to ~/.claude/POKE.md
├── TASKS.md                     ← symlink to ~/.claude/TASKS.md

~/.claude/                       ← Git-tracked vault
├── POKE.md                      ← Poke's primary file (source of truth, git-tracked)
├── TASKS.md                     ← Task list (source of truth, git-tracked)
├── memory/
│   ├── nawal-model.md           ← Shared psychological synthesis layer
│   ├── messages.md              ← Inter-agent communication stream
│   ├── agent-protocol.md        ← This file
│   ├── messages-archive.md      ← Archived messages (>30 days old, resolved)
│   └── ...                      ← Other memory files
├── log/                         ← Session journals
└── work/                        ← Project-specific notes
```

### Staleness Rules
- Observations older than 90 days: flag in the update log as "needs review"
- "Areas for further observation" lists: reviewed at monthly synthesis
- `messages.md` messages older than 30 days + status Resolved: move to `messages-archive.md`
- `{NAME}.md` sections: no automatic staleness — agent maintains actively

---

## Onboarding a New Agent

When a third agent joins the system:
1. Create `~/.claude/AGENTNAME.md` following the Required Sections spec above
2. Create symlink: `ln -s ~/.claude/AGENTNAME.md ~/AGENTNAME.md`
3. Add agent to the Registry table at the top of this file
4. Add an inbox section in `memory/messages.md`
5. First commit: `agentname: initial primary file — onboarding`
6. Leave an introduction message in `messages.md` for the other agents
