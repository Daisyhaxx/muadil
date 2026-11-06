// Karşılaştırma paneli: başlık + lejant, radar, ortak yönler / farklar, tablo görünümü.
import { esc, pct, score } from "./format.js";
import { renderRadar } from "./radar.js";

const listItems = (stats) =>
  stats.map((s) => `<li><span>${esc(s.label)}</span><span>${pct(s.query_pct)} / ${pct(s.candidate_pct)}</span></li>`).join("")
  || `<li><span>—</span></li>`;

const tableRows = (stats) =>
  stats.map((s) => `<tr><td>${esc(s.label)}</td><td class="num">${pct(s.query_pct)}</td>
    <td class="num">${pct(s.candidate_pct)}</td><td class="num">${score(s.contribution)}</td></tr>`).join("");

export function renderCompare(section, data) {
  const { query: q, candidate: c, stats } = data;
  const ranked = [...stats].sort((a, b) => b.contribution - a.contribution);
  const common = ranked.slice(0, 5);
  const different = ranked.filter((s) => s.contribution < 0).slice(-3).reverse();

  section.innerHTML = `
    <h2>${esc(q.name)} – ${esc(c.name)} · benzerlik ${score(data.similarity)}</h2>
    <p class="sub">Mevki içi percentile (0–100), 90 dakika başına. Değerler: sorgu / aday.</p>
    <div class="legend">
      <span><i class="swatch series-1"></i>${esc(q.name)}</span>
      <span><i class="swatch series-2"></i>${esc(c.name)}</span>
    </div>
    <div class="radar-wrap"></div>
    <div class="explain">
      <div><h3>Ortak yönler</h3><ul>${listItems(common)}</ul></div>
      <div><h3>En büyük farklar</h3><ul>${listItems(different)}</ul></div>
    </div>
    <details>
      <summary>Tüm istatistikler (tablo)</summary>
      <table>
        <thead><tr><th>İstatistik</th><th class="num">${esc(q.name)}</th><th class="num">${esc(c.name)}</th>
          <th class="num">Katkı</th></tr></thead>
        <tbody>${tableRows(stats)}</tbody>
      </table>
    </details>`;
  renderRadar(section.querySelector(".radar-wrap"), stats, [q.name, c.name]);
  section.hidden = false;
}
