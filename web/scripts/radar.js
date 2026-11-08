// İki oyunculu yüzdelik radarı (SVG). Aday değişince çizgi yeni şekline akar, aranan oyuncu sabit kalır.
// Dar alanda etiketler sığmaz: yalnızca şekil çizilir, değerler alttaki okuma satırı ve tablodan gelir.
import { esc, pct } from "./format.js";
import { projector, sharedOutline, toPoints } from "./radar-geometry.js";

const NS = "http://www.w3.org/2000/svg";
const MORPH_MS = 260;
const MIN_LABELLED_RADIUS = 130;
const MAX_RADIUS = 240;
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
const canHover = matchMedia("(hover: hover)");

function add(tag, attrs, parent) {
  const node = document.createElementNS(NS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  parent.appendChild(node);
  return node;
}

function widestLabel(host, stats) {
  const style = getComputedStyle(host);
  const context = document.createElement("canvas").getContext("2d");
  context.font = `600 ${style.fontSize} ${style.fontFamily}`;
  return Math.max(...stats.map((s) => context.measureText(s.label).width));
}

export function createRadar(host, readout) {
  let stats = [];
  let names = ["", ""];
  let shown = [];   // o anda çizili aday değerleri (geçiş sırasında ara değerler)
  let parts = null;
  let active = -1;
  let frame = 0;
  let width = 0;

  const queryValues = () => stats.map((s) => s.query_pct);
  const finalValues = () => stats.map((s) => s.candidate_pct);

  function showHint() {
    readout.innerHTML = `<span class="hint">${canHover.matches ? "Değerleri görmek için bir eksenin üstüne gel" : "Değerleri görmek için bir dilime dokun"}</span>`;
  }

  function setActive(index) {
    if (index === active) return;
    if (active >= 0 && parts) {
      parts.spokes[active].classList.remove("is-active");
      parts.axes[active]?.classList.remove("is-active");
    }
    active = index;
    if (active < 0) return showHint();
    parts.spokes[active].classList.add("is-active");
    parts.axes[active]?.classList.add("is-active");
    const s = stats[active];
    readout.innerHTML = `<strong>${esc(s.label)}</strong>
      <span><i class="mark a" aria-hidden="true"></i><span class="sr-only">${esc(names[0])}</span>${pct(s.query_pct)}</span>
      <span><i class="mark b" aria-hidden="true"></i><span class="sr-only">${esc(names[1])}</span>${pct(s.candidate_pct)}</span>`;
  }

  function draw(project) {
    const q = queryValues();
    const qPoints = q.map((v, i) => project(i, v));
    const cPoints = shown.map((v, i) => project(i, v));
    const qText = toPoints(qPoints), cText = toPoints(cPoints);
    parts.washA.setAttribute("points", qText);
    parts.lineA.setAttribute("points", qText);
    parts.washB.setAttribute("points", cText);
    parts.lineB.setAttribute("points", cText);
    parts.shared.setAttribute("points", toPoints(sharedOutline(q, shown, project)));
    qPoints.forEach(([x, y], i) => { parts.dotsA[i].setAttribute("cx", x); parts.dotsA[i].setAttribute("cy", y); });
    cPoints.forEach(([x, y], i) => parts.dotsB[i].setAttribute("transform", `translate(${x} ${y})`));
  }

  function build() {
    const axes = stats.length;
    width = Math.round(host.clientWidth);
    if (!width || !axes) return;
    active = -1;

    const fontSize = parseFloat(getComputedStyle(host).fontSize);
    const room = width / 2 - widestLabel(host, stats) - 14;
    const labelled = room >= MIN_LABELLED_RADIUS;
    const radius = labelled ? Math.min(room, MAX_RADIUS) : Math.min(width / 2 - 12, 170);
    const marginY = labelled ? fontSize * 2.4 : 12;
    const height = Math.round(2 * radius + 2 * marginY);
    const cx = width / 2, cy = height / 2;
    const project = projector(cx, cy, radius, axes);

    const svg = document.createElementNS(NS, "svg");
    Object.entries({
      viewBox: `0 0 ${width} ${height}`, width, height, class: "radar", role: "img", tabindex: "0",
      "aria-label": `${names[0]} ve ${names[1]} için yüzdelik radar. Ok tuşlarıyla eksenler arasında gezilebilir; tüm değerler aşağıdaki tabloda.`,
    }).forEach(([k, v]) => svg.setAttribute(k, v));

    const washA = add("polygon", { class: "wash-a" }, svg);
    const washB = add("polygon", { class: "wash-b" }, svg);
    const shared = add("polygon", { class: "shared" }, svg);
    for (const v of [0.25, 0.5, 0.75, 1]) {
      add("polygon", { class: "ring", points: toPoints(stats.map((_, i) => project(i, v))) }, svg);
    }
    const spokes = stats.map((_, i) => {
      const [x, y] = project(i, 1);
      return add("line", { class: "spoke", x1: cx, y1: cy, x2: x, y2: y }, svg);
    });
    const lineA = add("polygon", { class: "line line-a" }, svg);
    const lineB = add("polygon", { class: "line line-b" }, svg);
    const dotsA = stats.map(() => add("circle", { class: "dot dot-a", r: 4 }, svg));
    const dotsB = stats.map(() => add("polygon", { class: "dot dot-b", points: "0,-5 5,0 0,5 -5,0" }, svg));

    for (const v of [25, 50, 75]) {
      const [x, y] = project(0.5, v / 100);
      add("text", { class: "ring-label", x, y }, svg).textContent = v;
    }

    const axisLabels = labelled ? stats.map((s, i) => {
      const angle = (2 * Math.PI * i) / axes;
      const [x, y] = project(i, 1.05);
      const sin = Math.sin(angle), cos = Math.cos(angle);
      const label = add("text", {
        class: "axis", x, y,
        "text-anchor": sin > 0.1 ? "start" : sin < -0.1 ? "end" : "middle",
        "dominant-baseline": cos > 0.3 ? "auto" : cos < -0.3 ? "hanging" : "middle",
      }, svg);
      label.textContent = s.label;
      return label;
    }) : [];

    const hits = add("g", {}, svg); // en üstte, alttaki şekiller olayları yutmasın
    stats.forEach((_, i) => {
      const hit = add("polygon", { class: "hit", points: toPoints([[cx, cy], project(i - 0.5, 1.4), project(i + 0.5, 1.4)]) }, hits);
      hit.addEventListener("pointerenter", () => setActive(i));
      hit.addEventListener("pointerdown", () => setActive(i));
    });

    svg.addEventListener("mousedown", (e) => e.preventDefault()); // odak halkası yalnızca klavyede
    svg.addEventListener("pointerleave", (e) => { if (e.pointerType === "mouse") setActive(-1); });
    svg.addEventListener("blur", () => setActive(-1));
    svg.addEventListener("keydown", (e) => {
      if (e.key === "Escape") return setActive(-1);
      const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (!step) return;
      e.preventDefault();
      setActive(active < 0 ? 0 : (active + step + axes) % axes);
    });

    parts = { project, washA, washB, shared, lineA, lineB, dotsA, dotsB, spokes, axes: axisLabels };
    host.replaceChildren(svg);
    showHint();
    draw(project);
  }

  function morphTo(target) {
    cancelAnimationFrame(frame);
    const from = shown.slice();
    const start = performance.now();
    const step = (now) => {
      const progress = Math.min(1, (now - start) / MORPH_MS);
      const eased = 1 - (1 - progress) ** 3;
      shown = from.map((v, i) => v + (target[i] - v) * eased);
      draw(parts.project);
      if (progress < 1) frame = requestAnimationFrame(step);
    };
    frame = requestAnimationFrame(step);
  }

  // Menü kayarken her karede yeniden çizme; görünür olduğunda ise hemen çiz
  let resizeTimer;
  new ResizeObserver(() => {
    const next = Math.round(host.clientWidth);
    if (next === width || !stats.length) return;
    clearTimeout(resizeTimer);
    if (width === 0 || next === 0) build();
    else resizeTimer = setTimeout(build, 150);
  }).observe(host);

  return {
    update(nextStats, nextNames) {
      const sameShape = parts && stats.length === nextStats.length
        && nextStats.every((s, i) => s.field === stats[i].field && s.query_pct === stats[i].query_pct);
      const wasActive = active;
      stats = nextStats;
      names = nextNames;
      const target = finalValues();

      if (sameShape && !reducedMotion.matches) {
        parts.spokes[0].ownerSVGElement.setAttribute("aria-label",
          `${names[0]} ve ${names[1]} için yüzdelik radar. Ok tuşlarıyla eksenler arasında gezilebilir; tüm değerler aşağıdaki tabloda.`);
        active = -1;
        if (wasActive >= 0) setActive(wasActive);
        morphTo(target);
        return;
      }
      cancelAnimationFrame(frame);
      shown = target;
      build();
    },
  };
}
