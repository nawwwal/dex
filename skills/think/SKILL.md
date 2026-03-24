---
name: think
description: "Use for cognitive operations — 'emerge', 'contradict', 'challenge', 'stranger', 'close', vault health ('graph', 'orphans'), or deep synthesis ('trace', 'ghost', 'leverage', 'full synthesis', 'deep audit')."
allowed-tools: Read, Write, Bash, Grep, Glob, mcp__plugin_episodic-memory_episodic-memory__search
---

# /think — Cognitive Intelligence Router

Read the user's intent and dispatch to the correct sub-skill. Multiple sub-skills can chain in sequence.

## Dispatch Logic

### Emergence / Learning
Triggers: "emerge", "patterns", "what did I learn", "TIL", "goal check", "what's stuck", "connections"
Chain: `$CLAUDE_SKILL_DIR/emerge.md` → `$CLAUDE_SKILL_DIR/contradict.md` [check for conflicts with new patterns]

### Full Synthesis / Deep Audit
Triggers: "full synthesis", "deep audit", "full think", "everything"
Chain (sequential):
1. `$CLAUDE_SKILL_DIR/context.md` [multi-hop vault traversal first]
2. `$CLAUDE_SKILL_DIR/emerge.md`
3. `$CLAUDE_SKILL_DIR/contradict.md`
4. `$CLAUDE_SKILL_DIR/drift.md`
5. `$CLAUDE_SKILL_DIR/leverage.md`
Optional: If user says "council" — use /council skill for multi-perspective debate.
Note: Council requires no active Agent Team in the session.

### Vault Graph / Health
Triggers: "graph", "map", "orphans", "vault health", "deadends", "topology", "backlinks"
Chain: `$CLAUDE_SKILL_DIR/graph.md` [runs obsidian-cli or grep fallback]

### Thinking Evolution
Triggers: "trace X", "how did my thinking on X evolve", "history of X", "what changed"
Chain: `$CLAUDE_SKILL_DIR/trace.md` + episodic-memory:search-conversations

### What's Being Avoided
Triggers: "drift", "what have I been avoiding", "going quiet", "blind spots", "silences"
Chain: `$CLAUDE_SKILL_DIR/drift.md` → `$CLAUDE_SKILL_DIR/emerge.md` [surface why silences matter]

### Devil's Advocate
Triggers: "challenge my thinking", "argue against", "steelman opposite", "pre-mortem"
Chain: `$CLAUDE_SKILL_DIR/challenge.md` [standalone — needs the specific claim]

### Find Contradictions
Triggers: "contradict", "incompatible beliefs", "conflicting decisions", "find conflicts"
Chain: `$CLAUDE_SKILL_DIR/contradict.md` [standalone]

### Deep Vault Context
Triggers: "context", "load context", "what's going on", "vault state"
Chain: `$CLAUDE_SKILL_DIR/context.md`

### Answer As Me
Triggers: "ghost", "how would I respond to", "answer as me", "what would I say", "in my voice"
Chain: `$CLAUDE_SKILL_DIR/context.md` [load voice.md + decisions + sessions] → `$CLAUDE_SKILL_DIR/ghost.md`

### Outside View
Triggers: "stranger", "how would a new teammate see", "outside view", "first impression"
Chain: `$CLAUDE_SKILL_DIR/context.md` → `$CLAUDE_SKILL_DIR/stranger.md`

### Session Close
Triggers: "close", "session done", "what did I learn today", "close session"
Chain: `$CLAUDE_SKILL_DIR/close.md` → [if confidence updates suggested] → emerge.md subset

### Leverage / Focus
Triggers: "leverage", "what to focus on", "compound", "highest ROI", "where to invest"
Chain: `$CLAUDE_SKILL_DIR/context.md` → `$CLAUDE_SKILL_DIR/leverage.md`

### Same Question Across Time
Triggers: "compound X", "same question", "how has X changed over time"
Chain: `$CLAUDE_SKILL_DIR/compound.md`
