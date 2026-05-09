# Research Mode

Use when the investigation requires gathering information from multiple sources: web, code, docs, or external references. The goal is to answer a question by having agents search in parallel and triangulate findings.

## Evidence preference

Prefer:

- web sources (articles, documentation, release notes, discussions)
- code implementations and APIs
- existing project docs and patterns
- competitive or alternative approaches

## Research principles

### Triangulation

No finding is solid until supported by 2+ independent sources. A single blog post is a lead, not a finding. Agents should flag single-source claims explicitly.

### Source quality

Rate sources by:

| Factor | High signal | Low signal |
|--------|------------|-----------|
| Authority | Official docs, core maintainers, peer-reviewed | Random blog, undated tutorial |
| Recency | Published within 12 months | 3+ years old without confirmation |
| Specificity | Names versions, gives examples | Vague advice, no context |

### Negative space

Explicitly note what you searched for but couldn't find. Missing information is a finding.

## Mode-specific lenses

Choose from these after the permanent lenses are covered.

### Landscape survey

- Focus on: broad overview of the topic, key players, main approaches, current state of the art
- Do not duplicate: deep technical investigation

### Deep diver

- Focus on: the highest-signal sub-question identified during reconnaissance, with full technical depth
- Do not duplicate: broad landscape mapping

### Competitive / alternative scanner

- Focus on: what else exists, how others solve the same problem differently, tradeoffs between approaches
- Do not duplicate: the deep diver's focused investigation

### Contrarian / counter-narrative

- Focus on: arguments against the prevailing approach, documented failures, abandoned alternatives and why they were abandoned
- Do not duplicate: the devil's advocate (contrarian investigates external evidence, devil's advocate challenges internal assumptions)

### Gap finder

- Focus on: what's missing from the available information, what questions remain unanswered, where the evidence thins out
- Do not duplicate: the blind-spot lens

## Good fit examples

- technology evaluations
- "how do others solve X" investigations
- competitive analysis
- best-practice surveys
- API or library comparisons
- architecture decision research
