# Skill Tests: think

## Category: Encoded Preference

## True Positives (should trigger + produce good output)
1. "what did I learn this week?" → Runs emerge.md → contradict.md chain
2. "emerge" → Same as above
3. "vault health" → Runs graph.md with obsidian-cli or grep fallback
4. "trace my thinking on the Agent Marketplace" → Runs trace.md + episodic-memory search
5. "ghost: how would I respond to Aravinth?" → Runs context.md → ghost.md chain
6. "full synthesis" → Full 5-step chain: context → emerge → contradict → drift → leverage
7. "what have I been avoiding?" → Runs drift.md → emerge.md

## True Negatives (should NOT trigger)
1. "I think about X" → Thinking verb in a sentence, not a trigger
2. "what do you think?" → Asking for Claude's opinion, not a /think invocation
3. "graph this data" → Data visualization, not vault graph (/ops visual instead)

## Edge Cases
1. "full synthesis council" → Should chain the full 5-step AND use /council for multi-perspective debate
2. "emerge and challenge my findings" → Should run emerge.md then challenge.md
3. "ghost, stranger, leverage" → Multiple modes; should run all three in sequence

## Quality Bar
- A "good" /think emerge: reads last 14 days of sessions, maps to competencies, uses fabrication check
- A "poor" /think emerge: generic advice not grounded in actual vault data
