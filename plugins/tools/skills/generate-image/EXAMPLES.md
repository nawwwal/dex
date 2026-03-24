# generate-image — Cross-Skill Usage Examples

How to call this skill from another skill's SKILL.md.

---

## Option A — Slash command (natural language, Claude-driven)

Add to your skill's SKILL.md:

```
If image generation is needed at any step, invoke /generate-image with the prompt
and any required params (aspect ratio, size, model). Claude will read the skill
and generate the image.
```

Best when: the prompt needs contextual refinement, multi-turn editing, or Claude
needs to make decisions about params based on prior conversation.

---

## Option B — Bash script (deterministic, structured output)

Add to your skill's SKILL.md (copy and adjust):

```bash
python ~/.claude/skills/generate-image/scripts/generate.py \
  --prompt "{your_prompt_here}" \
  --aspect-ratio 16:9 \
  --size 2K \
  --output ./output.png
```

Parse JSON from stdout:

```python
import json, subprocess
result = subprocess.run([...], capture_output=True, text=True)
data = json.loads(result.stdout)
# data["path"]  — saved file path
# data["text"]  — text response (if TEXT,IMAGE modalities used)
# data["model"] — model used
# data["usage"] — token counts
```

If exit code is non-zero, check stderr for the error message.

---

## Option C — Image editing (source image required)

```bash
python ~/.claude/skills/generate-image/scripts/generate.py \
  --prompt "Make the background white and add a drop shadow" \
  --input-image ./source.png \
  --output ./edited.png
```

Source image must be: png, jpg, webp, heic, or heif.

---

## Option D — Higher quality (user explicitly asked for pro)

```bash
python ~/.claude/skills/generate-image/scripts/generate.py \
  --model gemini-3-pro-image-preview \
  --prompt "{your_prompt_here}" \
  --aspect-ratio 4:5 \
  --size 2K \
  --output ./output.png
```

Only use this when the user explicitly requests higher quality or "pro".
Default (Flash) is preferred for speed and cost.

---

## Option E — With text response alongside image

```bash
python ~/.claude/skills/generate-image/scripts/generate.py \
  --prompt "Generate an infographic about photosynthesis" \
  --modalities TEXT,IMAGE \
  --aspect-ratio 9:16 \
  --size 2K \
  --output ./infographic.png
```

The `text` field in the JSON output will contain the model's text explanation.

---

## Option F — With thinking (complex prompts)

```bash
python ~/.claude/skills/generate-image/scripts/generate.py \
  --prompt "A logo for a fintech startup that conveys trust and speed" \
  --thinking High \
  --modalities TEXT,IMAGE \
  --output ./logo.png
```

Use `--thinking High` for prompts requiring multi-element composition,
style matching, or creative reasoning. Slower but higher quality.
