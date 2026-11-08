// Kapsam çubuğu: yazmak yerine seçim. Bütün filtreler aynı cam menüyü açar.
// Lig çoklu seçimlidir ve açık kalır; diğerleri tek seçimlidir ve seçince kapanır.
import { esc, icon, leagueName, monthYear } from "./format.js";

function contractOptions() {
  const now = new Date();
  const first = now.getMonth() < 5 ? now.getFullYear() : now.getFullYear() + 1;
  return [0, 1, 2].map((k) => {
    const value = `${first + k}-06-30`;
    return { value, text: `${monthYear(value)} veya önce`, short: `En geç ${monthYear(value)}` };
  });
}

const upTo = (values, unit, value = (v) => String(v)) =>
  values.map((v) => ({ value: value(v), text: `${unit(v)} ve altı`, short: `${unit(v)} ve altı` }));

const money = (v) => `€${String(v).replace(".", ",")} M`;

const SINGLE = [
  { name: "max_age", label: "Yaş", aria: "En yüksek yaş", options: upTo([19, 20, 21, 22, 23, 24, 25, 27, 30], (v) => `${v} yaş`) },
  { name: "max_value", label: "Değer", aria: "En yüksek piyasa değeri", options: upTo([0.5, 1, 2, 5, 10, 20, 30, 50], money) },
  { name: "foot", label: "Ayak", aria: "Tercih edilen ayak", options: [
    { value: "Right", text: "Sağ", short: "Sağ ayak" },
    { value: "Left", text: "Sol", short: "Sol ayak" },
    { value: "Both", text: "İki ayak", short: "İki ayak" },
  ] },
  { name: "contract_until", label: "Sözleşme", aria: "Sözleşme bitişi", options: contractOptions() },
];

const trigger = (id, label) => `
  <button type="button" class="pill" id="${id}-btn" popovertarget="${id}-menu" data-active="false">
    <span class="pill-text">${label}</span>${icon("updown")}
  </button>`;

const row = (type, name, value, text, checked = false) => `
  <label class="menu-row">
    <input type="${type}" name="${name}" value="${esc(value)}"${checked ? " checked" : ""}>
    ${icon("check")}<span>${esc(text)}</span>
  </label>`;

const singleMenu = (f) => `
  ${trigger(f.name, f.label)}
  <div popover id="${f.name}-menu" class="menu" role="radiogroup" aria-label="${f.aria}" data-single>
    ${row("radio", f.name, "", "Tümü", true)}
    ${f.options.map((o) => row("radio", f.name, o.value, o.text)).join("")}
  </div>`;

function place(menu, button, compact) {
  menu.style.cssText = "";
  if (compact.matches) return; // dar alanda alttan açılır (CSS)
  const box = button.getBoundingClientRect();
  menu.style.left = `${box.left}px`;
  menu.style.top = `${box.bottom + 6}px`;
  menu.style.maxHeight = `min(26rem, ${Math.round(innerHeight - box.bottom - 18)}px)`;
}

function bindMenu(menu, button, compact) {
  menu.addEventListener("beforetoggle", (e) => {
    if (e.newState === "open") place(menu, button, compact);
  });
  // Klavyeyle de kullanılabilsin diye odak menünün içine, seçili satıra gider
  menu.addEventListener("toggle", (e) => {
    if (e.newState !== "open") return;
    const input = menu.querySelector("input:checked") ?? menu.querySelector("input");
    input?.focus({ preventScroll: true });
    input?.closest(".menu-row").scrollIntoView({ block: "nearest" });
  });
  if (!("single" in menu.dataset)) return;
  // Ok tuşları seçimi değiştirirken menü açık kalır; tıklama, Enter ve boşluk kapatır
  menu.addEventListener("click", (e) => {
    if (e.detail > 0 && e.target.closest(".menu-row")) setTimeout(() => menu.hidePopover());
  });
  menu.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") setTimeout(() => menu.hidePopover());
  });
}

export function createFilters(form, leagues, compact, onChange) {
  form.innerHTML = `
    ${trigger("league", "Lig")}
    <div popover id="league-menu" class="menu" role="group" aria-label="Ligler">
      ${Object.entries(leagues).map(([key, name]) => row("checkbox", "league", key, name)).join("")}
    </div>
    ${SINGLE.map(singleMenu).join("")}
    <button type="button" class="scope-reset" id="filters-reset" hidden>Temizle</button>`;

  const leagueBtn = form.querySelector("#league-btn");
  const reset = form.querySelector("#filters-reset");
  const checkedValue = (name) => form.querySelector(`[name="${name}"]:checked`)?.value ?? "";

  const refresh = () => {
    let active = 0;
    for (const f of SINGLE) {
      const pill = form.querySelector(`#${f.name}-btn`);
      const option = f.options.find((o) => o.value === checkedValue(f.name));
      pill.querySelector(".pill-text").textContent = option ? option.short : f.label;
      pill.dataset.active = String(Boolean(option));
      active += option ? 1 : 0;
    }
    const chosen = [...form.querySelectorAll("[name=league]:checked")].map((c) => c.value);
    leagueBtn.querySelector(".pill-text").textContent =
      chosen.length === 0 ? "Lig" : chosen.length === 1 ? leagueName(chosen[0]) : `${chosen.length} lig`;
    leagueBtn.dataset.active = String(chosen.length > 0);
    reset.hidden = active + chosen.length === 0;
  };

  form.querySelectorAll("[popover]").forEach((menu) =>
    bindMenu(menu, form.querySelector(`[popovertarget="${menu.id}"]`), compact));

  // Liste kayınca menü düğmesinden kopmasın
  form.closest(".list-pane")?.addEventListener("scroll", () => {
    form.querySelector("[popover]:popover-open")?.hidePopover();
  }, { passive: true });

  let timer;
  form.addEventListener("change", () => {
    refresh();
    clearTimeout(timer);
    timer = setTimeout(onChange, 120);
  });
  form.addEventListener("submit", (e) => e.preventDefault());

  const clearAll = () => {
    form.reset();
    refresh();
    onChange();
  };
  reset.addEventListener("click", clearAll);

  return {
    clearAll,
    read() {
      const data = new FormData(form);
      return {
        max_age: data.get("max_age"),
        max_value: data.get("max_value"),
        foot: data.get("foot"),
        contract_until: data.get("contract_until"),
        league: data.getAll("league"),
      };
    },
    write(params) {
      for (const f of SINGLE) {
        const wanted = params.get(f.name);
        const radio = wanted && [...form.querySelectorAll(`[name="${f.name}"]`)].find((r) => r.value === wanted);
        if (radio) radio.checked = true;
      }
      const leaguesWanted = params.getAll("league");
      form.querySelectorAll("[name=league]").forEach((c) => { c.checked = leaguesWanted.includes(c.value); });
      refresh();
    },
  };
}
