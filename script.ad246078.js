document.getElementById("year").textContent = new Date().getFullYear();

// ---------------------------------------------------------
// Project card launch: spin fast on click, then follow the link.
// Skipped entirely under reduced motion — click navigates as normal.
// (pop/soft切替の廃止に伴い、テーマ関連のロジックは全て削除。
//  このスピン演出だけ、新デザインのカードに合わせて残した。)
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
