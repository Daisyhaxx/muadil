"""Takım etkisi: savunma alanlarının topa sahip olma düzeltmesi (β). Esneklik ölçümü + retrieval karşılaştırması.

1) Esneklik: aynı ligde takım değiştiren saha oyuncularında Δlog(istatistik) ~ Δlog(1 − p) eğimi
   (p = takımın topa sahip olma oranı). Standart PAdj eğimi 1 varsayar.
2) Retrieval: β = 0 (düzeltme yok), mevcut, 0,5 ve 1 (standart PAdj); lig içi havuz MRR.
Çalıştır: python -m src.eval.team_eval --out results/team_eval.md
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from ..features.team_adjust import DEFENSIVE_FIELDS, POSSESSION_ELASTICITY
from .bootstrap import RESAMPLES, format_difference, mrr_difference
from .report import markdown_table
from .retrieval import SeasonPair, season_table, target_ranks
from .run_eval import DEFAULT_PAIRS
from .variants import BASELINE

BETAS = (0.0, POSSESSION_ELASTICITY, 0.5, 1.0)
FLOOR = 0.05  # log(x + FLOOR): sıfır değerler için


def team_changers(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Ardışık iki sezonda aynı mevki grubunda, aynı ligde, takım değiştirmiş saha oyuncuları (satır = oyuncu-çift)."""
    parts = []
    for a, b in DEFAULT_PAIRS:
        m = tables[a].merge(tables[b], on=["player_id", "position_group"], suffixes=("_a", "_b"))
        parts.append(m.assign(pair=f"{a} → {b}"))
    m = pd.concat(parts, ignore_index=True)
    return m[(m.league_a == m.league_b) & (m.team_id_a != m.team_id_b) & (m.position_group != "goalkeeper")]


def _slope(x: np.ndarray, y: np.ndarray) -> float:
    x, y = x - x.mean(), y - y.mean()
    return float((x * y).sum() / (x**2).sum())


def elasticity(changers: pd.DataFrame, field: str, seed: int = 0) -> tuple[float, float, float, int]:
    """(eğim, %95 alt, %95 üst, n); bootstrap ile."""
    y = (np.log(changers[f"{field}_b"] + FLOOR) - np.log(changers[f"{field}_a"] + FLOOR)).to_numpy()
    x = (np.log(1 - changers.team_possession_b) - np.log(1 - changers.team_possession_a)).to_numpy()
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    idx = np.random.default_rng(seed).integers(0, len(x), (RESAMPLES // 5, len(x)))
    boot = [_slope(x[i], y[i]) for i in idx]
    return _slope(x, y), *np.quantile(boot, [0.025, 0.975]), len(x)


def elasticity_table(changers: pd.DataFrame) -> str:
    rows = []
    for field in DEFENSIVE_FIELDS:
        if changers[[f"{field}_a", f"{field}_b"]].notna().all(axis=1).sum() == 0:
            continue  # örn. outfielderBlocks: 24/25'te hiçbir ligde yok, her çiftte bir sezon eksik
        slope, low, high, n = elasticity(changers, field)
        row = {"Alan": field, "n": str(n), "Eğim": f"{slope:.2f} [{low:.2f}, {high:.2f}]"}
        for pair, part in changers.groupby("pair"):
            row[pair] = f"{elasticity(part, field)[0]:.2f}"
        rows.append(row)
    return markdown_table(rows)


def retrieval_table(years: list[str]) -> str:
    results = {}
    for beta in BETAS:
        tables = {y: season_table(y, possession_beta=beta) for y in years}
        pairs = [SeasonPair(a, b, tables[a], tables[b]) for a, b in DEFAULT_PAIRS]
        results[beta] = pd.concat([target_ranks(p, BASELINE) for p in pairs], ignore_index=True)
    base = results[0.0]
    changed_team, changed_league = base.changed_team.to_numpy(), base.changed_league.to_numpy()
    slices = {"Tümü": np.ones(len(base), bool), "Aynı takım": ~changed_team, "Takım değiştirdi": changed_team,
              "Takım değiştirdi · aynı lig": changed_team & ~changed_league}
    rows = []
    for beta, ranks in results.items():
        label = {0.0: "β = 0 (düzeltme yok)", 1.0: "β = 1 (standart PAdj)"}.get(beta, f"β = {beta:g}")
        row = {"Düzeltme": label + (" (mevcut)" if beta == POSSESSION_ELASTICITY else "")}
        row |= {f"{k} (n={m.sum()})": f"{(1 / ranks.league_rank[m]).mean():.3f}" for k, m in slices.items()}
        for name in ("Tümü", "Takım değiştirdi"):
            m = slices[name]
            row[f"Fark: {name}"] = "—" if beta == 0.0 else format_difference(
                mrr_difference(ranks.league_rank[m], base.league_rank[m]))
        rows.append(row)
    return markdown_table(rows)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    years = list(dict.fromkeys(y for pair in DEFAULT_PAIRS for y in pair))
    changers = team_changers({y: season_table(y, possession_beta=0.0) for y in years})
    change = (changers.team_possession_b - changers.team_possession_a).abs().mean()

    text = (f"## Takım etkisi: topa sahip olma düzeltmesi · {' · '.join(BASELINE.labels)}\n\n"
            "### Esneklik: savunma alanı ~ rakibin topa sahip olması\n\n"
            f"Aynı ligde takım değiştiren saha oyuncuları (n = {len(changers)} oyuncu-çift; topa sahip olma "
            f"değişimi ort. {change * 100:.1f} puan). Eğim = Δlog(istatistik) / Δlog(1 − p); standart PAdj 1 "
            "varsayar. Köşeli parantez: %95 bootstrap aralığı. `outfielderBlocks` 24/25'te olmadığı için "
            "ölçülemiyor (düzeltme yine uygulanıyor).\n\n"
            + elasticity_table(changers)
            + "\n\n### Retrieval: lig içi havuz MRR\n\n"
            "Savunma alanları × (0,5 / (1 − p))^β. Fark = β = 0'a göre MRR farkı, %95 bootstrap aralığı.\n\n"
            + retrieval_table(years) + "\n")
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
