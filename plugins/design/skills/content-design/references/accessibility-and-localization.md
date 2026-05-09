# Accessibility and Localization

Use this file to make copy usable when read by assistive technology, translated, truncated, or encountered outside the visual layout.

## Accessibility rules

- Link text must describe the destination out of context.
- Button text must describe the action.
- Icon-only controls need labels that describe action or state, not the icon shape.
- Accessibility hints must not contain essential information because users may turn hints off.
- Critical instructions must remain visible; do not put them only in tooltips, placeholders, toasts, or hover states.
- Error messages should be close to the field or state they explain.
- Status changes that affect task completion must be announced or persisted in the UI.

## Alt text

Formula: meaning or action, not visual format.

Use:

- Search payments
- Download settlement report
- Payment success illustration, if the image conveys success
- QR code for payment link

Avoid:

- Image of search icon
- Screenshot
- Beautiful dashboard illustration
- IMG_2024.png

If the image is decorative, use empty alt text.

## Tooltips, placeholders, and toasts

Do not place essential content in disappearing or optional surfaces.

- Placeholder text disappears when the user types.
- Tooltips are optional help, not required reading.
- Toasts disappear and should not carry KYC rejection reasons, settlement failure details, account suspension, legal terms, or critical recovery steps.

Move critical copy into inline validation, persistent banners, modal body, or page-level status.

## Localization rules

Write for translation before translation starts.

Avoid:

- Idioms, puns, slang, and cultural jokes.
- Sentence fragments that cannot be reordered in other languages.
- Variables embedded in grammar that may break agreement or word order.
- "Just", "simply", "only", and "easy" for tasks that may not be easy.
- Emojis as meaning carriers.
- Repeated "learn more" links that lose context.

Use:

- Complete, direct sentences for body copy.
- Stable product nouns.
- Named variables with context: amount, date, bank account, payment ID, settlement ID.
- Numerals for amounts, limits, dates, counts, and durations.
- "Working days" for bank and compliance timelines.

## Screen-reader checks

Ask:

- Can a user understand this link without surrounding text?
- Can a user complete the flow without seeing placeholder text?
- Does an icon label describe the action?
- Does the error identify the field or object?
- Is critical state still available after a toast disappears?

