document.getElementById("year").textContent = new Date().getFullYear();

// hero oscilloscope — a signal trace standing in for "build activity"
const canvas = document.getElementById("scope");
if (canvas) {
  const ctx = canvas.getContext("2d");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const accent = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim() || "#29f1ff";

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
    ctx.shadowBlur = 10;
    ctx.stroke();
  }

  resize();
  window.addEventListener("resize", resize);

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
