# Learning System Orchestrator

**Purpose:** Coordinates the entire learning workflow around the original `reviewing-designs-5f` skill.

---

## Architecture

```
USER INVOKES: reviewing-designs-5f skill
                        ↓
┌────────────────────────────────────────────────────────┐
│             ORCHESTRATOR (This Workflow)               │
│                                                        │
│  Step 1: Load Learned Context                         │
│  Step 2: Run Original Skill (untouched)               │
│  Step 3: Append Mode A (Experimental Observation)     │
│  Step 4: Append Mode B (Context Questions, if needed) │
│  Step 5: Collect Feedback (optional)                  │
│  Step 6: Log Session                                  │
│  Step 7: Check Weekly Learning Trigger                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Workflow

### Step 1: Load Learned Context

```python
def load_learned_context():
    """
    Load all learned context before review starts.
    This provides the original skill with learned business rules,
    user personas, calibrated scoring, etc.
    """
    context = {
        "learnings_summary": read_file("skill-memory/reviewing-designs-5f/LEARNINGS.md"),
        "business_rules": read_file("skill-memory/reviewing-designs-5f/context/business-rules.md"),
        "user_personas": read_file("skill-memory/reviewing-designs-5f/context/user-personas.md"),
        "design_system": read_file("skill-memory/reviewing-designs-5f/context/design-system.md"),
        "competitive_context": read_file("skill-memory/reviewing-designs-5f/context/competitive-context.md"),
        "product_specifics": read_file("skill-memory/reviewing-designs-5f/context/product-specifics.md"),
        "scoring_calibrations": load_scoring_weights(),
        "active_hypotheses": read_file("skill-memory/reviewing-designs-5f/experiments/active-hypotheses.md")
    }

    return context
```

### Step 2: Run Original Skill

```python
def run_original_review_skill(design_input, learned_context):
    """
    Execute the original reviewing-designs-5f skill.

    IMPORTANT: The original skill is NOT modified.
    We simply pass learned context as additional input.
    """

    # Inject learned context into skill prompt
    enhanced_prompt = f"""
    {design_input}

    ---
    LEARNED CONTEXT (from previous reviews):

    {learned_context["learnings_summary"]}

    Use this context to inform your review, especially:
    - Known business rules and compliance requirements
    - User personas and environment
    - Established design patterns
    - Calibrated scoring thresholds
    """

    # Run original skill
    review_output = invoke_skill("reviewing-designs-5f", enhanced_prompt)

    return review_output
```

### Step 3: Append Mode A (Experimental Observation)

```python
def append_mode_a_observation(review_output, learned_context, design_input):
    """
    Add experimental observation section to review output.
    This is 5% learning content.
    """

    # Select relevant hypothesis
    hypothesis = select_hypothesis_for_observation(
        active_hypotheses=learned_context["active_hypotheses"],
        design_type=design_input.type
    )

    if hypothesis:
        observation = generate_observation(hypothesis, design_input)
        review_output += f"\n\n{observation}"

    return review_output
```

### Step 4: Append Mode B (Context Questions)

```python
def append_mode_b_questions(review_output, learned_context, design_input):
    """
    Add context questions if uncertainties detected.
    """

    # Detect uncertainties
    uncertainties = detect_uncertainties(design_input, learned_context)

    # Apply smart suppression
    review_count = get_review_count()
    questions_to_show = filter_questions(
        uncertainties,
        review_count,
        already_answered=learned_context.get("answered_questions", [])
    )

    # Generate questions (max 2)
    if questions_to_show:
        questions = generate_questions(questions_to_show[:2])
        review_output += f"\n\n{questions}"

    return review_output
```

### Step 5: Collect Feedback

```python
def collect_feedback(review_output, review_id):
    """
    Prompt user for optional feedback.
    """

    # Check if feedback is disabled
    if os.getenv("SKIP_5F_FEEDBACK") == "true":
        return None

    # Append feedback prompt
    feedback_prompt = generate_feedback_prompt(review_output)
    review_output += f"\n\n{feedback_prompt}"

    # Wait for user response (non-blocking)
    # User can skip or provide feedback

    return review_output
```

### Step 6: Log Session

```python
def log_review_session(review_data, feedback_data, context_answers):
    """
    Append session data to review-sessions.jsonl
    """

    session = {
        "review_id": generate_uuid(),
        "timestamp": datetime.now().isoformat(),
        "design_type": review_data.get("type", "unknown"),
        "product_area": review_data.get("area", "unknown"),
        "5f_scores_original": review_data["scores"],
        "feedback": feedback_data,
        "context_learned": context_answers,
        "metadata": {
            "review_number": get_review_count() + 1,
            "learning_mode_shown": determine_modes_shown(review_data)
        }
    }

    # Append to JSONL
    append_jsonl("skill-memory/reviewing-designs-5f/feedback/review-sessions.jsonl", session)

    # Immediate high-confidence learning
    process_immediate_learnings(session)
```

### Step 7: Check Weekly Learning Trigger

```python
def check_weekly_learning_trigger():
    """
    Check if weekly learning cycle should run.
    """

    last_cycle = get_last_cycle_date()
    days_since_cycle = (datetime.now() - last_cycle).days

    if days_since_cycle >= 7:
        print("🔄 Weekly learning cycle triggered...")
        run_weekly_learning_cycle()
```

---

## Full Orchestrator Code

```python
def orchestrate_review_with_learning(design_input):
    """
    Main orchestrator function that wraps the original skill with learning.
    """

    print("📚 Loading learned context...")
    learned_context = load_learned_context()

    print("🎨 Running 5F design review...")
    review_output = run_original_review_skill(design_input, learned_context)

    print("🧪 Adding experimental observation (Mode A)...")
    review_output = append_mode_a_observation(review_output, learned_context, design_input)

    print("❓ Checking for context questions (Mode B)...")
    review_output = append_mode_b_questions(review_output, learned_context, design_input)

    print("📊 Collecting feedback...")
    review_output = collect_feedback(review_output, review_id=generate_uuid())

    # Display final review to user
    display_review(review_output)

    # Capture user responses (feedback + context answers)
    user_responses = capture_user_responses()

    if user_responses:
        print("💾 Logging review session...")
        log_review_session(
            review_data=extract_review_data(review_output),
            feedback_data=user_responses.get("feedback"),
            context_answers=user_responses.get("context_answers")
        )

    print("🔍 Checking for weekly learning trigger...")
    check_weekly_learning_trigger()

    print("✅ Review complete!")

    return review_output
```

---

## Usage

### For Users

**Normal review (with learning enabled):**
```bash
reviewing-designs-5f [design-file]
```

The orchestrator automatically runs in the background. User sees:
1. Main 5F review (original skill)
2. Learning observation (Mode A)
3. Optional context question (Mode B, if triggered)
4. Optional feedback prompt

**Disable learning for one review:**
```bash
SKIP_5F_LEARNING=true reviewing-designs-5f [design-file]
```

**Disable globally:**
```bash
# Add to CLAUDE.md or env
SKIP_5F_LEARNING=true
```

### For Developers

**Manual orchestration:**
```python
from orchestrator import orchestrate_review_with_learning

design_input = {
    "type": "dashboard",
    "url": "https://figma.com/...",
    "description": "Payment analytics dashboard"
}

orchestrate_review_with_learning(design_input)
```

---

## Key Design Principles

### 1. **Non-Invasive**
- Original `reviewing-designs-5f` skill is NEVER modified
- Learning happens in parallel, not inline
- User can disable learning entirely

### 2. **Transparent**
- All learning is visible (Mode A, Mode B, feedback prompts)
- User can see exactly what's being learned
- Improvement tracker shows all changes

### 3. **Optional**
- Feedback is always optional
- Context questions can be skipped
- User controls learning via commands

### 4. **Gradual**
- Starts with high question frequency (50% for reviews 1-5)
- Decreases as context builds (5% for reviews 21+)
- Learns faster early, stabilizes later

### 5. **Controllable**
- User can edit memory files directly
- User can reset learning entirely
- User can answer pending questions anytime

---

## Integration Points

```
Original Skill (reviewing-designs-5f)
            ↓
     [Orchestrator wraps it]
            ↓
┌───────────────────────────────┐
│   Enhanced Review Output      │
│                               │
│  1. Original Review ✓         │
│  2. + Mode A Observation      │
│  3. + Mode B Questions        │
│  4. + Feedback Prompt         │
└───────────────────────────────┘
            ↓
    [User engages/skips]
            ↓
┌───────────────────────────────┐
│   Learning Pipeline           │
│                               │
│  1. Log to review-sessions    │
│  2. Immediate context updates │
│  3. Weekly analysis (async)   │
│  4. Memory file updates       │
└───────────────────────────────┘
```

---

## No Modification Required

**Original skill stays intact:**
- `reviewing-designs-5f/SKILL.md` - Unchanged
- `reviewing-designs-5f/prompts/` - Unchanged
- `reviewing-designs-5f/logic/` - Unchanged

**Learning system is external:**
- Lives in `skill-memory/reviewing-designs-5f/`
- Wraps the original skill via orchestrator
- Can be enabled/disabled without touching original skill

---

This orchestrator is the **single entry point** that coordinates all learning workflows while keeping the original skill pristine.
