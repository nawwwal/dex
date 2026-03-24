# Design Case Study

Creates a portfolio case study narrative from vault data.

## Step 1: Load Project Context
Read from vault:
- work/{project}/index.md — project overview
- Recent sessions mentioning this project
- memory/decisions.md entries for this project
- Any success criteria or impact metrics

## Step 2: Structure the Narrative
3-act structure:

### Act 1: Problem
- What was the business/user problem?
- What were the constraints?
- Who were the stakeholders?
- What was the initial state?

### Act 2: Process
- How did you approach it?
- Key design decisions made (link to decisions.md)
- What alternatives were considered?
- What failed and what was learned?

### Act 3: Outcome
- What shipped?
- Metrics: before vs. after
- Stakeholder feedback
- What would you do differently?

**Hero image (optional):** Portfolio case studies are stronger with a visual outcome.
If the shipped design can be described, invoke `/generate-image`:
> `/generate-image` — prompt: "clean product UI of [feature]: [brief description of what shipped]" — aspect-ratio: 16:9

## Step 3: Map to Competencies
Tag each section with the relevant competency:
- [Design Engineering] — if technical implementation was involved
- [Ownership] — if you drove it end-to-end
- [UI Design] — if visual quality is demonstrated
- [Product Thinking] — if user/business impact is shown

## Step 4: Write the Case Study
Minimum 500 words. Specific, concrete, metrics-driven.
Avoid vague language. Every claim needs evidence.

## Step 5: Append to career/case.md
Add a reference to this case study in the Evidence Log:
`- [Project]: [[work/{project}/index]] — [competency tags] — Case study written`
