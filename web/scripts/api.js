// Backend çağrıları. Boş parametreler gönderilmez; diziler tekrar eden parametre olur (?league=a&league=b).

async function get(path, params = {}) {
  const url = new URL(path, location.origin);
  for (const [key, value] of Object.entries(params)) {
    for (const v of [value].flat()) {
      if (v !== "" && v != null) url.searchParams.append(key, v);
    }
  }
  const res = await fetch(url);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(typeof body.detail === "string" ? body.detail : res.statusText);
  }
  return res.json();
}

export const getMeta = () => get("/api/meta");
export const searchPlayers = (q) => get("/api/players", { q });
export const getSimilar = (playerId, filters) => get(`/api/similar/${playerId}`, filters);
export const getCompare = (playerId, candidateId) => get(`/api/compare/${playerId}/${candidateId}`);
