# Mode A: Experimental Observations

**Purpose:** Inject 5% learning content into review output to surface hypotheses being tested.

---

## When to Run

- **Trigger:** Every review
- **Placement:** End of main review output (separate section)
- **Size:** 3-5 sentences
- **Blocking:** No (user can ignore)

---

## How It Works

### Step 1: Check Active Hypotheses

Load `experiments/active-hypotheses.md` and select:
- **Priority 1:** Hypothesis relevant to current design (e.g., if reviewing dashboard, show table vs. card hypothesis)
- **Priority 2:** Oldest hypothesis with fewest data points
- **Priority 3:** Random hypothesis from active list

### Step 2: Generate Observation

Template:
```markdown
---
## 🧪 Learning Mode (experimental observation)

**Hypothesis I'm testing:**
"[Hypothesis statement from active-hypotheses.md]"

**Observation from this design:**
[Specific observation about current design that relates to hypothesis]

**Context:**
[Brief competitive/industry context if relevant]

**Quick validation:**
Does this match your intentional pattern?
- ✅ Yes, this is our standard
- ❌ No, this is a deviation/experiment
- 🤷 Unsure, we should test

[This helps me learn when to flag pattern deviations vs. recognize intentional innovation]
```

### Step 3: Capture Response

If user responds:
- **Yes** → Add data point to hypothesis (confirmation)
- **No** → Add data point to hypothesis (contradiction)
- **Unsure** → Add data point as neutral
- **No response** → Don't count as data point

Update `experiments/active-hypotheses.md`:
```markdown
### H001: Users prefer table layouts for financial data
- Data Points Collected: 4/10 → 5/10
- Confidence: 75% → 80% (4 confirmations, 1 contradiction)
- Evidence:
  - ...previous evidence...
  - Review #16: User confirmed tables are standard pattern ✅
```

### Step 4: Check for Promotion

If hypothesis reaches **10 data points AND 70% confidence**:
- Auto-promote to business rule
- Add to `context/design-system.md` or `context/business-rules.md`
- Summarize in `LEARNINGS.md`
- Archive hypothesis as validated

---

## Example Output

```markdown
---
## 🧪 Learning Mode (experimental observation)

**Hypothesis I'm testing:**
"Indian B2B SaaS users prefer table layouts over card grids for financial transaction data"

**Observation from this design:**
You're using a **table layout** for transaction history. This matches patterns I've seen in 7 of your last 9 dashboard reviews.

**Context:**
Your competitors (Tally, Zoho Books) predominantly use dense table layouts for financial data. Card grids are more common in modern SaaS tools like Notion or Airtable.

**Quick validation:**
Is table layout your standard pattern for financial data?
- ✅ Yes, tables are our standard
- ❌ No, we're experimenting with different layouts
- 🤷 We haven't standardized this yet

💡 *Why I ask: Once I validate this pattern (need 3 more confirmations), I'll automatically flag card layouts as potential UX risks in future reviews.*
```

---

## Hypothesis Generation

New hypotheses are created from:
1. **Pattern observations** - When same pattern appears 3+ times across reviews
2. **User feedback** - When user mentions "this should be our standard"
3. **Competitive patterns** - When design deviates from known competitor patterns

**Auto-generated hypothesis example:**
```markdown
After Review #3: User used tables in all 3 reviews
→ Create H001: "User prefers table layouts for financial data"
→ Add to active-hypotheses.md
→ Start surfacing in Mode A for validation
```

---

## Implementation

**As part of review output:**
1. Main review runs normally (original skill, untouched)
2. **After main review**, append Mode A section
3. Section is clearly marked as "Learning Mode"
4. User can engage or ignore

**No modification to original skill required.**
