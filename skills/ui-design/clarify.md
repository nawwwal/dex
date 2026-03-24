# Clarify — UX Copy Improvements

Fix confusing interface text to be clear, specific, and actionable.

## Rules (all modes — copy is design-system-agnostic)

### Error messages
- ❌ "An error occurred." → ✅ "Couldn't save changes. Check your connection and try again."
- ❌ "Invalid input." → ✅ "Account number must be 9–18 digits."
- Always include: what went wrong + what to do next

### Form labels
- ❌ Generic placeholder: "Enter value" → ✅ Specific: "Enter IFSC code"
- ❌ "Name" label → ✅ "Business name (as registered)"
- Labels should live ABOVE the input, not only as placeholder text (placeholder disappears on focus)

### Buttons and CTAs
- ❌ "Submit" → ✅ "Save payment details"
- ❌ "OK" → ✅ "Got it, close" or "Yes, delete"
- ❌ "Cancel" alone → ✅ "Cancel", paired with what you're cancelling ("Cancel refund")
- Buttons should say what happens, not just confirm

### Empty states
- ❌ Blank screen → ✅ Purposeful empty state with: what this section is for + how to get started + primary CTA
- ❌ "No data found." → ✅ "No transactions yet. Once you receive a payment, it'll appear here." + "View test transactions" link

### Loading and success states
- ❌ "Loading..." → ✅ "Fetching your settlements..."
- ❌ "Done." → ✅ "Payment of ₹1,500 sent to the user's HDFC account"

### Navigation labels
- ❌ Generic "Settings" → ✅ "Payment settings"
- ❌ "Details" → ✅ "Transaction details"
- Labels should explain the destination, not just name a category

## Output

```
## Clarify: {TARGET}

### Changes made
- [file:line] — "Submit" → "Save bank details"
- [file:line] — "Error occurred" → "Couldn't load settlements. Refresh to try again."
- [file:line] — Empty state: added heading + CTA

### Couldn't clarify (needs product context)
- [file:line] — "Process payment" — unclear what "process" means; ask PM
```
