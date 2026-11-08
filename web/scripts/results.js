// Aranan oyuncu başlığı ve muadil listesi.
import { esc, groupName, icon, leagueName, money, score } from "./format.js";

export function renderQuery(box, q) {
  box.innerHTML = `
    <h2><i class="mark a" aria-hidden="true"></i>${esc(q.name)}</h2>
    <p>${esc(q.team)} · ${esc(leagueName(q.league))}</p>
    <p>${esc(groupName(q.position_group))} · ${q.age ?? "—"} yaş · ${money(q.market_value)}</p>`;
}

const row = (p, rank) => `
  <li><button type="button" class="row" data-id="${p.player_id}" aria-current="false">
    <span class="rank">${rank}</span>
    <span>
      <span class="row-name">${esc(p.name)}</span>
      <span class="row-sub">${esc(p.team)} · ${esc(leagueName(p.league))}</span>
      <span class="row-meta">${p.age ?? "—"} yaş · ${esc(p.positions[0] ?? "—")} · ${money(p.market_value)}</span>
    </span>
    <span class="row-end">
      <i class="mark b" aria-hidden="true"></i>
      <span class="score"><span class="sr-only">benzerlik </span>${score(p.similarity)}</span>
      ${icon("right")}
    </span>
  </button></li>`;

export const renderResults = (list, results) => {
  list.innerHTML = results.map((p, i) => row(p, i + 1)).join("");
};

export const renderGhosts = (list) => {
  list.innerHTML = Array.from({ length: 6 }, () => `<li><span class="ghost"></span></li>`).join("");
};

export function markSelected(list, id) {
  for (const button of list.querySelectorAll(".row")) {
    button.setAttribute("aria-current", String(Number(button.dataset.id) === id));
  }
}

export function bindResults(list, onSelect) {
  list.addEventListener("click", (e) => {
    const button = e.target.closest(".row");
    if (button) onSelect(Number(button.dataset.id), true);
  });
  // Liste içinde ok tuşlarıyla gezinme
  list.addEventListener("keydown", (e) => {
    if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
    const rows = [...list.querySelectorAll(".row")];
    const next = rows[rows.indexOf(document.activeElement) + (e.key === "ArrowDown" ? 1 : -1)];
    if (!next) return;
    e.preventDefault();
    next.focus();
    onSelect(Number(next.dataset.id), false);
  });
}
