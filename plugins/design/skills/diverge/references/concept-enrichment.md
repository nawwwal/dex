# Concept Enrichment Techniques

Loaded during Step 1 (break down the problem), Step 4 (how each concept dies), and Step 5 (hybrid combinations, narratives, picking what to prototype). Not all sections are used in every step. Follow the loading instructions in SKILL.md.

---

## Break down the problem

Use at the start of Step 1, before generating any concepts.

### 1. Jobs to Be Done

State 3 JTBD statements for the problem. Format: "When [situation], I want to [motivation], so I can [outcome]."

| Type | Purpose |
|------|---------|
| Obvious | The functional job everyone would state |
| Emotional / social | The job the user wouldn't say out loud: status, anxiety reduction, belonging, control |
| Surprising | A non-obvious job discovered by asking "what else is this really about?" |

The surprising JTBD often produces the most interesting concepts. Spend time on it.

### 2. Constraint Identification

What is the **real constraint** underneath the problem? Not "users need a better dashboard" but the actual bottleneck:

| Constraint type | If this is the real constraint, solutions should... |
|----------------|---------------------------------------------------|
| Time | Compress, eliminate, or pre-compute |
| Knowledge | Supply, infer, or bypass the need to know |
| Access | Democratize, proxy, or circumvent the gate |
| Trust | Build, prove, or replace with guarantees |
| Motivation | Create, remove the need for, or make automatic |
| Coordination | Synchronize, eliminate dependencies, or make async |
| Attention | Reduce demand on, redirect, or automate monitoring |

Identify the **primary constraint** and the **secondary constraint**. These directly shape which axes and provocations to prioritize.

### 3. Eliminate the problem

Not "solve it better." Make it not exist.

Ask: **"What would make this problem disappear entirely?"** Three angles:

- **Eliminate the cause:** What upstream change removes the problem?
- **Automate around it:** What if the problem is handled without human involvement?
- **Reframe it:** What if this isn't actually a problem, but a symptom of something else?

Write one problem dissolution statement. This often produces the most radical concept in the set.

### 4. Similar problems in other fields

Who else solves a **structurally similar problem** in a completely different domain?

A restaurant reservation system and a doctor's appointment system share structure. But "restaurant for doctors" isn't interesting. What IS interesting is how restaurants solved the no-show problem (deposits, waitlists, overbooking) and whether those mechanisms transfer.

Identify **2 similar problems in other fields**. For each, name the mechanism they use that the user's domain hasn't tried.

---

## Hybrid combinations

Use during Step 5, after the user has selected concepts to prototype.

### Process

1. From the shortlisted concepts, pick the **3 most structurally different** ones.
2. Create **2-3 hybrid pairs** by combining:
   - Concept A's **mechanism** with Concept B's **interaction model**
   - Or Concept A's **user posture** with Concept C's **system behavior**
3. For each hybrid, write one sentence: "This is [Concept A]'s [mechanism] delivered through [Concept B]'s [interaction model]."
4. **Evaluate:** Is the hybrid more interesting than the weakest shortlisted concept?
5. If yes, propose the swap. If no, discard. Don't force it.

### Quality Check

A good hybrid has emergent properties: it produces something neither parent concept could produce alone. A bad hybrid is just Feature A + Feature B. If the hybrid is additive rather than emergent, discard it.

---

## Day-in-the-Life Narratives

Use during Step 5 for each shortlisted concept (typically 2-4 concepts).

### Format

Three paragraphs per concept:

**Paragraph 1: The Trigger**
What situation brings the user to this product? Be specific: time of day, emotional state, what just happened, what they were doing before. This is not "User opens app." This is "It's 4:47pm on Thursday. Priya just got out of a meeting where the CFO asked about Q3 projections and she didn't have the number. She's annoyed at herself."

**Paragraph 2: The Interaction**
Step by step, what happens? Not features. The felt experience. What does the user see, decide, feel? What surprised them? What was easier than expected? Where did they hesitate?

**Paragraph 3: The Aftermath**
What's different after using it? What did the user NOT have to do? How do they feel? What happens next in their day because of this interaction?

### Quality Gates

- If the narrative sounds like a press release or marketing copy, **rewrite it**. It should sound like a diary entry.
- If the narrative could describe any of the other shortlisted concepts, it's not specific enough to the mechanism. **Rewrite it.**
- If Paragraph 2 is longer than Paragraphs 1 and 3 combined, you're listing features. **Rewrite it.**

---

## How each concept dies

Use during Step 4, as an additional column in the comparison table.

### Format

For each concept, state the **single most likely way it dies**:

| Quality level | Example |
|--------------|---------|
| Too vague (rewrite) | "Users might not like it" |
| Too vague (rewrite) | "Adoption could be low" |
| Specific enough | "Users game the streak mechanic within 2 weeks and it becomes a guilt-producing chore" |
| Specific enough | "The agent makes one wrong decision in month 1 and the user never trusts it again" |
| Specific enough | "The ambient display becomes invisible wallpaper after the novelty wears off, around week 3" |
| Specific enough | "Power users hit the ceiling of the simplified interface in the first session and feel patronized" |

The death scenario should name **who** is affected, **what** goes wrong, and **when** it happens.

---

## Picking what to prototype

Use after Step 5, before moving to building.

The diverge skill is about NOT converging prematurely. But the output must be actionable. This step helps the user decide **what to prototype**, not what to ship.

### Decision Framework

For each shortlisted concept, rate 1-5:

| Factor | Question |
|--------|----------|
| Signal strength | Would a prototype of this teach us something genuinely new? |
| Feasibility to prototype | Can we build a testable version in 1-2 days? |
| Risk of skipping | If we DON'T explore this, do we miss a potentially important insight? |
| Team conviction | Does the team find this genuinely interesting, not just intellectually novel? |

### Recommendation Format

Present as:

```
Prototype first: [Concept X] — highest signal strength, feasible, teaches us [specific thing]
Prototype second: [Concept Y] — riskier but if it works, changes our understanding of [specific aspect]
Park for later: [Concept Z] — interesting but prototype won't teach us enough yet
```

Frame recommendations in terms of **learning**, not commitment. The goal of prototyping is to learn, not to ship.
