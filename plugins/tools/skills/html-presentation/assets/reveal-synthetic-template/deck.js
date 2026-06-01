const deckSpec = {
  title: "Reveal.js Synthetic Deck",
  subtitle: "A generated presentation scaffold",
  visualSystem: "black-stage-workshop",
  slides: [
    {
      type: "title",
      id: "start",
      eyebrow: "HTML presentation",
      title: "Reveal.js decks can be generated from structured content",
      body: ["Use this template when the deck has repeatable sections, variants, or data-driven slides."],
      notes: "Open with the reason this deck is generated instead of hand-authored."
    },
    {
      type: "claim",
      id: "mechanic",
      eyebrow: "Mechanic",
      title: "The renderer separates content, layout, and Reveal.js configuration",
      body: [
        "Content lives in deckSpec.",
        "Slide renderers own markup.",
        "Reveal.initialize owns runtime behavior."
      ],
      fragments: [1, 2],
      notes: "Step through the three layers and explain how this keeps variants manageable."
    },
    {
      type: "comparison",
      id: "choices",
      eyebrow: "Choice",
      title: "Pick the authoring mode by what will change",
      columns: [
        { title: "HTML", body: "Precise bespoke slides." },
        { title: "Markdown", body: "Fast text-heavy talks." },
        { title: "JavaScript", body: "Repeatable generated decks." }
      ],
      notes: "Make the tradeoff explicit before writing the deck."
    },
    {
      type: "code",
      id: "renderer-api",
      eyebrow: "Renderer API",
      title: "Slide renderers stay small and typed",
      language: "js",
      code: "function renderClaim(slide) {\\n  return section([\\n    eyebrow(slide),\\n    heading(slide.title),\\n    ...paragraphList(slide.body, slide.fragments)\\n  ]);\\n}",
      lineNumbers: "1-6|2|4",
      notes: "Highlight the function boundary first, then the data-driven body rendering."
    },
    {
      type: "metric",
      id: "quality-bar",
      eyebrow: "Quality bar",
      title: "A generated deck still needs handoff discipline",
      value: "7 checks",
      body: "Navigation, fragments, notes, assets, console, print route, and responsive fit.",
      notes: "A synthetic deck is not done until the runtime has been checked like a real web artifact."
    }
  ]
};

const configProfiles = {
  "standalone-talk": {
    width: 1920,
    height: 1080,
    margin: 0,
    hash: true,
    controls: true,
    progress: true,
    slideNumber: "c/t",
    center: false,
    transition: "slide",
    backgroundTransition: "fade",
    plugins: [RevealHighlight, RevealNotes]
  },
  "generated-report": {
    width: 1920,
    height: 1080,
    margin: 0,
    hash: true,
    controls: true,
    progress: true,
    slideNumber: "c/t",
    center: false,
    transition: "none",
    pdfSeparateFragments: false,
    plugins: [RevealHighlight, RevealNotes]
  }
};

const visualSystems = {
  "black-stage-workshop": {
    backgroundColor: "#030303"
  }
};

function slugify(value) {
  return String(value)
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);

  for (const [key, value] of Object.entries(attrs)) {
    if (value === undefined || value === null || value === false) continue;
    if (key === "className") node.className = value;
    else if (key === "dataset") Object.assign(node.dataset, value);
    else node.setAttribute(key, value === true ? "" : value);
  }

  for (const child of [].concat(children)) {
    if (child === undefined || child === null) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }

  return node;
}

function notes(text) {
  return text ? el("aside", { className: "notes" }, text) : null;
}

function paragraphList(items = [], fragmentIndexes = []) {
  return items.map((item, index) => {
    const attrs = fragmentIndexes.includes(index) ? { className: "fragment" } : {};
    return el("p", attrs, item);
  });
}

function applyCommon(section, slide) {
  section.id = slide.id || slugify(slide.title);
  const visualSystem = slide.visualSystem || deckSpec.visualSystem;
  if (visualSystem) section.classList.add(`theme-${visualSystem}`);
  if (slide.visibility) section.dataset.visibility = slide.visibility;
  const backgroundColor = slide.background?.color || visualSystems[visualSystem]?.backgroundColor;
  if (backgroundColor) section.dataset.backgroundColor = backgroundColor;
  if (slide.background?.image) section.dataset.backgroundImage = slide.background.image;
  if (slide.background?.gradient) section.dataset.backgroundGradient = slide.background.gradient;
  const noteNode = notes(slide.notes);
  if (noteNode) section.append(noteNode);
  return section;
}

function eyebrow(slide) {
  return slide.eyebrow ? el("div", { className: "eyebrow" }, slide.eyebrow) : null;
}

function renderTitle(slide) {
  const section = el("section", { className: "slide-title" }, [
    el("div", {}, [
      eyebrow(slide),
      el("h1", {}, slide.title),
      slide.subtitle ? el("p", { className: "subtitle" }, slide.subtitle) : null,
      ...paragraphList(slide.body)
    ])
  ]);
  return applyCommon(section, slide);
}

function renderClaim(slide) {
  const section = el("section", { className: "slide-claim" }, [
    eyebrow(slide),
    el("h2", {}, slide.title),
    ...paragraphList(slide.body, slide.fragments)
  ]);
  return applyCommon(section, slide);
}

function renderComparison(slide) {
  const cards = (slide.columns || []).map((column) =>
    el("div", { className: "panel" }, [
      el("h3", {}, column.title),
      el("p", {}, column.body)
    ])
  );
  const section = el("section", { className: "slide-comparison" }, [
    eyebrow(slide),
    el("h2", {}, slide.title),
    el("div", { className: "comparison-grid" }, cards)
  ]);
  return applyCommon(section, slide);
}

function mediaNode(media = {}) {
  if (!media.src) return el("div", { className: "media-frame muted" }, "Missing media source");
  if (media.type === "video") {
    return el("video", {
      src: media.src,
      controls: true,
      "data-autoplay": media.autoplay || undefined,
      muted: media.muted || undefined
    });
  }
  if (media.type === "iframe") {
    return el("iframe", {
      src: media.src,
      loading: "lazy",
      allowfullscreen: true,
      title: media.title || "Embedded content"
    });
  }
  return el("img", { src: media.src, alt: media.alt || "" });
}

function renderSplit(slide) {
  const visual = slide.code
    ? renderCodeBlock(slide)
    : el("div", { className: "media-frame" }, mediaNode(slide.media));
  const section = el("section", { className: "slide-split" }, [
    el("div", {}, [
      eyebrow(slide),
      el("h2", {}, slide.title),
      ...paragraphList(slide.body, slide.fragments)
    ]),
    visual
  ]);
  return applyCommon(section, slide);
}

function renderVisual(slide) {
  const section = el("section", { className: "slide-visual" }, [
    eyebrow(slide),
    el("h2", {}, slide.title),
    el("figure", {}, [
      mediaNode(slide.media),
      slide.caption ? el("figcaption", {}, slide.caption) : null
    ])
  ]);
  return applyCommon(section, slide);
}

function renderCodeBlock(slide) {
  const codeAttrs = {
    className: slide.language ? `language-${slide.language}` : undefined,
    "data-line-numbers": slide.lineNumbers || undefined,
    "data-trim": true
  };
  return el("pre", {}, el("code", codeAttrs, slide.code || ""));
}

function renderCode(slide) {
  const section = el("section", { className: "slide-code" }, [
    eyebrow(slide),
    el("h2", {}, slide.title),
    renderCodeBlock(slide)
  ]);
  return applyCommon(section, slide);
}

function renderMetric(slide) {
  const section = el("section", { className: "slide-metric" }, [
    eyebrow(slide),
    el("h2", {}, slide.title),
    el("span", { className: "metric-value" }, slide.value),
    el("p", {}, slide.body)
  ]);
  return applyCommon(section, slide);
}

function renderProcess(slide) {
  const steps = (slide.steps || []).map((step, index) =>
    el("li", slide.fragments?.includes(index) ? { className: "fragment" } : {}, step)
  );
  const section = el("section", { className: "slide-process" }, [
    eyebrow(slide),
    el("h2", {}, slide.title),
    el("ol", { className: "process-list" }, steps)
  ]);
  return applyCommon(section, slide);
}

function renderAppendix(slide) {
  const items = (slide.items || []).map((item) =>
    el("div", { className: "panel" }, [
      el("h3", {}, item.title),
      el("p", {}, item.body)
    ])
  );
  const section = el("section", { className: "slide-appendix" }, [
    eyebrow(slide),
    el("h2", {}, slide.title),
    el("div", { className: "appendix-grid" }, items)
  ]);
  slide.visibility ||= "uncounted";
  return applyCommon(section, slide);
}

const renderers = {
  title: renderTitle,
  claim: renderClaim,
  split: renderSplit,
  visual: renderVisual,
  code: renderCode,
  comparison: renderComparison,
  metric: renderMetric,
  process: renderProcess,
  appendix: renderAppendix
};

function validateDeck(spec) {
  const ids = new Set();
  for (const slide of spec.slides || []) {
    if (!slide.type || !renderers[slide.type]) throw new Error(`Unknown slide type: ${slide.type}`);
    if (!slide.title) throw new Error(`Slide ${slide.id || "(missing id)"} is missing a title`);
    const id = slide.id || slugify(slide.title);
    if (ids.has(id)) throw new Error(`Duplicate slide id: ${id}`);
    ids.add(id);
  }
}

function renderDeck(spec) {
  validateDeck(spec);
  document.title = spec.title || document.title;

  const slides = document.querySelector("#slides");
  slides.replaceChildren(...spec.slides.map((slide) => renderers[slide.type](slide)));
}

renderDeck(deckSpec);

Reveal.initialize(configProfiles["standalone-talk"]).then(() => {
  Reveal.sync();
  Reveal.layout();
});
