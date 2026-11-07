"""Ligler arası arama: lig farkının ne kadarı çıkarılsın (α)? Mevcut yöntemin α ızgarası + lig yanlılığı.

x' = log(1 + x) − α · (μ_lig − μ_havuz)  (`src/features/league_adjust.py`), sonra z-skor + cosine.
Lig yanlılığı: son sezonda filtresiz arama, ilk 10 sonucun ne kadarı sorgunun liginden. Havuzdaki pay = yansız.
Çalıştır: python -m src.eval.league_eval --out results/league_eval.md
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .bootstrap import format_difference, mrr_difference
from .pairwise import SIMILARITY
from .report import markdown_table
from .retrieval import SeasonPair, season_table, standardize, target_ranks
from .run_eval import DEFAULT_PAIRS
from .variants import BASELINE, PREVIOUS, Variant

ALPHAS = (0.0, 0.25, 0.5, 0.75, 1.0)
TOP = 10


def own_league_share(table: pd.DataFrame, variant: Variant, top: int = TOP) -> tuple[float, float]:
    """(ilk `top` sonuçta sorgunun liginden olanların payı, havuzdaki payı) — tüm oyuncular sorgu."""
    shares, expected = [], []
    for group, rows in table.groupby("position_group"):
        v = standardize(rows, variant.columns(group))
        sim = SIMILARITY[variant.metric](v, v)
        np.fill_diagonal(sim, -np.inf)
        leagues = rows.league.to_numpy()
        best = np.argsort(-sim, axis=1)[:, :top]
        shares.append((leagues[best] == leagues[:, None]).mean(axis=1))
        counts = pd.Series(leagues).map(pd.Series(leagues).value_counts()).to_numpy()
        expected.append((counts - 1) / (len(rows) - 1))
    return float(np.concatenate(shares).mean()), float(np.concatenate(expected).mean())


def _mrr(ranks: pd.Series) -> str:
    return f"{(1 / ranks).mean():.3f}"


def summary_row(label: str, ranks: pd.DataFrame, reference: pd.DataFrame, bias: tuple[float, float]) -> dict:
    changed = ranks.changed_league.to_numpy()
    row = {"Yöntem": label, "Tümü": _mrr(ranks.league_rank), "Aynı lig": _mrr(ranks.league_rank[~changed]),
           "Lig değiştirdi": _mrr(ranks.league_rank[changed]),
           "Takım değiştirdi": _mrr(ranks.league_rank[ranks.changed_team.to_numpy()])}
    for pair in ranks.pair.unique():
        in_pair = (ranks.pair == pair).to_numpy()
        row[f"Lig değiştirdi {pair}"] = _mrr(ranks.league_rank[in_pair & changed])
    row["Lig değiştirdi · tüm-lig havuzu"] = _mrr(ranks["rank"][changed])
    row["Fark: lig değiştirdi"] = ("—" if ranks is reference else format_difference(
        mrr_difference(ranks.league_rank[changed], reference.league_rank[changed])))
    row[f"İlk {TOP}'da kendi ligi"] = f"{bias[0] * 100:.1f}%"
    return row


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    years = list(dict.fromkeys(y for pair in DEFAULT_PAIRS for y in pair))
    latest = years[-1]

    def pairs_for(tables: dict[str, pd.DataFrame]) -> list[SeasonPair]:
        return [SeasonPair(a, b, tables[a], tables[b]) for a, b in DEFAULT_PAIRS]

    def ranks_for(tables: dict[str, pd.DataFrame], variant: Variant) -> pd.DataFrame:
        return pd.concat([target_ranks(p, variant) for p in pairs_for(tables)], ignore_index=True)

    default = {y: season_table(y) for y in years}
    reference = ranks_for(default, PREVIOUS)
    rows = [summary_row(f"Önceki: {' · '.join(PREVIOUS.labels[1:])}", reference, reference,
                        own_league_share(default[latest], PREVIOUS))]
    for alpha in ALPHAS:
        tables = {y: season_table(y, league_weight=alpha) for y in years}
        label = f"α = {alpha:g}" + (" (mevcut)" if alpha == 0.5 else "")
        rows.append(summary_row(label, ranks_for(tables, BASELINE), reference,
                                own_league_share(tables[latest], BASELINE)))
    expected = own_league_share(default[latest], BASELINE)[1]

    text = (f"## Ligler arası arama: lig farkı düzeltmesi (α) · {' · '.join(BASELINE.labels)}\n\n"
            "Lig içi havuz MRR (sütunlar kesit). \"Tüm-lig havuzu\" = filtresiz arama, hedef lig değiştirmiş. "
            "Fark = önceki yönteme göre MRR farkı ve %95 bootstrap aralığı.\n"
            f"Son sütun: {latest}'da filtresiz arama, ilk {TOP} sonucun sorgunun liginden olan payı; "
            f"havuzdaki pay (yansız arama) {expected * 100:.1f}%.\n\n"
            + markdown_table(rows) + "\n")
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
