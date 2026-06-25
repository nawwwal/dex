const doc = document.documentElement;
const sections = [...document.querySelectorAll(".brief-section[id]")];
const switcher = document.querySelector(".section-switcher");
const current = document.querySelector(".section-current");
const list = document.querySelector(".section-list");

function hexToRgb(hex) {
  const value = hex.replace("#", "").trim();
  const full = value.length === 3 ? value.split("").map((c) => c + c).join("") : value;
  const number = Number.parseInt(full, 16);
  return {
    r: (number >> 16) & 255,
    g: (number >> 8) & 255,
    b: number & 255
  };
}

function luminance({ r, g, b }) {
  const convert = (channel) => {
    const c = channel / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * convert(r) + 0.7152 * convert(g) + 0.0722 * convert(b);
}

function mix(a, b, amount) {
  return {
    r: Math.round(a.r + (b.r - a.r) * amount),
    g: Math.round(a.g + (b.g - a.g) * amount),
    b: Math.round(a.b + (b.b - a.b) * amount)
  };
}

function rgb({ r, g, b }) {
  return `rgb(${r} ${g} ${b})`;
}

function applyTheme() {
  const bg = hexToRgb(doc.dataset.bg || "#101010");
  const dark = luminance(bg) < 0.42;
  const fg = dark ? { r: 244, g: 241, b: 235 } : { r: 22, g: 21, b: 20 };
  const muted = mix(fg, bg, dark ? 0.42 : 0.38);
  const panel = mix(bg, fg, dark ? 0.06 : 0.08);
  const border = mix(bg, fg, dark ? 0.22 : 0.18);

  doc.style.setProperty("--brief-bg", rgb(bg));
  doc.style.setProperty("--brief-fg", rgb(fg));
  doc.style.setProperty("--brief-muted", rgb(muted));
  doc.style.setProperty("--brief-panel", rgb(panel));
  doc.style.setProperty("--brief-border", rgb(border));
  doc.style.setProperty("--brief-link", rgb(fg));
}

function buildSwitcher() {
  list.replaceChildren(
    ...sections.map((section, index) => {
      const label = section.dataset.sectionTitle || section.querySelector("h2")?.textContent || `Section ${index + 1}`;
      const link = document.createElement("a");
      link.href = `#${section.id}`;
      link.textContent = `${index + 1} - ${label}`;
      return link;
    })
  );
}

function updateCurrent() {
  const active = sections.reduce((candidate, section) => {
    const top = section.getBoundingClientRect().top;
    return top < window.innerHeight * 0.45 ? section : candidate;
  }, sections[0]);
  const index = sections.indexOf(active);
  const label = active?.dataset.sectionTitle || active?.querySelector("h2")?.textContent || "Section";
  current.textContent = `${index + 1} - ${label}`;
}

applyTheme();
buildSwitcher();
updateCurrent();

current.addEventListener("click", () => {
  const expanded = switcher.classList.toggle("is-open");
  current.setAttribute("aria-expanded", String(expanded));
});

switcher.addEventListener("pointerenter", () => {
  switcher.classList.add("is-hovered");
});

switcher.addEventListener("pointerleave", () => {
  switcher.classList.remove("is-hovered");
});

switcher.addEventListener("focusin", () => {
  switcher.classList.add("is-hovered");
});

switcher.addEventListener("focusout", () => {
  window.setTimeout(() => {
    if (!switcher.contains(document.activeElement)) switcher.classList.remove("is-hovered");
  }, 0);
});

window.addEventListener("scroll", updateCurrent, { passive: true });
