// Uygulama akışı: meta yükle → oyuncu seç → benzerleri getir → satır seç → karşılaştır.
import { getCompare, getMeta, getSimilar } from "./api.js";
import { renderCompare } from "./compare.js";
import { esc, setMeta } from "./format.js";
import { renderQuery, renderResults, selectFirst } from "./results.js";
import { initSearch } from "./search.js";

const $ = (id) => document.getElementById(id);
const form = $("filters");
const table = $("results-table");
const status = $("status");
const compare = $("compare");

let queryId = null;
let searchRun = 0;

function setStatus(text, isError = false) {
  status.textContent = text;
  status.classList.toggle("error", isError);
  status.hidden = !text;
}

function readFilters() {
  const data = new FormData(form);
  return {
    top: data.get("top"),
    max_age: data.get("max_age"),
    max_value: data.get("max_value"),
    foot: data.get("foot"),
    contract_until: data.get("contract_until"),
    league: data.getAll("league"),
  };
}

async function showCompare(candidateId) {
  try {
    renderCompare(compare, await getCompare(queryId, candidateId));
  } catch (err) {
    setStatus(`Karşılaştırma alınamadı: ${err.message}`, true);
  }
}

async function runSearch() {
  if (queryId == null) return;
  const run = ++searchRun;
  setStatus("Aranıyor…");
  try {
    const data = await getSimilar(queryId, readFilters());
    if (run !== searchRun) return; // daha yeni bir arama başladı
    renderQuery($("query-card"), data.query);
    renderResults(table, data.results, showCompare);
    compare.hidden = data.results.length === 0;
    setStatus(data.results.length ? "" : "Filtrelere uyan oyuncu yok.");
    selectFirst(table);
  } catch (err) {
    setStatus(`Arama başarısız: ${err.message}`, true);
  }
}

function renderLeagueFilter(leagues) {
  const fieldset = $("league-filter");
  fieldset.insertAdjacentHTML("beforeend", Object.entries(leagues).map(([key, name]) =>
    `<label><input type="checkbox" name="league" value="${esc(key)}">${esc(name)}</label>`).join(""));
}

async function init() {
  const meta = await getMeta();
  setMeta(meta);
  $("season").textContent = `${meta.year} · ${meta.min_minutes}+ dk · profil ${meta.profile_years.join(" + ")}`;
  renderLeagueFilter(meta.leagues);

  initSearch($("player-input"), $("suggestions"), (player) => {
    queryId = player.player_id;
    history.replaceState(null, "", `?player=${queryId}`); // paylaşılabilir link
    runSearch();
  });

  let timer;
  form.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(runSearch, 300); });
  form.addEventListener("submit", (e) => e.preventDefault());

  const linked = new URLSearchParams(location.search).get("player");
  if (linked) {
    queryId = Number(linked);
    runSearch();
  }
}

init().catch((err) => setStatus(`Sunucuya bağlanılamadı: ${err.message}`, true));
