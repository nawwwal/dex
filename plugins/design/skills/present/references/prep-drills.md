# Prep Drills

Use this when the user wants to get prepped before a design presentation, rehearse a narrative, or identify better questions they could have asked during or after a conversation.

## Prep Output

Default shape:

Known:
- The specific idea, project, artifact, or flow the user is presenting.
- The exact decision the room needs to make.
- The obvious conversation the room will probably have.

Weak joint:
- The precise place the narrative, evidence, stakeholder alignment, or decision logic can break.

Sharper questions:
1. Question.
   Context used: ...
   First principle tested: ...
   Why it matters: ...
   What a strong answer would reveal: ...
2. Question.
   Context used: ...
   First principle tested: ...
   Why it matters: ...
   What a strong answer would reveal: ...
3. Question.
   Context used: ...
   First principle tested: ...
   Why it matters: ...
   What a strong answer would reveal: ...

Likely objections:
- Objection: ...
  Response path: ...

Next prep move:
- The one thing the user should clarify before the meeting.

## Question Quality Bar

Do not ask questions that merely sound smart. A useful prep question changes the conversation by forcing a clearer decision, sharper evidence, or more honest tradeoff.

Strong question:

- names the specific idea, user, screen, flow, stakeholder, decision, evidence, or tradeoff
- states the first-principles uncertainty being tested
- can be answered by someone in the room
- reveals whether the design direction is valid
- helps the user decide what to show or not show
- connects to user behavior, business impact, operational risk, or product judgment

Weak question:

- can be asked about any design project without changing a word
- asks whether people like it
- asks for general thoughts
- hides multiple questions inside one sentence
- tries to impress instead of clarify
- reopens decisions that are already closed unless the closure is false

Before giving prep questions, build a context model:

- artifact:
- actor:
- current behavior:
- proposed behavior:
- mechanism:
- stakeholder stake:
- evidence:
- tradeoff:
- launch risk:

If a field is unknown, either ask for it or mark the question as conditional. Do not pretend generic insight is contextual.

## Before The Meeting

Use these categories to prep the user. Rewrite every question with the actual project terms before showing it.

Decision:

- For [project], is the room deciding viability, scope, launch readiness, sequencing, or ownership?
- If [stakeholder group] cannot approve [direction], what useful commitment can they make about [next step]?
- Is [feedback ask] secretly asking the audience to decide [hidden decision]?

Problem:

- What would make [current failure] undeniable to [skeptical stakeholder]?
- Is the current problem statement for [project] describing [user pain], or just defending [preferred solution]?
- Which part of [current failure] gets worse if [direction] ships poorly?

Evidence:

- What is the strongest proof for [current failure], and should it appear before [artifact] or stay in appendix?
- What evidence about [claim] is missing but likely to be demanded by [stakeholder]?
- Which claim about [impact/mechanism] should be softened because the current evidence only proves [narrower claim]?

Audience:

- What will [stakeholder] fear losing if [direction] wins: speed, control, compliance, craft quality, revenue, team ownership, or roadmap flexibility?
- Who benefits from keeping [current flow/process] unchanged?
- Which topic in [project] is likely to become a proxy fight for [larger concern]?

Tradeoff:

- What are you making harder in [direction] so [more important behavior/outcome] becomes easier?
- Which tradeoff in [direction] does the room need to explicitly accept before judging [artifact]?
- Which alternative to [direction] looks attractive until the cost to [user/team/system] is named?

Design:

- Which screen, state, or transition in [artifact] proves [mechanism] works?
- What part of [artifact] is most likely to be misread by [audience/user], and what would that misreading cause?
- Where does [direction] ask [actor] to trust the system, and what verification or confidence signal supports that trust?

Launch:

- What could fail after launch in [direction] that is invisible in [static mocks/prototype]?
- What support, ops, compliance, or edge-case burden might [direction] create for [team]?
- What signal after launch would prove [mechanism] changed [target behavior]?

## After A Conversation

When reviewing a meeting, Slack thread, critique, or feedback session, identify missed questions.

Use this format:

- Missed question: ...
- Moment it should have been asked: ...
- What it would have exposed: ...
- Why the conversation needed it: ...
- How to ask it next time: ...

Look for:

- vague agreement that hid a decision
- taste feedback that was not translated into a practical concern
- unresolved stakeholder anxiety
- evidence that was accepted too quickly
- alternatives dismissed without naming the tradeoff
- disagreement over the problem rather than the design
- feedback that drifted away from the stated open questions

## Rehearsal Challenge

If the user provides a draft narrative, challenge it in this order:

1. For [project], is the meeting really for viability, critique, approval, alignment, or risk surfacing?
2. What must [audience] believe about [current failure] before seeing [artifact]?
3. Which claim about [direction] is most vulnerable to evidence, stakeholder resistance, or real-world usage?
4. Which stakeholder will object first to [tradeoff], and what practical concern sits under that objection?
5. What question should the user ask before showing [artifact] so the room judges it against [problem] instead of taste?
6. What question should the user ask immediately after showing [specific flow] to test [first-principles uncertainty]?
7. What should the user refuse to discuss because it is outside [decision boundary]?

## Tone

Be direct. The user wants preparation, not reassurance.

Good:

"The weak joint is the decision boundary. You are asking for feedback, but the narrative sounds like approval. Ask this first: Are we deciding whether this direction is viable, or whether it is ready to ship?"

Avoid:

"Here are some questions that could apply to any design review."
