# Agent Tests: design-reviewer

## Category: Encoded Preference (agent, auto-triggered)

## True Positives (auto-trigger conditions)
1. Write tool used on *.tsx file with 25+ lines containing JSX → agent auto-fires
2. User says "review my UI" → agent invoked
3. User says "check accessibility" → agent invoked

## True Negatives (should NOT auto-trigger)
1. Write to *.ts file (no JSX) → not a UI review
2. Write to *.tsx with only type changes (< 20 lines) → too small to review
3. Write to *.md file → not UI code

## Quality Bar (after Reflection Pass upgrade)
- A "good" review: Pass 1 generates findings, Pass 2 self-critiques against Blade maintainer persona, final report is refined
- Pass 2 must check: any Blade violations correctly identified? Any false positives (valid patterns flagged)?
- A "poor" review: only Pass 1, no self-critique, treats all flagged items as equally severe
