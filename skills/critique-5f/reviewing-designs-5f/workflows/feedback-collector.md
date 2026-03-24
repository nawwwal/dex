# Feedback Collector Workflow

**Purpose:** Runs AFTER the main `reviewing-designs-5f` skill completes to collect optional feedback.

---

## When to Run

- **Trigger:** Immediately after 5F design review completes
- **Blocking:** No (user can skip entirely)
- **Frequency:** Every review (but always optional)

---

## Workflow Steps

### Step 1: Display Feedback Prompt

```markdown
---
## 📊 Help This Reviewer Learn (Optional - 10 seconds)

**How useful was this review?**
⭐️ [1] [2] [3] [4] [5]

**What was most helpful?** (check all that apply)
- [ ] Specific issues identified
- [ ] Relevance to our product/users
- [ ] Actionable recommendations
- [ ] Understanding of our business context
- [ ] 5F Framework scoring accuracy

**What did I miss about your product/users/business?**
[Free text field - optional]

**Did you disagree with any scores?**
If you would score differently, enter your scores:

| Dimension | Current | Your Score |
|-----------|---------|------------|
| Fast      | 7/10    | [____]     |
| Focused   | 6/10    | [____]     |
| Fun       | 8/10    | [____]     |
| Fluent    | 7/10    | [____]     |
| Fair      | 9/10    | [____]     |

[Skip Feedback] [Submit]
```

### Step 2: Capture Structured Data

If user provides feedback, structure as:

```json
{
  "review_id": "uuid-generated",
  "timestamp": "ISO-8601-format",
  "design_type": "extracted-from-review",
  "product_area": "user-specified-or-unknown",
  "5f_scores_original": {
    "fast": 7,
    "focused": 6,
    "fun": 8,
    "fluent": 7,
    "fair": 9
  },
  "feedback": {
    "rating": 4,
    "helpful_aspects": ["specificity", "actionability"],
    "missed_context": "User's free text response",
    "score_overrides": {
      "fast": 8,
      "focused": null
    }
  },
  "metadata": {
    "review_number": "calculated-from-sessions-count",
    "learning_mode_shown": "mode_a|mode_b|both|none"
  }
}
```

### Step 3: Append to Log

```bash
# Append JSON line to review-sessions.jsonl
echo '{"review_id": "..."}' >> skill-memory/reviewing-designs-5f/feedback/review-sessions.jsonl
```

### Step 4: Immediate High-Confidence Learning

If feedback contains explicit new context:
- **Business rule mentioned** → Add to `experiments/active-hypotheses.md`
- **Context question answered** → Update relevant `context/*.md` file immediately
- **Consistent pattern (5th mention)** → Promote to `LEARNINGS.md`

### Step 5: Thank User

```markdown
✅ **Thanks! This helps the reviewer improve.**

Your feedback:
- Added to learning log (review-sessions.jsonl)
- Will be analyzed in weekly learning cycle
- [IF high-confidence] Updated: context/user-personas.md with "Primary users: Business managers"

You can view what I've learned anytime with: **View learned context**
```

---

## Implementation

This is implemented as a **post-review prompt** that appears after the main review output.

**In practice:**
1. User invokes `reviewing-designs-5f` skill
2. Skill runs normally, outputs review
3. **Then** this feedback collector runs
4. User optionally provides feedback
5. Feedback is logged for weekly analysis

**No modification to original skill required.**

---

## User Controls

- **Skip entirely:** Click "Skip Feedback" or just continue
- **Disable globally:** Set `SKIP_5F_FEEDBACK=true` in workspace settings
- **View feedback history:** `/context-5f history`
