// Gösterim yardımcıları (tr-TR biçimleri, lig/mevki adları, HTML kaçışı).

let meta = { leagues: {}, position_groups: {} };
export const setMeta = (m) => { meta = m; };

export const leagueName = (key) => meta.leagues[key] ?? key;
export const groupName = (key) => meta.position_groups[key] ?? key;

// Profilin dayandığı sezonlar: "25/26 + 24/25 ortalaması (önceki sezon ×0,5)" ya da tek sezon "25/26"
export function profileLabel() {
  const years = meta.profile_years ?? [meta.year];
  if (years.length < 2) return years[0];
  const decay = new Intl.NumberFormat("tr-TR").format(meta.profile_decay);
  return `${years.join(" + ")} ortalaması (dakika ağırlıklı, önceki sezon ×${decay})`;
}

const oneDecimal = new Intl.NumberFormat("tr-TR", { maximumFractionDigits: 1 });
const twoDecimals = new Intl.NumberFormat("tr-TR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const integer = new Intl.NumberFormat("tr-TR");

export const money = (v) => (v == null ? "—" : `€${oneDecimal.format(v / 1e6)} M`);
export const score = (v) => twoDecimals.format(v);
// null = ligde veri yok (örn. TFF 1. Lig'de xG)
export const pct = (v) => (v == null ? "—" : Math.round(v * 100));
export const int = (v) => (v == null ? "—" : integer.format(v));
export const foot = (f) => ({ Left: "Sol ayak", Right: "Sağ ayak", Both: "İki ayaklı" })[f] ?? "Ayak bilinmiyor";
export const monthYear = (d) =>
  d ? new Date(d).toLocaleDateString("tr-TR", { month: "short", year: "numeric" }) : "—";

const ESCAPES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
export const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ESCAPES[c]);
