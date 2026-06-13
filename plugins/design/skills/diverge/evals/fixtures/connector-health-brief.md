# Connector Health Dashboard Brief

Surface: connector health dashboard for AI agents.

User role: platform operator or agent owner.

Core job: decide which connector problems to fix first and whether agents are safe to run.

Product objects:
- Connector
- Agent
- Sync run
- Credential
- Scope grant
- Schema mapping

Known states:
- expired auth
- rate limit
- API down
- scope changed
- schema mismatch
- setup incomplete
- not connected
- healthy

Available user actions:
- reconnect credential
- retry sync
- approve scope change
- review schema diff
- pause agent
- open repair guide
- assign owner

System actions:
- detect health degradation
- block or warn on agent runs
- queue retries
- surface blast radius

Constraints:
- B2B SaaS product register
- operators need fast triage, not decorative dashboards
- must support 20+ connectors without alert fatigue

Anti-patterns:
- app grid with equal-weight cards
- alert carousel
- status colors with no repair path
- metaphor names that hide mechanics
