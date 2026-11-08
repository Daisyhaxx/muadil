// Gösterim yardımcıları (tr-TR biçimleri, lig/mevki adları, HTML kaçışı).

let meta = { leagues: {}, position_groups: {} };
export const setMeta = (m) => { meta = m; };

export const leagueName = (key) => meta.leagues[key] ?? key;
export const groupName = (key) => meta.position_groups[key] ?? key;

export function profileLabel() {
  const years = meta.profile_years ?? [meta.year];
  return years.length < 2 ? years[0] : `${years.join(" + ")} ortalaması`;
}

const oneDecimal = new Intl.NumberFormat("tr-TR", { maximumFractionDigits: 1 });
const twoDecimals = new Intl.NumberFormat("tr-TR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const integer = new Intl.NumberFormat("tr-TR");

export const money = (v) => (v == null ? "—" : `€${oneDecimal.format(v / 1e6)} M`);
export const score = (v) => twoDecimals.format(v);
// null = ligde veri yok (örn. TFF 1. Lig'de xG)
export const pct = (v) => (v == null ? "—" : Math.round(v * 100));
export const int = (v) => (v == null ? "—" : integer.format(v));
export const foot = (f) => ({ Left: "Sol", Right: "Sağ", Both: "İki ayak" })[f] ?? "—";
export const monthYear = (d) =>
  d ? new Date(d).toLocaleDateString("tr-TR", { month: "short", year: "numeric" }) : "—";

// Ürünün asıl sorusu: aday, aranan oyuncudan daha genç / daha ucuz mu?
export function tradeoff(q, c) {
  const parts = [];
  if (q.age != null && c.age != null && q.age !== c.age) {
    const d = q.age - c.age;
    parts.push(d > 0 ? `${d} yaş genç` : `${-d} yaş büyük`);
  }
  if (q.market_value != null && c.market_value != null && q.market_value !== c.market_value) {
    const d = q.market_value - c.market_value;
    parts.push(`${money(Math.abs(d))} ${d > 0 ? "ucuz" : "pahalı"}`);
  }
  return parts.length ? `Aranan oyuncudan ${parts.join(", ")}.` : "";
}

const ESCAPES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
export const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ESCAPES[c]);

export const icon = (name) => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"/></svg>`;
