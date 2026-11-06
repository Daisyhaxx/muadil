// Oyuncu arama kutusu: yazdıkça öneri listesi, klavye ile gezinme.
import { searchPlayers } from "./api.js";
import { esc, groupName, leagueName } from "./format.js";

export function initSearch(input, list, onSelect) {
  let items = [];
  let active = -1;
  let timer;
  let requestId = 0;

  const close = () => {
    list.hidden = true;
    input.setAttribute("aria-expanded", "false");
    active = -1;
  };

  const highlight = () => {
    [...list.children].forEach((li, i) => li.setAttribute("aria-selected", String(i === active)));
  };

  const choose = (i) => {
    const player = items[i];
    if (!player) return;
    input.value = player.name;
    close();
    onSelect(player);
  };

  const render = () => {
    list.innerHTML = items.length
      ? items.map((p) => `<li role="option"><strong>${esc(p.name)}</strong>
          <span>${esc(p.team)} · ${esc(leagueName(p.league))} · ${esc(groupName(p.position_group))}</span></li>`).join("")
      : `<li class="empty">Eşleşme yok (sadece yeterli dakikası olan oyuncular)</li>`;
    [...list.querySelectorAll("li[role=option]")].forEach((li, i) =>
      li.addEventListener("mousedown", (e) => { e.preventDefault(); choose(i); }));
    list.hidden = false;
    input.setAttribute("aria-expanded", "true");
  };

  input.addEventListener("input", () => {
    clearTimeout(timer);
    const q = input.value.trim();
    if (q.length < 2) return close();
    timer = setTimeout(async () => {
      const id = ++requestId;
      const found = await searchPlayers(q);
      if (id !== requestId) return; // eski cevap
      items = found;
      active = -1;
      render();
    }, 200);
  });

  input.addEventListener("keydown", (e) => {
    if (list.hidden) return;
    if (e.key === "ArrowDown") active = Math.min(active + 1, items.length - 1);
    else if (e.key === "ArrowUp") active = Math.max(active - 1, 0);
    else if (e.key === "Enter") return e.preventDefault(), choose(active < 0 ? 0 : active);
    else if (e.key === "Escape") return close();
    else return;
    e.preventDefault();
    highlight();
  });

  input.addEventListener("blur", close);
}
