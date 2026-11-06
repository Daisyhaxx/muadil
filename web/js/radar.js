// İki oyuncunun percentile radarı (SVG). Her eksende fareyle gelince iki değer gösterilir.
import { esc, pct } from "./format.js";

const NS = "http://www.w3.org/2000/svg";
const W = 640, H = 500, CX = W / 2, CY = H / 2, R = 190;
const SERIES = [["query_pct", "series-1"], ["candidate_pct", "series-2"]];

function el(tag, attrs, parent) {
  const node = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  parent.appendChild(node);
  return node;
}

// i. eksen, saat yönünde ve tepeden başlar; value 0–1
function point(i, n, value) {
  const a = (2 * Math.PI * i) / n;
  return [CX + R * value * Math.sin(a), CY - R * value * Math.cos(a)];
}

const polygon = (pts) => pts.map((p) => p.join(",")).join(" ");

function axisLabel(svg, i, n, text) {
  const a = (2 * Math.PI * i) / n;
  const [x, y] = point(i, n, 1.07);
  const sx = Math.sin(a), cy = Math.cos(a);
  el("text", {
    x, y, class: "axis-label",
    "text-anchor": sx > 0.1 ? "start" : sx < -0.1 ? "end" : "middle",
    "dominant-baseline": cy > 0.1 ? "auto" : cy < -0.1 ? "hanging" : "middle",
  }, svg).textContent = text;
}

export function renderRadar(container, stats, names) {
  const n = stats.length;
  const svg = document.createElementNS(NS, "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("class", "radar");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", `${names[0]} ve ${names[1]} percentile radarı`);

  for (const v of [0.25, 0.5, 0.75, 1]) el("polygon", { points: polygon(stats.map((_, i) => point(i, n, v))), class: "ring" }, svg);
  stats.forEach((_, i) => { const [x, y] = point(i, n, 1); el("line", { x1: CX, y1: CY, x2: x, y2: y, class: "spoke" }, svg); });
  // Ölçek etiketleri iki eksenin arasında, çizgiye binmesin
  for (const v of [25, 50, 75]) { const [x, y] = point(0.5, n, v / 100); el("text", { x, y, class: "ring-label" }, svg).textContent = v; }

  for (const [key, cls] of SERIES) {
    const pts = stats.map((s, i) => point(i, n, s[key]));
    el("polygon", { points: polygon(pts), class: `area ${cls}` }, svg);
    pts.forEach(([x, y]) => el("circle", { cx: x, cy: y, r: 4, class: `dot ${cls}` }, svg));
  }
  stats.forEach((s, i) => axisLabel(svg, i, n, s.label));
  const hits = el("g", {}, svg); // en üstte, alanlar olayları yutmasın

  const tooltip = document.createElement("div");
  tooltip.className = "tooltip";
  tooltip.hidden = true;

  // Her eksen için dilim şeklinde, işaretten büyük hover alanı
  stats.forEach((s, i) => {
    const hit = el("polygon", { points: polygon([[CX, CY], point(i - 0.5, n, 1.05), point(i + 0.5, n, 1.05)]), class: "hit" }, hits);
    hit.addEventListener("pointermove", (e) => {
      const box = container.getBoundingClientRect();
      tooltip.innerHTML = `<strong>${esc(s.label)}</strong>
        <div class="row"><span class="swatch series-1"></span>${esc(names[0])}: ${pct(s.query_pct)}</div>
        <div class="row"><span class="swatch series-2"></span>${esc(names[1])}: ${pct(s.candidate_pct)}</div>`;
      tooltip.style.left = `${e.clientX - box.left + 14}px`;
      tooltip.style.top = `${e.clientY - box.top + 14}px`;
      tooltip.hidden = false;
    });
    hit.addEventListener("pointerleave", () => { tooltip.hidden = true; });
  });

  container.replaceChildren(svg, tooltip);
}
