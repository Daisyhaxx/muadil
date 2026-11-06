"""Çok sezonlu profil testi: sorgu profili = sezon N ve öncekilerin ağırlıklı ortalaması, hedef = N+1 (tek sezon).

Hedefin profiline N girmez (sızıntı olmasın diye havuz hep tek sezon). Geçmişi olmayan sorgunun vektörü değişmez.
Çalıştır: python -m src.eval.history_eval --out results/history_eval.md
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from ..features.history import blend
from .bootstrap import format_difference, mrr_difference
from .metrics import summarize
from .report import markdown_table
from .retrieval import QueryVectors, SeasonPair, season_table, standardize, target_ranks
from .variants import BASELINE

# etiket → eski sezon ağırlık çarpanı (None = tek sezon)
PROFILES: dict[str, float | None] = {
    "Tek sezon (mevcut)": None,
    "Çok sezon · sadece dakika ağırlıklı": 1.0,
    "Çok sezon · önceki sezon ×0.5": 0.5,
    "Çok sezon · önceki sezon ×0.25": 0.25,
}


def _standardized(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    return pd.DataFrame(standardize(df, cols), index=df.player_id.to_numpy(), columns=cols)


def history_vectors(history: list[pd.DataFrame], decay: float) -> QueryVectors:
    """Her sezon kendi mevki grubunda standardize edilir, sonra oyuncu bazında ağırlıklı ortalama alınır."""
    def vectors(season: pd.DataFrame, cols: list[str]) -> np.ndarray:
        group = season.position_group.iloc[0]
        pasts = [past[past.position_group == group] for past in history]
        frames = [_standardized(season, cols)] + [_standardized(p, cols) for p in pasts]
        minutes = [df.set_index("player_id").minutesPlayed for df in [season, *pasts]]
        return blend(frames, minutes, decay).to_numpy()
    return vectors


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--year", default="24/25", help="Sorgu sezonu N")
    p.add_argument("--next-year", default="25/26", help="Hedef sezon N+1")
    p.add_argument("--history", nargs="+", default=["23/24"], help="N'den önceki sezonlar, yeniden eskiye")
    p.add_argument("--out", type=Path)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    pair = SeasonPair(args.year, args.next_year, season_table(args.year), season_table(args.next_year))
    history = [season_table(y) for y in args.history]

    ranks = {}
    for name, decay in PROFILES.items():
        vectors = standardize if decay is None else history_vectors(history, decay)
        ranks[name] = target_ranks(pair, BASELINE, vectors).set_index("player_id")
    base = ranks["Tek sezon (mevcut)"]

    # Geçmişi olan = önceki sezonlardan birinde aynı mevki grubunda 900+ dk
    past = pd.concat(history)[["player_id", "position_group"]].drop_duplicates()
    has_history = base.reset_index().merge(past, how="left", indicator=True)["_merge"].eq("both").to_numpy()
    subsets = {"Tümü": has_history | True, "Geçmişi olan": has_history,
               "Geçmişi olan · takım değiştirdi": has_history & base.changed_team.to_numpy()}

    rows = []
    for name, r in ranks.items():
        summary = summarize(r.league_rank)
        row = {"Profil": name} | {k: f"{summary[k] * 100:.1f}%" for k in ("R@1", "R@5", "R@10")}
        row["MRR"] = f"{summary['MRR']:.3f}"
        for label, mask in subsets.items():
            diff = mrr_difference(r.league_rank[mask], base.league_rank[mask])
            row[f"Fark: {label} (n={mask.sum()})"] = "—" if r is base else format_difference(diff)
        rows.append(row)

    text = (f"## Çok sezonlu profil · {pair.label} (geçmiş: {', '.join(args.history)}) · "
            f"{' · '.join(BASELINE.labels)} · havuz: hedefin ligi\n\n"
            "Fark = MRR farkı (tek sezona göre) ve %95 bootstrap güven aralığı.\n\n"
            + markdown_table(rows) + "\n")
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
