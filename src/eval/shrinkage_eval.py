"""Az dakikalı oyuncular: alan bazlı shrinkage sezonlar arası testte (aynı oyuncu sonraki sezon bulunuyor mu?).

k çapraz kurulur: 24/25 → 25/26 testinde k 23/24 → 24/25'ten gelir, tersi de. Ölçek hep referanstan (900+ dk).
Havuz hedefin ligi. Çalıştır: python -m src.eval.shrinkage_eval --out results/shrinkage_eval.md
"""
import argparse
import sys
import warnings
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd

from ..features.dataset import MIN_MINUTES, build_features, load_season, prepare_season
from ..features.history import blend
from ..features.shrinkage import STABILITY_SCALE, stability_points
from ..similarity.metric import standardize
from ..similarity.profile import DECAY
from .bootstrap import format_difference, mrr_difference
from .metrics import summarize
from .pairwise import cosine
from .report import markdown_table
from .variants import BASELINE

LOWEST = 300
PAIRS = {"23/24 → 24/25": ("23/24", "24/25", ("24/25", "25/26")), "24/25 → 25/26": ("24/25", "25/26", ("23/24", "24/25"))}
Mask = Callable[[pd.DataFrame], pd.Series]


def band(low: int, high: int) -> Mask:
    return lambda d: d.minutesPlayed.between(low, high - 1)


def at_least(low: int) -> Mask:
    return lambda d: d.minutesPlayed >= low


FULL = at_least(MIN_MINUTES)
TESTS: dict[str, tuple[Mask, Mask, Mask]] = {
    "A · Sorgu 450–899 dk → hedef 900+, havuz 900+": (band(450, 900), FULL, FULL),
    "B · Sorgu 900+ → hedef 450–899 dk, havuz 450+": (FULL, band(450, 900), at_least(450)),
    "C · Sorgu 900+ → hedef 900+, havuz 450+ (az dakikalılar havuzu bozuyor mu?)": (FULL, FULL, at_least(450)),
    "A2 · Sorgu 300–449 dk → hedef 900+, havuz 900+": (band(300, 450), FULL, FULL),
    "B2 · Sorgu 900+ → hedef 300–449 dk, havuz 300+": (FULL, band(300, 450), at_least(300)),
}


def _same_k(points: pd.DataFrame) -> pd.DataFrame:
    return points.apply(lambda row: row.where(row.isna(), row.median()), axis=1)


# etiket → kararlılık tablosunu dönüştüren fonksiyon (None = düzeltme yok). `shrink_low_minutes` c = ¼ ile çarpar.
MODES: dict[str, Callable[[pd.DataFrame], pd.DataFrame] | None] = {
    "Düzeltme yok": None,
    "Tek k (tüm alanlara aynı)": lambda p: _same_k(p) / STABILITY_SCALE,
    "Alan bazlı k × 1": lambda p: p / STABILITY_SCALE,
    "Alan bazlı k × ½": lambda p: p * 0.5 / STABILITY_SCALE,
    "Alan bazlı k × ¼ (mevcut)": lambda p: p,
}


def table(raw: pd.DataFrame, stability: pd.DataFrame | None) -> pd.DataFrame:
    df = build_features(raw, MIN_MINUTES, floor=LOWEST, stability=stability)
    return df.sort_values("minutesPlayed", ascending=False).drop_duplicates("player_id")


def _z(rows: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    return standardize(rows[cols], rows.is_reference).set_axis(rows.player_id.to_numpy())


def ranks(queries: pd.DataFrame, targets: pd.DataFrame, q: Mask, t: Mask, p: Mask, vectors=_z) -> pd.DataFrame:
    """Sorgu başına hedefin hedef-ligi havuzundaki sırası; sıra sabit (mevki grubu, oyuncu) ki yöntemler eşleşsin."""
    parts = []
    for group, rows in queries.groupby("position_group"):
        cols = BASELINE.columns(group)
        next_rows = targets[targets.position_group == group]
        pool = next_rows[p(next_rows)]
        z_pool = _z(next_rows, cols).loc[pool.player_id].to_numpy()
        chosen = q(rows) & rows.player_id.isin(pool.loc[t(pool), "player_id"])
        if not chosen.any():
            continue
        z_query = vectors(rows, cols).set_axis(rows.player_id.to_numpy()).loc[rows.player_id[chosen]].to_numpy()
        target = pd.Series(np.arange(len(pool)), index=pool.player_id.to_numpy()).loc[rows.player_id[chosen]].to_numpy()
        sim = cosine(z_query, z_pool)
        ahead = sim > sim[np.arange(len(target)), target][:, None]
        same_league = pool.league.to_numpy()[target][:, None] == pool.league.to_numpy()[None, :]
        parts.append(pd.DataFrame({"group": group, "player_id": rows.player_id[chosen].to_numpy(),
                                   "rank": 1 + (ahead & same_league).sum(axis=1)}))
    return pd.concat(parts, ignore_index=True).sort_values(["group", "player_id"], ignore_index=True)


def test_rows(tables: dict[str, dict[str, pd.DataFrame]], name: str) -> list[dict]:
    q, t, p = TESTS[name]
    results = {mode: pd.concat([ranks(*tables[mode][pair], q, t, p).assign(pair=pair) for pair in PAIRS], ignore_index=True)
               for mode in MODES}
    base = results["Düzeltme yok"]
    rows = []
    for mode, r in results.items():
        s = summarize(r["rank"])
        rows.append({"Yöntem": mode, "n": str(s["n"]), "MRR": f"{s['MRR']:.3f}", "R@1": f"{s['R@1'] * 100:.1f}%",
                     "R@10": f"{s['R@10'] * 100:.1f}%",
                     "MRR farkı": "—" if r is base else format_difference(mrr_difference(r["rank"], base["rank"]))})
    return rows


def confidence_rows(raw: dict[str, pd.DataFrame], stability: pd.DataFrame) -> list[dict]:
    """Sorgu: 24/25 (450+), profil 23/24 ile iki sezonlu (uygulamadaki gibi); başarı efektif dakikaya göre."""
    query, target = table(raw["24/25"], stability), table(raw["25/26"], stability)
    past = build_features(raw["23/24"], MIN_MINUTES).sort_values("minutesPlayed").drop_duplicates("player_id", keep="last")

    def two_seasons(rows: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
        previous = past[past.position_group == rows.position_group.iloc[0]]
        frames = [_z(rows, cols), _z(previous, cols)]
        minutes = [rows.set_index("player_id").minutesPlayed, previous.set_index("player_id").minutesPlayed]
        return blend(frames, minutes, DECAY)

    r = ranks(query, target, at_least(450), FULL, FULL, two_seasons)
    current = query.set_index("player_id").minutesPlayed
    previous = past.set_index("player_id").minutesPlayed
    r["effective"] = r.player_id.map(current) + DECAY * r.player_id.map(previous).fillna(0)
    edges, labels = [450, 700, 900, 1200, 1800, 2700, np.inf], ["450–699", "700–899", "900–1199", "1200–1799", "1800–2699", "2700+"]
    r["band"] = pd.cut(r.effective, edges, right=False, labels=labels)
    return [{"Efektif dakika": b, "n": str(len(g)), "MRR": f"{(1 / g['rank']).mean():.3f}", "R@10": f"{(g['rank'] <= 10).mean() * 100:.1f}%"}
            for b, g in r.groupby("band", observed=True)]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path)
    return p.parse_args()


def main() -> int:
    warnings.filterwarnings("ignore", category=FutureWarning)
    args = parse_args()
    raw = {y: load_season(y) for y in ("23/24", "24/25", "25/26")}
    prepared = {y: prepare_season(r, MIN_MINUTES) for y, r in raw.items()}
    points = {name: stability_points(prepared[a], prepared[b]) for name, (_, _, (a, b)) in PAIRS.items()}

    tables = {mode: {name: (table(raw[n], transform(points[name]) if transform else None),
                            table(raw[n1], transform(points[name]) if transform else None))
                     for name, (n, n1, _) in PAIRS.items()}
              for mode, transform in MODES.items()}

    sections = ["## Az dakikalı oyuncular\n\nHavuz: hedefin ligi. MRR farkı: düzeltmesiz yönteme göre, %95 bootstrap güven aralığı.\n"]
    sections += [f"### {name}\n\n{markdown_table(test_rows(tables, name))}\n" for name in TESTS]
    sections.append("### Efektif dakikaya göre başarı\n\nSorgu 24/25 (450+ dk), iki sezonlu profil (23/24 ile), hedef 25/26, havuz 900+.\n\n"
                    + markdown_table(confidence_rows(raw, points["24/25 → 25/26"])) + "\n")
    text = "\n".join(sections)
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
