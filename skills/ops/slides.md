# HTML Presentation Generator

Creates animation-rich HTML presentations from scratch or by converting PPT/PPTX.

## Mode A: Create from Scratch

Step 1: Ask the user to describe the talk/presentation:
- Topic and audience
- How many slides (aim for 15 or fewer)
- Key points to cover
- Aesthetic preference (show 3 options visually) — if thumbnail previews would help
  the user choose, invoke `/generate-image` for each theme before writing any HTML:
  > `/generate-image` — prompt: "[theme name] presentation aesthetic, [mood keywords]" — aspect-ratio: 16:9

Step 2: Generate structure first (slide titles + 1-line summary each)
Get approval before generating full HTML.

Step 3: Generate complete single-file HTML presentation.
If the presentation needs a cover image or section illustrations, invoke `/generate-image`
and embed the result as a base64 data URI in the HTML:
> `/generate-image` — prompt: "minimalist [theme] hero image for a presentation titled '[title]'" — aspect-ratio: 16:9
- Keyboard navigation (arrows, space)
- Progress indicator
- Speaker notes (press N to toggle)
- Smooth slide transitions
- Mobile responsive

## Mode B: Convert PPT/PPTX

Step 1: Read the file path provided
Step 2: Extract content using python3:
```bash
python3 -c "
import pptx
from pptx import Presentation
prs = Presentation('INPUT.pptx')
for i, slide in enumerate(prs.slides):
    print(f'=== SLIDE {i+1} ===')
    for shape in slide.shapes:
        if hasattr(shape, 'text'): print(shape.text)
"
```
Step 3: Convert extracted content to styled HTML presentation.

## Slide Template
```html
<!DOCTYPE html>
<html>
<head>
<style>
.slide { min-height: 100vh; padding: 4rem; display: none; animation: fadeIn 0.3s ease; }
.slide.active { display: flex; flex-direction: column; justify-content: center; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; } }
.progress { position: fixed; bottom: 0; height: 3px; background: var(--accent); transition: width 0.3s; }
</style>
</head>
<body>
<!-- Slides go here -->
<script>
let current = 0;
const slides = document.querySelectorAll('.slide');
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ') next();
  if (e.key === 'ArrowLeft') prev();
});
function show(n) { slides.forEach(s => s.classList.remove('active')); slides[n].classList.add('active'); }
function next() { current = Math.min(current + 1, slides.length - 1); show(current); }
function prev() { current = Math.max(current - 1, 0); show(current); }
show(0);
</script>
</body>
</html>
```
