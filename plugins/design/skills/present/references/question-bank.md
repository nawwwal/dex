# Contextual Question Bank

Use this file to ask sharper intake questions. Ask only 3-5 questions per turn unless the user asks for a full worksheet.

Do not copy these as generic questions. Convert each prompt into a project-specific question by naming the user's actual idea, artifact, user, stakeholder, metric, constraint, or decision.

Before asking, fill this context model:

- idea or project:
- audience:
- artifact being shown:
- user or actor:
- user job:
- current failure:
- proposed mechanism:
- evidence:
- decision needed:
- tradeoff:
- likely resistance:

If this model is too empty, ask only for the missing fields needed to create contextual questions.

## First Round

Use these only to gather missing context:

1. For [project/artifact], is this a casual chat, critique/review, or approval-style presentation?
2. Who is in the room for [project], and what can each person approve, block, or reshape?
3. By the end of this conversation, what decision should be clearer for [project]?
4. What problem does [project] solve before we name the solution?
5. What artifact are we presenting for [project]: prototype, static mocks, doc, concept, flow, strategy, or shipped learning?

## Problem

- Which specific user or team experiences [current failure] in [journey moment]?
- What behavior, support ticket, drop-off, delay, rework, compliance issue, or repeated workaround proves [current failure] exists?
- How did [project/team] learn about [current failure], and whose view is missing?
- What evidence would make [skeptical stakeholder] accept that [current failure] is worth solving now?
- What gets worse for [user/business/ops] if [current failure] remains unsolved for another cycle?
- After [proposed mechanism] works, what should [actor] be able to do, understand, decide, or trust differently?
- Is [current failure] mainly a user comprehension problem, operational risk, business conversion issue, design-system inconsistency, or stakeholder-alignment gap?

## Audience

- In the room for [project], who can approve, block, or reshape [decision needed]?
- What prior belief will [stakeholder] bring about [current flow/problem]?
- Does [stakeholder] need proof of impact, reassurance about risk, or a concrete tradeoff before accepting [direction]?
- What language does this audience already use for [problem], and should the narrative adopt or correct that language?
- Which topic around [project] is likely to pull the room away from [decision needed]?
- Which part of [artifact] will create noise for this audience and should stay in appendix or working files?

## Thinking

- Which constraint, such as tech, policy, ops load, design system, migration, data quality, or timeline, most shaped [direction]?
- What product belief does [proposed mechanism] depend on?
- What alternatives to [direction] did you explore, and what exact cost made each weaker?
- Which user or business problem did you intentionally leave unsolved in [scope], and why?
- What assumption about [actor behavior] must be true for [direction] to work?
- Which moment in [artifact] best proves [proposed mechanism], and what observable change makes it strong?
- Which moment in [artifact] is most likely to fail under real usage, stakeholder review, or edge cases?

## Open Questions

- What feedback on [specific moment/flow] would change the next design move?
- What question about [constraint/decision/stakeholder risk] can only this audience answer?
- What should the room ignore in [artifact] because it does not affect [decision needed] yet?
- What feedback would be unhelpful because [closed decision] is already fixed for [reason]?
- Which decision around [project] should not be reopened unless someone can disprove [evidence/assumption]?
- Which tradeoff in [direction] do you need the room to explicitly accept?
- What would count as a successful review for [project]: approval, sharper risk, narrowed scope, stronger evidence, or a concrete next step?

## Prep Questions

Generate these from the context model. Each prep question must name the specific object under pressure.

Examples of acceptable contextual questions:

- "Your approval-risk flow assumes ops users will trust the risk label without opening the details drawer. What evidence shows they will act on that label instead of escalating manually?"
- "If the PM is optimizing activation this quarter, will they see the extra eligibility step as reducing failed payouts or as adding friction before value is visible?"
- "In the bulk-payout review screen, what prevents a finance operator from approving a high-risk batch just because the new summary makes the flow feel complete?"

Use these first-principles transforms:

- If the design changes behavior, ask what currently motivates that behavior and why the new flow would overpower it.
- If the design adds information, ask what decision that information changes and what happens if the user ignores it.
- If the design removes a step, ask what error, accountability, or confidence signal that step was quietly providing.
- If the design introduces automation or AI, ask where the user must verify, override, or distrust the system.
- If the design simplifies a complex flow, ask which edge case has been hidden and who pays for it later.
- If the design depends on stakeholder alignment, ask what each stakeholder must believe before the design can be judged fairly.
- If the design claims speed, ask what quality, control, auditability, or learning is being traded away.
- If the design claims clarity, ask which ambiguity has actually been resolved and which one has only been moved.

## Designs

- Does [artifact] need a prototype because sequence, delay, state change, or recovery matters?
- Which primary flow in [artifact] best proves [proposed mechanism]?
- Where should the audience look first in [screen/flow], and what should that moment prove?
- What must the room understand about [problem/evidence/constraint] before inspecting visual details?
- Which alternatives to [direction] should stay ready in the working file, and what objection would justify showing each one?
- What note-taking method will keep feedback attached to [specific frame/flow/decision] instead of becoming general design commentary?

## Feedback Translation

When the user says "they liked it," ask:

- What did they think it would improve?
- What did they understand faster?
- What risk did it reduce?

When the user says "they hated it," ask:

- What practical concern sat under the reaction?
- Was the concern about behavior, comprehension, cost, risk, politics, or change resistance?
- What evidence would separate preference from product risk?

When the user says "I want it to feel better," ask:

- What user action should become easier?
- What hierarchy should become clearer?
- What emotion or confidence signal should change, and what visual or interaction choice would create that change?
