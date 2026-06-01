# Style Reference Library

Use this when the deck should feel designed, not templated. These patterns are extracted from the provided Figma references, screenshots, and Razorpay branding guide. Do not copy the source slides literally. Extract the mechanics and rebuild them for the user's content.

## Non-Negotiables

- Pick one deck-wide typography stack.
- Pick one deck-wide palette and surface model.
- Use Reveal.js full-viewport backgrounds, not a centered slide container with browser whitespace around it.
- Verify text contrast before handoff. If the deck is unreadable in a screenshot, the design has failed.
- Use style systems as modes, not random slide costumes. A deck can have a title mode and a content mode; it should not switch fonts and colors every slide.

## Source References

- L D Design Session template: graphic workshop deck with a blue technical title field, serif title block, blueprint lines, halftone texture, footer metadata, and high-contrast framed composition.
- FTX 2026 deck template: event deck with huge uppercase Space Grotesk headlines, pale atmospheric image fields, oversized background photography, thin footer rules, and minimal logo metadata.
- User screenshots: black-stage teaching decks with pill labels, white chips, colored symbols, hand-drawn path diagrams, dark process frames, mono annotations, pastel mats, and large centered claim slides.
- Razorpay brand PDF: blue/green brand tokens, Tasa Orbiter Display for headlines, Inter for body copy, clean candid imagery, 24x24 icons, and a 60/30/10 color usage split.

## Visual Systems

### 1. Black Stage Workshop

Use for design sessions, demos, product walkthroughs, and internal teaching.

Term -> meaning -> execution -> avoid

- **Black stage** -> the slide behaves like a dark canvas where content objects carry attention -> set slide background to near-black; put information in white or pastel chips, thin-line frames, or cropped product imagery -> full-slide gradients, decorative shadows, or low-contrast gray text.
- **Chunky agenda chips** -> each agenda item is a physical label, not a bullet -> blue number pill, white text pill, simple symbol block, 12-18px radius, uneven but deliberate horizontal offsets -> plain numbered list.
- **Diagram mess** -> complexity is shown as tangled process, then resolved -> draw thin white paths, small rounded labels, and one clean destination pill -> random squiggles without a before/after point.
- **Mono annotation** -> small operational labels feel like workshop marks -> uppercase mono captions, dotted leader lines, arrows, tiny step numbers -> big explanatory paragraphs near diagrams.

Best for: hands-on demos, how-we-work sections, relationship/workflow slides, concept-to-product stories.

### 2. Pale Mat With Dark Exhibit

Use when one diagram, screenshot, or process needs to feel like an object placed on a table.

Term -> meaning -> execution -> avoid

- **Pale mat** -> the page has an outer editorial surface that softens a dark inner diagram -> use pale green/blue/off-white body background and a rounded black exhibit panel -> black full-bleed for every slide.
- **Exhibit panel** -> the main visual is framed as the thing to inspect -> large dark rectangle with 8-12px radius, 1px border, inset labels, diagram centered inside -> small dark card floating in whitespace.
- **Caption claim** -> the takeaway sits outside the exhibit, usually below -> large sentence under the panel, centered or aligned to panel width -> burying the takeaway inside the diagram.

Best for: process maps, before/after diagrams, AI workflow explanations, systems stories.

### 3. Graphic Title System

Use for session openers and chapter breaks that need identity.

Term -> meaning -> execution -> avoid

- **Blueprint field** -> the background implies design, systems, and setup -> blue field, fine grid/linework, halftone/noise texture, subtle geometric arcs -> generic abstract gradient.
- **Serif display block** -> the title is a crafted object -> large italic serif inside a white rectangle, centered, with compact sans subtitle below -> stacking multiple display fonts.
- **Metadata footer** -> speaker/date/audience create event legitimacy -> small centered footer line, low opacity, fixed baseline -> oversized logos or noisy sponsor footers.

Best for: workshop title slides, design review openers, formal session starts.

### 4. Event Atmosphere

Use for external, executive, or launch decks where scale matters.

Term -> meaning -> execution -> avoid

- **Atmospheric field** -> background carries event energy without competing with the headline -> huge blurred or angled image, pale wash, low-detail area behind type -> busy photo directly behind text.
- **Huge uppercase claim** -> one message owns the slide -> 80-120px uppercase geometric sans, tight line height, dark navy or white depending on field -> three headline levels competing.
- **Footer rule** -> event branding is present but restrained -> thin horizontal rule, event mark left, company mark right, 24-40px margins -> logo cluster in the title area.

Best for: conference decks, keynote titles, big section breaks, executive summaries.

### 5. Product Split Explainer

Use for product behavior, integrations, or feature walkthroughs.

Term -> meaning -> execution -> avoid

- **Copy rail** -> the left side carries the argument -> small eyebrow, headline, compact benefit list, arrows or bullets as operators -> large body paragraphs.
- **Artifact rail** -> the right side shows the product evidence -> screenshot, Figma embed, browser capture, or code sample on colored block -> decorative mockups unrelated to the claim.
- **Color field** -> the screenshot side gets one strong color block -> lavender, blue, mint, or brand green side panel aligned to slide edge -> multiple unrelated background colors.

Best for: always-updated slides, integration value, product demos, code/design side-by-side.

### 6. Type And Symbol Bumper

Use between sections when the deck needs a breath.

Term -> meaning -> execution -> avoid

- **Word chips** -> words are composed from separate label blocks -> white/pastel pills with black text, plus one or two symbol tiles -> long sentence in one text box.
- **Symbol rhythm** -> icons act as punctuation -> simple vector shapes, same baseline, 1-2 accent colors -> illustrative icon packs with mixed stroke styles.
- **Dead-center lockup** -> one phrase sits in the exact visual center -> horizontal row, baseline aligned, large enough to read instantly -> centered paragraph blocks.

Best for: "Let's dive into..." moments, agenda transitions, demo starts.

### 7. Domain Cloud

Use when making a universal or ecosystem claim.

Term -> meaning -> execution -> avoid

- **Orbit field** -> surrounding topics imply breadth -> thin circles around the slide, low-opacity labels, center claim in high contrast -> bubble chart pretending to show data.
- **One accented word** -> the core claim gets one colored emphasis -> white sentence with one purple/green/blue word -> rainbow text emphasis.
- **Peripheral fade** -> supporting topics are intentionally secondary -> 10-25% opacity, clipped by slide edges -> fully legible clutter around the claim.

Best for: "design is everywhere" claims, ecosystem maps, broad category framing.

## Composition Rules

- Build slides from objects: chips, fields, frames, rails, labels, symbols, paths, screenshots. Avoid generic cards unless the content is a repeated item set.
- Use one dominant surface per slide: black stage, pale mat, blue field, atmospheric image, or product split. Do not stack all of them.
- Keep the deck foundations consistent. Surface type may change for a section break, but typography, logo behavior, and contrast rules should not reset every slide.
- Treat diagrams as scenes. Place labels near the object they explain; use leader lines when distance is necessary.
- Use deliberate asymmetry. Offset chips and diagrams when it creates hierarchy; keep baselines and spacing consistent enough that it does not look accidental.
- Put claims where the audience reads first. For most decks: title top-left, exhibit center, takeaway bottom. For bumpers: exact center.

## Palette Recipes

### Black Stage Candy

- Background: `#030303`, `#101010`
- Text: `#f7f7f2`
- Primary chip: `#4b42ff`
- Mint: `#eaffdc`
- Green: `#56f56f`
- Lavender: `#c99bd4`
- Coral: `#ff4438`
- Cyan: `#bff5ff`

Use for internal design/workshop decks. The effect comes from high contrast and chunky shapes, not from gradients.

### Razorpay Brand Native

- Backgrounds: `#ffffff`, `#f8fafc`, `#edf7f7`, `#0c1927`
- Brand blue: `#305eff`, `#5278ff`, logo light blue `#3395ff`
- Navy: `#0c2651`
- Green: `#6ed00b`, `#c1ff84`, `#00be5f`
- Secondary depth: `#389494`, `#387594`
- Accent: `#ff8a80`, `#826dff`, `#fbec51`, `#7dd5e9`

Use when the deck should feel Razorpay-owned. Keep the 60/30/10 split: primary brand colors dominate, secondary colors support, tertiary colors punctuate.

### FTX Atmosphere

- Background: pale blue-white wash
- Text: deep navy
- Accent: subtle blue glow or motion-blur image
- Structure: footer rule and minimal marks

Use for event scale and keynote presence. The slide should feel spacious, not busy.

## Type Recipes

- **Razorpay brand deck**: Tasa Orbiter Display for headlines, Inter for body, monospace only for technical annotations.
- **Workshop black-stage deck**: Inter or Space Grotesk for big sans text, a condensed mono for labels, occasional expressive symbol blocks.
- **Graphic session opener**: Instrument Serif Italic or another high-contrast italic display face for the title, Inter for metadata.
- **Event deck**: Space Grotesk uppercase for the main claim, Inter for footer and small metadata.

If a font is not available, use CSS fallbacks and state the substitution. Do not install fonts without asking unless the project already manages font assets.

## Motion Recipes

- Chip agenda: each row appears as number chip -> symbol -> label.
- Tangled process: show mess first, then fade in the clean product destination.
- Exhibit slide: keep panel static; reveal annotations one at a time.
- Product split: fade text rail first, then slide/fade artifact rail.
- Domain cloud: no per-bubble animation unless the talk explains clusters.
- Event title: no fragment animation; use a single slide transition.

Motion should change what the viewer knows. If it only makes the deck feel busy, remove it.
