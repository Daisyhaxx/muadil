// Sorgu oyuncusu kartı ve sonuç tablosu.
import { esc, foot, groupName, int, leagueName, money, monthYear, score } from "./format.js";

export function renderQuery(card, q) {
  card.innerHTML = `
    <h2>${esc(q.name)}</h2>
    <p>${esc(q.team)} · ${esc(leagueName(q.league))} · ${esc(groupName(q.position_group))}
       (${esc(q.positions.join(", "))}) · ${q.age ?? "—"} yaş · ${int(q.minutes)} dk ·
       ${money(q.market_value)} · ${foot(q.preferred_foot)} · sözleşme ${monthYear(q.contract_until)}</p>`;
  card.hidden = false;
}

function row(p, rank) {
  const common = p.common.slice(0, 3).map((s) => s.label).join(", ");
  const width = Math.max(0, Math.min(1, p.similarity)) * 100;
  return `
    <tr tabindex="0" data-id="${p.player_id}" aria-selected="false">
      <td class="num">${rank}</td>
      <td><span class="player-name">${esc(p.name)}</span>
          <span class="sub">${esc(p.team)}</span>
          <span class="common">Ortak: ${esc(common)}</span></td>
      <td>${esc(leagueName(p.league))}</td>
      <td class="num">${p.age ?? "—"}</td>
      <td>${esc(p.positions.join(", "))}</td>
      <td class="num">${int(p.minutes)}</td>
      <td class="num">${money(p.market_value)}</td>
      <td><div class="meter"><div class="track"><div class="fill" style="width:${width}%"></div></div>
          <span>${score(p.similarity)}</span></div></td>
    </tr>`;
}

export function renderResults(table, results, onSelect) {
  const body = table.tBodies[0];
  body.innerHTML = results.map((p, i) => row(p, i + 1)).join("");
  table.hidden = results.length === 0;

  for (const tr of body.rows) {
    const select = () => {
      for (const other of body.rows) other.setAttribute("aria-selected", String(other === tr));
      onSelect(Number(tr.dataset.id));
    };
    tr.addEventListener("click", select);
    tr.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(); }
    });
  }
}

export function selectFirst(table) {
  table.tBodies[0].rows[0]?.click();
}
