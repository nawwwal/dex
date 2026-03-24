# Trace Thinking Evolution

Shows how thinking on a topic evolved across sessions and decisions.

## Step 1: Understand the Topic
What topic/question is being traced? Extract key terms.

## Step 2: Search Vault and Conversation History
```bash
TOPIC="$1"  # or derived from user's message
grep -r "$TOPIC" ~/.claude/log/ ~/.claude/memory/ --include="*.md" -l 2>/dev/null | sort
```

Also search episodic memory if available:
Use `episodic-memory:search-conversations` with the topic as query.

## Step 3: Build Timeline
For each relevant source, extract:
- Date
- What was said/decided about the topic
- Confidence level at the time

## Step 4: Identify Inflection Points
Where did thinking shift significantly?
What caused the shift? (new information, failed experiment, stakeholder feedback)

## Step 5: Output Timeline
```
## Thinking Timeline: {TOPIC}

### {DATE}: [early position]
[what you believed then, from: source]
Confidence: [high/medium/low]

### {DATE}: [shift]
[what changed and why]

### {DATE}: [current position]
[what you believe now]
Confidence: [solid/evolving/hypothesis]

**Key insight:** [the main lesson from this evolution]
```
