# Layered Pipeline

Use this for non-trivial crux work: strategy, product framing, PRDs, design direction, source artifacts, repo-backed plans, loaded language, emotionally charged claims, or any problem where one quick question would miss the structure.

The pipeline is fixed. The visible answer is adaptive.

## Method Agents

When subagents are available and permitted, use one method agent per method group. When subagents are not available, run the same methods internally in the same order.

Do not show method-agent outputs to the user. Each method produces an intermediate artifact for later stages.

## Fixed DAG

```text
0. Intake
   ↓
1. Ground Truth Pass
   ↓
2A. Naming Pressure      2B. Evidence Ledger      2C. Context Map
   ↓                     ↓                       ↓
3A. Dao Extraction       3B. Qi Inspection        3C. Reversal / Opposite-Truth
        \                 |                       /
         \                ↓                      /
          → 4. Crux Candidate Collation ←
                         ↓
5A. Weak Joint Selection     5B. Specific Bet Formulation
             \               /
              → 6. Crude Test Design
                         ↓
7. Final Question Selection
                         ↓
8A. Essence Writer
                         ↓
8B. Reframing Generator      8C. Opportunity Expander
             \               /
              → 8D. Final Cohesion Pass
```

## Stage Contracts

### 0. Intake

Input: user request.

Output:

```text
surface claim:
user intent:
stakes:
provided artifacts:
visible decision:
```

Do not solve the problem here. Normalize what kind of crux work this is.

### 1. Ground Truth Pass

Input: intake.

Inspect files, docs, code, screens, pasted text, issue language, or conversation context before reasoning from the user's wording.

Output:

```text
observed facts:
user terms:
artifact terms:
contradictions:
missing evidence:
source reliability:
```

Every later method must use this as source of truth. If no external source exists, say the source is only the user's claim.

### 2A. Naming Pressure

Runs in parallel with `2B` and `2C`.

Input: ground truth pass.

Job: convert loaded nouns and style words into observable behavior.

Examples:

- `deep` → higher retention from one capability
- `wide` → more surface area across adjacent jobs
- `trust` → user delegates a high-risk action or accepts a recommendation
- `premium` → status signal, lower perceived risk, refined hierarchy, or enterprise readiness
- `simple` → fewer steps, fewer choices, lower cognitive load, faster first success, or lower visual density

Output:

```text
loaded terms:
behavior translations:
terms still ambiguous:
```

### 2B. Evidence Ledger

Runs in parallel with `2A` and `2C`.

Input: ground truth pass.

Job: classify each load-bearing claim as perception, inference, analogy, testimony, taste, social proof, memory, or assumption.

Output:

```text
claim evidence:
strongest evidence:
weakest evidence:
claims pretending to know more than they know:
```

Treat frameworks, analogies, market maps, and business-model language as inference unless tied to observed behavior.

### 2C. Context Map

Runs in parallel with `2A` and `2B`.

Input: ground truth pass.

Job: map the system around the claim.

Output:

```text
actors:
incentives:
constraints:
handoffs:
decision rights:
failure points:
feedback loops:
```

This prevents a clever crux from ignoring the real system.

### 3A. Dao Extraction

Runs after `2A`, `2B`, and `2C`.

Input: naming pressure, evidence ledger, and context map.

Job: name the invisible operating principle, invariant, or causal model.

Output:

```text
dao:
what must stay true:
what the current frame hides:
```

Example: "This is not about going wide or deep. It is about whether one capability creates enough customer pull to survive incumbent entry."

### 3B. Qi Inspection

Runs after `3A` and the ground truth pass.

Input: dao and grounded facts.

Job: inspect whether the visible expression carries or contradicts the dao.

Visible expression can mean product shape, feature, interface, workflow, roadmap, strategy phrase, deck slide, or written claim.

Output:

```text
qi:
where qi supports dao:
where qi contradicts dao:
```

### 3C. Reversal / Opposite-Truth

Runs after `2A` and `2C`.

Input: naming pressure and context map.

Job: find where the opposite claim is true, where both claims are true, and what framing makes the original debate irrelevant.

Output:

```text
where original is true:
where opposite is true:
where both are true:
better frame:
```

Use this to dissolve prestige abstractions without making "avoid binaries" the whole answer.

### 4. Crux Candidate Collation

Input: dao extraction, qi inspection, and reversal.

Output:

```text
candidate avoided realities:
candidate weak joints:
candidate specific bets:
candidate tests:
candidate crux questions:
discarded clever lines:
```

Discard anything that sounds elegant but would not change the work.

### 5A. Weak Joint Selection

Runs in parallel with `5B`.

Input: collated candidates.

Job: choose the one place the idea is most likely lying to itself.

Output:

```text
weak joint:
why this is the weak joint:
what would change if it fails:
```

### 5B. Specific Bet Formulation

Runs in parallel with `5A`.

Input: collated candidates.

Job: rewrite the strategy as a concrete bet.

Output:

```text
specific bet:
customer:
moment:
capability:
behavior change:
reason:
commitment signal:
```

Use this shape internally:

```text
For [customer], in [moment], [capability] changes [behavior], because [reason]. We know it works if [commitment signal].
```

Do not force this exact sentence into the final answer if another shape reads better.

### 6. Crude Test Design

Input: weak joint and specific bet.

Job: design the smallest test that reduces uncertainty by measuring commitment, not praise.

Output:

```text
test:
success signal:
failure signal:
desirability signal:
feasibility signal:
viability signal:
legibility signal:
time to test:
what it teaches:
```

### 7. Final Question Selection

Input: weak joint, specific bet, and crude test.

Job: choose the one question whose answer changes the direction of the work.

Output:

```text
crux question:
why this question decides the matter:
```

Most responses should end with this question. If the user needs a concrete answer, recommendation, or rewrite more than a question, place the decisive line last instead.

### 8A. Essence Writer

Input: selected weak joint, specific bet, crude test, and final question.

Job: explain the core in simple language.

Output:

```text
essence:
plain-language explanation:
```

The essence should make the user understand what is really at stake.

### 8B. Reframing Generator

Runs after `8A` and in parallel with `8C`.

Input: essence.

Job: give the user better ways to frame the conversation.

Output:

```text
better frames:
questions to ask instead:
terms to replace:
```

A better frame must move the user closer to a customer, moment, behavior, capability, proof, or tradeoff.

### 8C. Opportunity Expander

Runs after `8A` and in parallel with `8B`.

Input: essence.

Job: show the ideas that open up once the core is understood.

Output:

```text
product directions:
research directions:
positioning directions:
roadmap directions:
```

Do not brainstorm from the original bad frame. Expand from the essence.

### 8D. Final Cohesion Pass

Input: essence, reframes, opportunities, test, and final question.

Job: render one human answer.

Rules:

- Use active voice.
- Use concrete nouns.
- Keep related ideas together.
- Omit method labels unless the user asks for the method.
- Use sections only when they improve scanning.
- Make each paragraph cause the next paragraph.
- Lead with the biggest flaw when critiquing.
- Define style or strategy words through observable mechanics.
- Do not fill a fixed template.
- End with the crux question unless a recommendation, rewrite, or next test is more useful.

## Adaptive Rendering

The final answer takes the shape of the topic:

- Strategy: a short memo that refuses the weak frame, states the real bet, names the weak joint, and offers better frames.
- Product idea: a diagnosis of the painful moment, specific bet, crude test, and next questions.
- Design critique: biggest flaw first, weak joint named, mechanics explained, better directions offered.
- Naming or copy: sharper language, why it works, what it replaces, what behavior it should create.
- PRD or repo-backed plan: observed source pressure, contradiction, deciding assumption, test, and crux question.
- Vague style request: translate words into hierarchy, density, contrast, motion, copy, interaction, or behavior.

The final answer should leave the user with more usable ideas because the core is clearer.
