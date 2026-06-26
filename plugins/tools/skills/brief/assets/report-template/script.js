const doc = document.documentElement;
const sections = [...document.querySelectorAll(".brief-section[id]")];
const switcher = document.querySelector(".section-switcher");
const current = document.querySelector(".section-current");
const list = document.querySelector(".section-list");
let selectedSection = null;
let selectionLockUntil = 0;
let wheelDelta = 0;
let wheelGestureLocked = false;
let wheelGestureUnlockTimer = null;

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
  const wheel = document.createElement("div");
  wheel.className = "section-wheel";
  wheel.replaceChildren(
    ...sections.map((section, index) => {
      const label = section.dataset.sectionTitle || section.querySelector("h2")?.textContent || `Section ${index + 1}`;
      const link = document.createElement("a");
      const labelText = document.createElement("span");
      link.href = `#${section.id}`;
      labelText.className = "section-label";
      labelText.textContent = `${index + 1} - ${label}`;
      link.append(labelText);
      link.dataset.sectionId = section.id;
      link.addEventListener("click", () => {
        selectedSection = section;
        selectionLockUntil = performance.now() + 900;
        setCurrent(section);
      });
      return link;
    })
  );
  list.replaceChildren(wheel);
}

function setCurrent(active) {
  const index = sections.indexOf(active);
  const label = active?.dataset.sectionTitle || active?.querySelector("h2")?.textContent || "Section";
  current.textContent = `${index + 1} - ${label}`;
  switcher.style.setProperty("--active-index", index);
  switcher.style.setProperty("--section-count", sections.length);
  list.querySelectorAll("a").forEach((link) => {
    if (link.dataset.sectionId === active.id) {
      link.setAttribute("aria-current", "true");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

function updateCurrent() {
  if (selectedSection && performance.now() < selectionLockUntil) {
    setCurrent(selectedSection);
    return;
  }

  selectedSection = null;
  const scroller = document.scrollingElement || doc;
  const atBottom = window.scrollY + window.innerHeight >= scroller.scrollHeight - 32;
  const activationLine = 120;
  const active = atBottom
    ? sections[sections.length - 1]
    : sections.reduce((candidate, section) => {
        const top = section.getBoundingClientRect().top;
        return top <= activationLine ? section : candidate;
      }, sections[0]);
  setCurrent(active);
}

function stepCurrent(direction) {
  const currentLink = list.querySelector('a[aria-current="true"]');
  const currentIndex = sections.findIndex((section) => section.id === currentLink?.dataset.sectionId);
  const nextIndex = Math.min(Math.max(currentIndex + direction, 0), sections.length - 1);
  if (nextIndex === currentIndex) return;

  selectedSection = sections[nextIndex];
  selectionLockUntil = performance.now() + 900;
  setCurrent(selectedSection);
  selectedSection.scrollIntoView({ behavior: "smooth", block: "start" });
  history.replaceState(null, "", `#${selectedSection.id}`);
}

function isWheelInsideSwitcher(event) {
  const rect = switcher.getBoundingClientRect();
  return (
    (event.clientX >= rect.left && event.clientX <= rect.right && event.clientY >= rect.top && event.clientY <= rect.bottom) ||
    switcher.matches(":hover, :focus-within")
  );
}

applyTheme();
buildSwitcher();
updateCurrent();

window.addEventListener("scroll", updateCurrent, { passive: true });

window.addEventListener("wheel", (event) => {
  if (!isWheelInsideSwitcher(event)) return;

  event.preventDefault();

  clearTimeout(wheelGestureUnlockTimer);
  wheelGestureUnlockTimer = setTimeout(() => {
    wheelDelta = 0;
    wheelGestureLocked = false;
  }, 360);

  if (wheelGestureLocked) return;

  wheelDelta += event.deltaY;

  if (Math.abs(wheelDelta) < 28) return;

  stepCurrent(wheelDelta > 0 ? 1 : -1);
  wheelDelta = 0;
  wheelGestureLocked = true;
}, { passive: false });
