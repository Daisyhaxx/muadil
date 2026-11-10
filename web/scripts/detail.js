// Karşılaştırma görünümü. İskelet bir kez kurulur; radar aynı kalır ki aday değişince şekil akabilsin.
import { confidence, esc, foot, icon, int, leagueName, money, monthYear, pct, profileLabel, score, tradeoff } from "./format.js";
import { createRadar } from "./radar.js";

const SKELETON = `
  <div class="detail-inner">
    <div class="matchup"></div>
    <p class="tradeoff"></p>
    <table class="h2h"><thead></thead><tbody></tbody></table>

    <section class="block">
      <h3 class="block-title">Oyun profili</h3>
      <p class="block-lead"></p>
      <div class="radar-host"></div>
      <div class="readout" aria-live="polite"></div>
      <div class="legend"></div>
      <p class="chart-note"></p>
    </section>

    <div class="traits">
      <section><h3>Ortak yönler</h3><ul class="common"></ul></section>
      <section><h3>En büyük farklar</h3><ul class="different"></ul></section>
    </div>

    <details class="all">
      <summary>${icon("right")}<span class="all-title"></span></summary>
      <table><thead></thead><tbody></tbody></table>
      <p class="all-note">Katkıların toplamı benzerlik skorunu verir.</p>
    </details>
  </div>`;

const REFERENCE_MINUTES = 900; // altındaki oyuncular düzeltilerek gösterilir (src/features/shrinkage.py)
const hasBoth = (s) => s.query_pct != null && s.candidate_pct != null;
const marks = {
  a: `<i class="mark a" aria-hidden="true"></i>`,
  b: `<i class="mark b" aria-hidden="true"></i>`,
};

const side = (player, key) => `
  <div class="side ${key}">
    <div class="side-name">${marks[key]}<h2>${esc(player.name)}</h2></div>
    <p>${esc(player.team)}</p>
    <p>${esc(leagueName(player.league))}</p>
  </div>`;

const facts = (q, c) => [
  ["Yaş", q.age ?? "—", c.age ?? "—"],
  ["Değer", money(q.market_value), money(c.market_value)],
  ["Sözleşme", monthYear(q.contract_until), monthYear(c.contract_until)],
  ["Mevki", q.positions.join(", ") || "—", c.positions.join(", ") || "—"],
  ["Ayak", foot(q.preferred_foot), foot(c.preferred_foot)],
  ["Dakika", int(q.minutes), int(c.minutes)],
  ["Veri güveni", confidence(q.confidence), confidence(c.confidence)],
];

function bell(s, names) {
  const hasQ = s.query_pct != null, hasC = s.candidate_pct != null;
  const q = (s.query_pct ?? 0) * 100, c = (s.candidate_pct ?? 0) * 100;
  const gap = hasQ && hasC
    ? `<i class="bell-gap" style="left:${Math.min(q, c)}%;width:${Math.abs(q - c)}%"></i>` : "";
  return `<li class="bell">
    <span class="bell-label">${esc(s.label)}</span>
    <span class="bell-values">
      ${marks.a}<span><span class="sr-only">${esc(names[0])} </span>${pct(s.query_pct)}</span>
      ${marks.b}<span><span class="sr-only">${esc(names[1])} </span>${pct(s.candidate_pct)}</span>
    </span>
    <span class="bell-track" aria-hidden="true">
      ${gap}
      ${hasQ ? `<i class="mark a" style="left:${q}%"></i>` : ""}
      ${hasC ? `<i class="mark b" style="left:${c}%"></i>` : ""}
    </span>
  </li>`;
}

const bells = (stats, names, emptyText) =>
  stats.map((s) => bell(s, names)).join("") || `<li class="empty-note">${emptyText}</li>`;

export function createDetail(root) {
  root.innerHTML = SKELETON;
  const $ = (selector) => root.querySelector(selector);
  const inner = $(".detail-inner");
  const radar = createRadar($(".radar-host"), $(".readout"));

  return {
    setBusy(busy) { inner.setAttribute("aria-busy", String(busy)); },

    update({ query: q, candidate: c, similarity, stats, common, different }) {
      const names = [q.name, c.name];
      const radarStats = stats.filter((s) => s.on_radar);
      const missing = radarStats.filter((s) => !hasBoth(s)).map((s) => s.label);

      $(".matchup").innerHTML = `${side(q, "a")}
        <div class="verdict-score"><strong>${score(similarity)}</strong><span>benzerlik</span></div>
        ${side(c, "b")}`;
      $(".tradeoff").textContent = tradeoff(q, c);
      $(".h2h thead").innerHTML = `<tr>
        <th scope="col" class="a">${marks.a}<span class="sr-only">${esc(q.name)}</span></th>
        <td></td>
        <th scope="col" class="b">${marks.b}<span class="sr-only">${esc(c.name)}</span></th></tr>`;
      $(".h2h tbody").innerHTML = facts(q, c).map(([label, a, b]) =>
        `<tr><td class="a">${esc(a)}</td><th scope="row">${label}</th><td class="b">${esc(b)}</td></tr>`).join("");

      const overlaps = common.slice(0, 3).map((s) => s.label).join(", ");
      const splits = different.slice(0, 2).map((s) => s.label).join(", ");
      $(".block-lead").textContent = [
        overlaps && `En çok örtüştükleri: ${overlaps}.`,
        splits && `En çok ayrıldıkları: ${splits}.`,
      ].filter(Boolean).join(" ");

      $(".legend").innerHTML = `
        <span>${marks.a}${esc(q.name)}</span>
        <span>${marks.b}${esc(c.name)}</span>
        <span><i class="swatch" aria-hidden="true"></i>Örtüşen alan</span>`;
      $(".chart-note").textContent =
        `Mevki içinde 0–100 yüzdelik, 90 dakika başına; ${profileLabel()}. ` +
        `Benzerlik ${stats.length} istatistikten hesaplanır, radar ${radarStats.length} tanesini gösterir.` +
        (missing.length ? ` Bu ligde verisi olmadığı için gösterilmiyor: ${missing.join(", ")}.` : "") +
        (q.minutes < REFERENCE_MINUTES || c.minutes < REFERENCE_MINUTES
          ? ` ${REFERENCE_MINUTES} dakikanın altında oynayanların değerleri mevki ortalamasına doğru çekildi.` : "");
      radar.update(radarStats.filter(hasBoth), names);

      $(".common").innerHTML = bells(common, names, "Belirgin ortak yön yok.");
      $(".different").innerHTML = bells(different, names, "Belirgin fark yok.");

      $(".all-title").textContent = `Tüm istatistikler (${stats.length})`;
      $(".all thead").innerHTML = `<tr>
        <th>İstatistik</th>
        <th>${marks.a}<span class="sr-only">${esc(q.name)}</span></th>
        <th>${marks.b}<span class="sr-only">${esc(c.name)}</span></th>
        <th>Katkı</th></tr>`;
      $(".all tbody").innerHTML = stats.map((s) => `<tr>
        <td>${esc(s.label)}</td><td>${pct(s.query_pct)}</td><td>${pct(s.candidate_pct)}</td><td>${score(s.contribution)}</td></tr>`).join("");
    },
  };
}
