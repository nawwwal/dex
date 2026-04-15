# Same Question Across Time

Asks the same question against vault data from different time periods to show how context compounds.

## Step 1: Identify the Question
What question should be asked across time? e.g.:
- "What is my most important project?"
- "What am I worried about?"
- "What's my biggest blind spot?"
- "How do I think about X?"

## Step 2: Query Each Period
Answer the question using ONLY data from:
- 90 days ago (using sessions from that period)
- 60 days ago
- 30 days ago
- Today

## Step 3: Show the Evolution
How did the answer change?
What caused each shift?
What stayed constant across all periods?

## Output
```
## {QUESTION} — Across Time

### 90 days ago ({DATE})
[answer based only on data from that period]

### 60 days ago ({DATE})
[answer + what changed]

### 30 days ago ({DATE})
[answer + what changed]

### Today
[current answer]

**What compounded:** [the insight that emerged from seeing all four together]
```
