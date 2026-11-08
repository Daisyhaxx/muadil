// Uygulama akışı: oyuncu seç → muadilleri getir → birini seç → karşılaştır.
// Geniş alanda liste ve ayrıntı yan yana; dar alanda ayrıntı ayrı bir görünüm olarak açılır.
import { getCompare, getMeta, getSimilar } from "./api.js";
import { createDetail } from "./detail.js";
import { createFilters } from "./filters.js";
import { esc, profileLabel, setMeta } from "./format.js";
import { bindResults, markSelected, renderGhosts, renderQuery, renderResults } from "./results.js";
import { initSearch } from "./search.js";
import { initSidebar } from "./sidebar.js";

const EXAMPLES = [
  { id: 822471, name: "Victor Osimhen", role: "Forvet" },
  { id: 907461, name: "Orkun Kökçü", role: "Orta saha" },
  { id: 904096, name: "Barış Alper Yılmaz", role: "Kanat" },
  { id: 754794, name: "Lucas Torreira", role: "Orta saha" },
  { id: 754330, name: "Uğurcan Çakır", role: "Kaleci" },
];
const PAGE_SIZES = [10, 25, 50];

const $ = (id) => document.getElementById(id);
const body = document.body;
const list = $("results");
const notice = $("notice");
const more = $("more");
const status = $("status");
const pane = $("detail");
const compact = matchMedia("(max-width: 53.99em)");

const state = { queryId: null, candidateId: null, top: PAGE_SIZES[0], loaded: false };
let filters;
let detail;
let searchRun = 0;
let compareRun = 0;

function urlFor() {
  const params = new URLSearchParams();
  if (state.queryId != null) params.set("player", state.queryId);
  if (state.candidateId != null) params.set("c", state.candidateId);
  for (const [key, value] of Object.entries(filters.read())) {
    for (const v of [value].flat()) if (v) params.append(key, v);
  }
  return `?${params}`;
}
const syncUrl = () => history.replaceState(history.state, "", urlFor());

function showNotice(text, action) {
  notice.innerHTML = `<p>${esc(text)}</p>${action ? `<button type="button">${esc(action.label)}</button>` : ""}`;
  notice.hidden = false;
  if (action) notice.querySelector("button").addEventListener("click", action.run);
}

async function selectCandidate(id, open = false) {
  state.candidateId = id;
  markSelected(list, id);
  syncUrl();
  if (open && compact.matches) {
    history.pushState({ detail: true }, "", urlFor());
    body.dataset.view = "detail";
    pane.scrollTop = 0;
  }
  const run = ++compareRun;
  detail.setBusy(true);
  try {
    const data = await getCompare(state.queryId, id);
    if (run !== compareRun) return;
    pane.hidden = false;
    detail.update(data);
  } catch (err) {
    if (run === compareRun) showNotice(`Karşılaştırma açılamadı: ${err.message}`, { label: "Tekrar dene", run: () => { notice.hidden = true; selectCandidate(id); } });
  } finally {
    if (run === compareRun) detail.setBusy(false);
  }
}

// Geçişleri kıyas ekranı yerleştikten sonra aç; ana ekrandan gelirken öğeler animasyonla uçuşmasın
function settle() {
  if (body.classList.contains("settled")) return;
  requestAnimationFrame(() => requestAnimationFrame(() => body.classList.add("settled")));
}

async function loadResults() {
  if (state.queryId == null) return;
  const run = ++searchRun;
  body.dataset.state = "ready";
  settle();
  notice.hidden = true;
  status.textContent = "Aranıyor…";
  if (state.loaded) list.setAttribute("aria-busy", "true");
  else renderGhosts(list);

  try {
    const data = await getSimilar(state.queryId, { ...filters.read(), top: state.top });
    if (run !== searchRun) return;
    state.loaded = true;
    renderQuery($("query"), data.query);
    renderResults(list, data.results);
    list.setAttribute("aria-busy", "false");
    document.title = `${data.query.name} · Muadil`;

    const ids = data.results.map((r) => r.player_id);
    status.textContent = `${ids.length} oyuncu`;
    more.hidden = ids.length < state.top || state.top === PAGE_SIZES.at(-1);

    if (!ids.length) {
      state.candidateId = null;
      pane.hidden = true;
      syncUrl();
      showNotice("Bu filtrelere uyan oyuncu yok.", { label: "Filtreleri temizle", run: () => filters.clearAll() });
      return;
    }
    if (ids.includes(state.candidateId)) selectCandidate(state.candidateId);
    else if (!compact.matches) selectCandidate(ids[0]);
    else { state.candidateId = null; syncUrl(); }
  } catch (err) {
    if (run !== searchRun) return;
    list.setAttribute("aria-busy", "false");
    list.innerHTML = "";
    status.textContent = "";
    showNotice(`Liste alınamadı: ${err.message}`, { label: "Tekrar dene", run: loadResults });
  }
}

function openPlayer(id) {
  state.queryId = id;
  state.candidateId = null;
  state.top = PAGE_SIZES[0];
  state.loaded = false;
  body.dataset.view = "list";
  loadResults();
}

function closeDetail() {
  if (history.state?.detail) history.back();
  else { body.dataset.view = "list"; syncUrl(); }
}

function trackKeyboard() {
  const viewport = window.visualViewport;
  if (!viewport) return;
  const update = () => document.documentElement.style.setProperty(
    "--kb", `${Math.max(0, innerHeight - viewport.height - viewport.offsetTop)}px`);
  viewport.addEventListener("resize", update);
  viewport.addEventListener("scroll", update);
}

async function init() {
  const meta = await getMeta();
  setMeta(meta);
  const leagueCount = Object.keys(meta.leagues).length;
  $("empty-text").textContent =
    `Bir oyuncu seç; ${leagueCount} ligde aynı mevkide oynayan, istatistik profili ona en çok benzeyenleri bulalım.`;
  $("examples").innerHTML = EXAMPLES.map((e) =>
    `<button type="button" class="example" data-id="${e.id}">${esc(e.name)}<span>${esc(e.role)}</span></button>`).join("");
  $("examples").addEventListener("click", (e) => {
    const button = e.target.closest(".example");
    if (button) openPlayer(Number(button.dataset.id));
  });
  $("provenance").textContent = `${meta.year} sezonu · en az ${meta.min_minutes} dakika · profil: ${profileLabel()}`;

  detail = createDetail(pane);
  filters = createFilters($("filters"), meta.leagues, compact, () => { syncUrl(); loadResults(); });
  bindResults(list, selectCandidate);
  initSearch({
    input: $("search-input"), list: $("suggestions"), clear: $("search-clear"),
    minMinutes: meta.min_minutes, onSelect: (p) => openPlayer(p.player_id),
  });

  more.addEventListener("click", () => {
    state.top = PAGE_SIZES[PAGE_SIZES.indexOf(state.top) + 1];
    loadResults();
  });
  $("back").addEventListener("click", closeDetail);
  addEventListener("popstate", (e) => { body.dataset.view = e.state?.detail ? "detail" : "list"; });
  compact.addEventListener("change", () => {
    if (!compact.matches && state.loaded && state.candidateId == null && list.querySelector(".row")) {
      selectCandidate(Number(list.querySelector(".row").dataset.id));
    }
  });
  trackKeyboard();
  initSidebar({ button: $("sidebar-toggle"), pane: $("list-pane"), compact });

  const params = new URLSearchParams(location.search);
  filters.write(params);
  const player = Number(params.get("player"));
  if (player) {
    state.queryId = player;
    state.candidateId = Number(params.get("c")) || null;
    if (state.candidateId && compact.matches) body.dataset.view = "detail";
    loadResults();
  } else if (matchMedia("(hover: hover)").matches) {
    $("search-input").focus();
  }
}

init().catch((err) => {
  $("empty-text").textContent = `Sunucuya ulaşılamadı (${err.message}). Sunucunun açık olduğundan emin olup sayfayı yenile.`;
});
