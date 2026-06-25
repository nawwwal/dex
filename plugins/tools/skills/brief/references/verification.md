# Verification

Before handoff:

1. Validate the eval JSON when changing skill tests.
2. Run the brief eval validator.
3. Run JavaScript syntax checks for the template and contrast helper.
4. Run contrast checks for at least one dark and one light theme pair.
5. Serve the template or generated brief locally when possible.
6. Check desktop and mobile widths.
7. Confirm section switcher expands on hover/focus and scrolls to sections.
8. Confirm all image assets resolve.
9. Confirm no empty image slots, image prompts, or placeholder image copy remain.
10. Confirm print CSS hides floating controls and keeps content readable.

If any visual generation failed, remove broken image beats from the final artifact and mention that images were omitted because generation was unavailable.
