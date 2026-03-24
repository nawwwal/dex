# Mode B: Context-Triggered Questions

**Purpose:** Ask targeted questions when skill is genuinely uncertain about how to score something.

---

## When to Run

- **Trigger:** When uncertainty is detected during review analysis
- **Frequency:**
  - Reviews 1-5: 50% trigger rate
  - Reviews 6-20: 20% trigger rate
  - Reviews 21+: 5% trigger rate
- **Placement:** End of main review, before feedback collection
- **Max questions:** 2 per review

---

## Trigger Detection Logic

### Before generating review scores:

```python
def detect_uncertainties(design_analysis):
    uncertainties = []

    # Load current context
    context = load_context_files()

    # Check for gaps
    if design_has_high_density(design_analysis) and not context.user_personas:
        uncertainties.append({
            "category": "user_personas",
            "trigger": "high_information_density",
            "impacts_dimension": "Focused",
            "priority": "high"
        })

    if design_has_forms(design_analysis) and not context.compliance_rules:
        uncertainties.append({
            "category": "regulatory_context",
            "trigger": "form_fields_detected",
            "impacts_dimension": "Fair",
            "priority": "medium"
        })

    # ... check all 10 trigger categories

    return uncertainties
```

### Trigger Categories (10 total)

| Trigger | Detection | Impacts | Priority |
|---------|-----------|---------|----------|
| **High info density** | >15 UI elements | Focused | High |
| **Form fields** | PAN/GST/Aadhaar inputs | Fair | High |
| **Heavy media** | Images >500kb, animations | Fast | Medium |
| **Upgrade prompts** | Paywall/upgrade UI | Fun | Low |
| **Novel pattern** | Deviation from common B2B patterns | Fluent | Medium |
| **Multi-step flow** | >3 steps | Fast & Fluent | High |
| **Pattern inconsistency** | Multiple styles on one screen | All | Medium |
| **Text-heavy UI** | Long labels, paragraphs | Focused | Low |
| **Accessibility gaps** | Contrast <4.5:1, no keyboard nav | Fair | Medium |
| **Mobile issues** | Hover states, small targets | Fast & Fluent | Medium |

---

## Question Templates

### Category 1: User Personas

**Trigger:** High information density (>15 fields) AND `context/user-personas.md` is empty

```markdown
---
## ❓ Quick Context Question (15 seconds - helps me score accurately)

I'm seeing **[N] data fields** on this screen. To give you an accurate **"Focused"** score:

**Your primary users are:**
- [ ] Data analysts (comfortable with dense tables, multiple filters)
- [ ] Business managers (need simplified views, key metrics only)
- [ ] Operations staff (task-focused, need quick actions)
- [ ] Mixed audience (need progressive disclosure)

**Why I'm asking:** This determines if [N] fields is "focused" or "overwhelming" for your users.

**What happens next:**
- Your answer updates `context/user-personas.md`
- All future "Focused" scores will use this context
- You can change this anytime by editing the context file

[Skip for Now] [Answer: ___________]
```

### Category 2: Regulatory Context

**Trigger:** Form collecting PAN/GST/Aadhaar AND `context/business-rules.md` has no compliance rules

```markdown
---
## ❓ Quick Context Question (helps flag compliance issues)

I see you're collecting **[PAN/GST/Aadhaar]** data. To check **"Fair"** (transparency & trust):

**Your regulatory context:**
- [ ] RBI-regulated (need explicit consent flows, security indicators)
- [ ] PCI DSS compliant (need secure data handling patterns)
- [ ] GDPR-compliant (need data processing notices)
- [ ] Standard Indian business (privacy policy sufficient)

**Why I'm asking:** Different regulations require different UI patterns for trust and transparency.

**What happens next:**
- I'll check for required compliance patterns in this and future reviews
- Added to `context/business-rules.md`

[Skip for Now] [Answer: ___________]
```

### Category 3: Performance Context

**Trigger:** Heavy media (images >500kb, animations) AND `context/user-personas.md` has no environment data

```markdown
---
## ❓ Quick Context Question (helps set performance expectations)

This design has **[images/animations/heavy content]**. To score **"Fast"**:

**Your users' typical environment:**
- [ ] Metro cities, WiFi/4G (can handle rich media)
- [ ] Tier 2/3 cities, 3G (need lightweight designs)
- [ ] Mixed (must work on lowest common denominator)
- [ ] Desktop-only (network not a constraint)

**Current performance:** [X]s load time

**Why I'm asking:** This sets the performance threshold for "Fast" scoring.

[Skip for Now] [Answer: ___________]
```

### Category 4: Business Model

**Trigger:** Upgrade prompts/paywalls AND `context/product-specifics.md` is empty

```markdown
---
## ❓ Quick Context Question (calibrates growth tactics tolerance)

I see **[upgrade prompts/paywalls]** in [N] places. To evaluate **"Fun"** (not annoying):

**Your growth stage:**
- [ ] Early-stage (aggressive growth > experience)
- [ ] Product-market fit (balanced approach)
- [ ] Mature (retention > acquisition, minimize friction)

**Your pricing model:**
- [ ] Freemium (need to drive conversions)
- [ ] Free trial (gentle nudges)
- [ ] Paid-only (no upgrade prompts needed)

**Why I'm asking:** Different stages have different acceptable friction levels.

[Skip for Now] [Answer: ___________]
```

### Category 5: Competitive Benchmark

**Trigger:** Novel UI pattern (e.g., bottom sheet on desktop) AND `context/competitive-context.md` is empty

```markdown
---
## ❓ Quick Context Question (innovation vs. confusion)

You're using **[novel pattern]** (uncommon for B2B desktop apps).

**Your competitive set:**
- [ ] Traditional tools (Tally, Zoho) - users expect standard patterns
- [ ] Modern SaaS (Notion, Airtable) - users embrace innovation
- [ ] Internal tools (no external benchmarks)

**User feedback on new patterns:**
- [ ] Users love when we innovate
- [ ] Users prefer familiar patterns
- [ ] We haven't tested this yet

**Why I'm asking:** Helps me distinguish intentional innovation from potential confusion.

[Skip for Now] [Answer: ___________]
```

### Category 6: Critical Flow Context

**Trigger:** Multi-step flow (>3 steps) AND `context/product-specifics.md` has no flow frequency data

```markdown
---
## ❓ Quick Context Question (prioritizes friction points)

I see a **[N]-step flow**. To prioritize **"Fast"** vs **"Fluent"**:

**This flow is:**
- [ ] One-time (e.g., onboarding) - can be longer for completeness
- [ ] Repeated weekly - every step is friction
- [ ] Repeated daily - must be very fast
- [ ] Optional (most users skip anyway)

**Drop-off data (if you have it):**
- [ ] We lose >40% at step [N] (urgent)
- [ ] Completion rate is acceptable
- [ ] We don't have data yet

**Why I'm asking:** Determines which friction points to flag as critical.

[Skip for Now] [Answer: ___________]
```

### Category 7: Design System Maturity

**Trigger:** Inconsistent patterns (3+ button styles) AND `context/design-system.md` is empty

```markdown
---
## ❓ Quick Context Question (sets consistency expectations)

I'm seeing **[N] different button/component styles** on this screen.

**Your design system:**
- [ ] Mature & documented (flag all deviations)
- [ ] Evolving (some inconsistency expected)
- [ ] No formal system (don't nitpick variations)

**Design system location (if exists):**
[Link to Figma/Storybook/docs]

**Why I'm asking:** Sets my threshold for consistency criticism.

[Skip for Now] [Answer: ___________]
```

### Category 8: Localization Context

**Trigger:** Text-heavy UI with long English labels AND `context/product-specifics.md` has no i18n data

```markdown
---
## ❓ Quick Context Question (flags localization risks)

I see long text labels that might break in translation.

**Your language support:**
- [ ] English-only (no localization concerns)
- [ ] Hindi + English (need shorter labels)
- [ ] Multi-language planned (need flexible layouts)

**User base:**
- [ ] English-fluent metros
- [ ] Mixed English proficiency
- [ ] Regional languages coming soon

**Why I'm asking:** Flags layout/text length risks early.

[Skip for Now] [Answer: ___________]
```

### Category 9: Accessibility Priority

**Trigger:** Contrast failures OR keyboard nav gaps AND `context/product-specifics.md` has no WCAG data

```markdown
---
## ❓ Quick Context Question (sets accessibility severity)

I found **[N] contrast ratio failures** (WCAG AA).

**Your accessibility stance:**
- [ ] WCAG AA mandatory (flag all violations as critical)
- [ ] WCAG AA aspirational (note for backlog)
- [ ] No formal requirement (low priority)

**User base includes:**
- [ ] Government/enterprise (accessibility required for procurement)
- [ ] General SMBs (nice-to-have)
- [ ] Internal tool (know our users' specific needs)

**Why I'm asking:** Determines severity of accessibility issues.

[Skip for Now] [Answer: ___________]
```

### Category 10: Mobile Strategy

**Trigger:** Hover states OR small touch targets (<44px) AND `context/product-specifics.md` has no mobile data

```markdown
---
## ❓ Quick Context Question (mobile usability importance)

This design uses **[hover states / small touch targets]**.

**Your mobile strategy:**
- [ ] Desktop-first (mobile <10% traffic)
- [ ] Responsive (must work on both)
- [ ] Mobile-first (desktop secondary)
- [ ] Desktop-only (no mobile needed)

**Current mobile traffic:** [___]%

**Why I'm asking:** Determines if I should flag mobile usability issues.

[Skip for Now] [Answer: ___________]
```

---

## Smart Suppression Rules

```python
def should_show_question(uncertainty, context):
    # Rule 1: Never ask same question twice
    if uncertainty.category in context.answered_questions:
        return False

    # Rule 2: Skip if context file already has answer
    if context.has_data_for(uncertainty.category):
        return False

    # Rule 3: Respect frequency limits
    review_count = get_review_count()
    if review_count <= 5:
        trigger_rate = 0.5  # 50%
    elif review_count <= 20:
        trigger_rate = 0.2  # 20%
    else:
        trigger_rate = 0.05  # 5%

    if random() > trigger_rate:
        return False

    # Rule 4: Max 2 questions per review
    if questions_shown_this_review >= 2:
        return False

    # Rule 5: Prioritize high-impact uncertainties
    # Only show medium/low priority if no high priority exists

    return True
```

---

## Handling Responses

### User Answers

```python
def handle_answer(question_category, answer):
    # Update appropriate context file
    if question_category == "user_personas":
        update_file("context/user-personas.md", {
            "primary_users": answer,
            "source": "context_question",
            "confidence": "high",
            "date": today()
        })

        # Summarize in LEARNINGS.md
        update_learnings_summary()

    # Mark as answered (never ask again)
    mark_answered(question_category)

    # Remove from pending questions
    remove_from_pending(question_category)
```

### User Skips

```python
def handle_skip(question_category, question_text):
    # Add to pending questions
    add_to_file("experiments/pending-questions.md", {
        "id": generate_id(),
        "category": question_category,
        "question": question_text,
        "asked_during": current_review_id,
        "priority": calculate_priority(),
        "date": today()
    })

    # User can answer later via /context-5f answer
```

---

## Implementation

**As part of review workflow:**

1. **Before generating scores:** Detect uncertainties
2. **Generate main review:** Use default thresholds where uncertain
3. **After main review:** Show 0-2 context questions (if triggered)
4. **Capture answers:** Update context files immediately
5. **Re-score (optional):** If answer changes scoring significantly, offer updated scores

**No modification to original skill required** - questions appear as post-review prompts.
