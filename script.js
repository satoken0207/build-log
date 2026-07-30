document.getElementById("year").textContent = new Date().getFullYear();

// ---------------------------------------------------------
// Theme toggle: "pop" (glossy Y2K) <-> "soft"
// ---------------------------------------------------------
const root = document.documentElement;
const toggle = document.getElementById("themeToggle");
const toggleLabel = document.getElementById("themeToggleLabel");

function applyTheme(theme) {
  root.setAttribute("data-theme", theme);
  if (toggle) toggle.setAttribute("aria-pressed", theme === "soft" ? "true" : "false");
  if (toggleLabel) toggleLabel.textContent = theme === "soft" ? "soft" : "pop";
  document.dispatchEvent(new CustomEvent("themechange", { detail: { theme } }));
}

const storedTheme = localStorage.getItem("theme");
applyTheme(storedTheme === "soft" ? "soft" : "pop");

if (toggle) {
  toggle.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "soft" ? "pop" : "soft";
    localStorage.setItem("theme", next);
    applyTheme(next);
  });
}

// ---------------------------------------------------------
// Project card launch: spin fast on click, then follow the link.
// Skipped entirely under reduced motion — click navigates as normal.
// ---------------------------------------------------------
const SPIN_MS = 500;
if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.querySelectorAll(".specimen-link").forEach((link) => {
    link.addEventListener("click", (e) => {
      const card = link.closest(".specimen");
      if (!card || card.classList.contains("is-launching")) return;
      e.preventDefault();
      card.classList.add("is-launching");
      setTimeout(() => { window.location.href = link.href; }, SPIN_MS);
    });
  });
}

// The browser can restore this page from bfcache on back/forward nav
// with the "is-launching" class (and its animation end-state, opacity:0)
// still applied from just before we navigated away. Clear it so the
// card is visible again instead of staying invisible forever.
window.addEventListener("pageshow", (e) => {
  if (e.persisted) {
    document.querySelectorAll(".specimen.is-launching").forEach((card) => {
      card.classList.remove("is-launching");
    });
  }
});

// ---------------------------------------------------------
// Hero oscilloscope — a signal trace standing in for "build
// activity". Redraws its color when the theme changes.
// ---------------------------------------------------------
const canvas = document.getElementById("scope");
if (canvas) {
  const ctx = canvas.getContext("2d");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let accent = "#ff2fa0";
  let glowBlur = 10;
  function readTokens() {
    const styles = getComputedStyle(root);
    accent = styles.getPropertyValue("--accent").trim() || accent;
    glowBlur = parseFloat(styles.getPropertyValue("--scope-blur")) || 0;
  }
  readTokens();
  document.addEventListener("themechange", () => {
    readTokens();
    if (reduceMotion) draw(0);
  });

  function resize() {
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function draw(t) {
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    ctx.clearRect(0, 0, w, h);

    ctx.beginPath();
    const points = 140;
    for (let i = 0; i <= points; i++) {
      const x = (i / points) * w;
      const p = i / points;
      const y =
        h / 2 +
        Math.sin(p * 14 + t) * (h * 0.16) * Math.sin(p * 2.4 + t * 0.3) +
        Math.sin(p * 55 + t * 2.2) * (h * 0.02);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.strokeStyle = accent;
    ctx.lineWidth = 1.6;
    ctx.shadowColor = accent;
    ctx.shadowBlur = glowBlur;
    ctx.stroke();
  }

  resize();
  window.addEventListener("resize", () => {
    resize();
    // Non-reduced-motion mode is redrawn continuously by the rAF loop below,
    // but reduced-motion only draws once — without this the canvas goes
    // blank after any resize (e.g. orientation change) since resizing a
    // <canvas> clears its bitmap.
    if (reduceMotion) draw(0);
  });

  if (reduceMotion) {
    draw(0);
  } else {
    let start = null;
    function frame(ts) {
      if (start === null) start = ts;
      draw((ts - start) / 700);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
}
