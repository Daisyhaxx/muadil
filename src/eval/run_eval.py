"""Sezonlar arası retrieval testi: tüm yöntemleri karşılaştırıp markdown tablo basar.

Çalıştır: python -m src.eval.run_eval
          python -m src.eval.run_eval --pairs 24/25:25/26 --out results/retrieval.md
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

from ..features.dataset import MIN_MINUTES
from .metrics import summarize
from .report import breakdown_table, comparison_table
from .retrieval import SeasonPair, season_table, target_ranks
from .variants import BASELINE, all_variants

DEFAULT_PAIRS = [("23/24", "24/25"), ("24/25", "25/26")]


def parse_pair(text: str) -> tuple[str, str]:
    year, sep, next_year = text.partition(":")
    if not sep:
        raise argparse.ArgumentTypeError(f"Geçersiz: {text!r} (örn. 24/25:25/26)")
    return year, next_year


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pairs", nargs="+", type=parse_pair, default=DEFAULT_PAIRS, metavar="N:N+1")
    p.add_argument("--min-minutes", type=int, default=MIN_MINUTES)
    p.add_argument("--out", type=Path, help="Markdown çıktısını bu dosyaya da yaz")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    years = dict.fromkeys(year for pair in args.pairs for year in pair)
    tables = {year: season_table(year, args.min_minutes) for year in years}
    pairs = [SeasonPair(a, b, tables[a], tables[b]) for a, b in args.pairs]

    results = {v: pd.concat([target_ranks(p, v) for p in pairs], ignore_index=True)
               for v in all_variants()}
    # Tüm-lig havuzu lig seviyesini koruyan yöntemleri ödüllendiriyor; seçim lig içi havuza göre
    best = max(results, key=lambda v: summarize(results[v]["league_rank"])["MRR"])
    labels = [p.label for p in pairs]

    sections = [
        "## Yöntem karşılaştırması — havuz: tüm ligler",
        comparison_table(results, labels),
        "## Yöntem karşılaştırması — havuz: sadece hedefin ligi",
        comparison_table(results, labels, rank="league_rank", pool_size="league_pool_size"),
        f"## Kırılım: mevcut yöntem ({' · '.join(BASELINE.labels)})",
        breakdown_table(results[BASELINE]),
    ]
    if best != BASELINE:
        sections += [f"## Kırılım: en iyi yöntem ({' · '.join(best.labels)})", breakdown_table(results[best])]
    text = "\n\n".join(sections) + "\n"

    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
