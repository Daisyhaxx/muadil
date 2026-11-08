// Oyuncu arama alanı: yazdıkça öneri, klavye ile gezinme, temizleme düğmesi.
import { searchPlayers } from "./api.js";
import { esc, groupName, leagueName } from "./format.js";

export function initSearch({ input, list, clear, minMinutes, onSelect }) {
  let items = [];
  let active = -1;
  let timer;
  let requestId = 0;

  const close = () => {
    list.hidden = true;
    input.setAttribute("aria-expanded", "false");
    input.removeAttribute("aria-activedescendant");
    active = -1;
  };

  const highlight = () => {
    [...list.children].forEach((li, i) => li.setAttribute("aria-selected", String(i === active)));
    if (active >= 0) {
      input.setAttribute("aria-activedescendant", list.children[active].id);
      list.children[active].scrollIntoView({ block: "nearest" });
    }
  };

  const choose = (i) => {
    const player = items[i];
    if (!player) return;
    input.value = "";
    clear.hidden = true;
    close();
    input.blur();
    onSelect(player);
  };

  const render = () => {
    list.innerHTML = items.length
      ? items.map((p, i) => `<li role="option" id="opt-${i}" aria-selected="false">
          <span class="name">${esc(p.name)}</span>
          <span class="info">${esc(p.team)} · ${esc(leagueName(p.league))} · ${esc(groupName(p.position_group))}</span></li>`).join("")
      : `<li class="none">Eşleşme yok. Yalnızca en az ${minMinutes} dakika oynayanlar aranır.</li>`;
    [...list.querySelectorAll("li[role=option]")].forEach((li, i) =>
      li.addEventListener("mousedown", (e) => { e.preventDefault(); choose(i); }));
    list.hidden = false;
    input.setAttribute("aria-expanded", "true");
  };

  input.addEventListener("input", () => {
    clearTimeout(timer);
    const q = input.value.trim();
    clear.hidden = input.value === "";
    if (q.length < 2) return close();
    timer = setTimeout(async () => {
      const id = ++requestId;
      try {
        const found = await searchPlayers(q);
        if (id !== requestId) return; // eski cevap
        items = found;
        active = -1;
        render();
      } catch {
        if (id !== requestId) return;
        list.innerHTML = `<li class="none">Arama yapılamadı. Sunucunun açık olduğundan emin ol.</li>`;
        list.hidden = false;
      }
    }, 150);
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (!list.hidden) return close();
      input.value = "";
      clear.hidden = true;
      input.blur();
      return;
    }
    if (list.hidden) return;
    if (e.key === "ArrowDown") active = Math.min(active + 1, items.length - 1);
    else if (e.key === "ArrowUp") active = Math.max(active - 1, 0);
    else if (e.key === "Enter") return e.preventDefault(), choose(active < 0 ? 0 : active);
    else return;
    e.preventDefault();
    highlight();
  });

  input.addEventListener("blur", close);
  clear.addEventListener("mousedown", (e) => e.preventDefault());
  clear.addEventListener("click", () => {
    input.value = "";
    clear.hidden = true;
    requestId++;
    close();
    input.focus();
  });

  // "/" ile aramaya atla; yazı alanındayken devreye girmez
  document.addEventListener("keydown", (e) => {
    if (e.key !== "/" || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest?.("input, select, textarea")) return;
    e.preventDefault();
    input.focus();
  });
}
