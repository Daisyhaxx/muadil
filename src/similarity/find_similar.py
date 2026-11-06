"""Komut satırından benzer oyuncu arama.

Çalıştır: python -m src.similarity.find_similar "Orkun Kökçü" --max-age 23 --max-value 5
Radar:    ... --radar radar.png   (sorgu oyuncusu vs. 1. sonuç)
"""
import argparse
import sys
from pathlib import Path

from ..features.dataset import MIN_MINUTES
from ..ingest.leagues import TOURNAMENTS
from ..viz.radar import save_radar
from .filters import Filters
from .profile import HISTORY_SEASONS
from .report import explanation_lines, results_table
from .service import SimilarityService


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("name", help="Oyuncu adı (aksan/büyük harf fark etmez)")
    p.add_argument("--year", default="25/26")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--min-minutes", type=int, default=MIN_MINUTES)
    p.add_argument("--history", type=int, default=HISTORY_SEASONS,
                   help="Profile katılacak önceki sezon sayısı (0 = sadece --year)")
    p.add_argument("--max-age", type=int, help="Bu yaş dahil")
    p.add_argument("--league", nargs="+", choices=sorted(TOURNAMENTS))
    p.add_argument("--max-value", type=float, help="Milyon €")
    p.add_argument("--foot", choices=["Left", "Right", "Both"])
    p.add_argument("--contract-until", help="Bu tarihten önce sözleşmesi bitenler, örn. 2027-06-30")
    p.add_argument("--explain", type=int, default=3, help="İlk kaç sonuç açıklansın")
    p.add_argument("--radar", type=Path, help="Sorgu vs. 1. sonuç radarını bu PNG'ye kaydet")
    return p.parse_args()


def build_filters(args: argparse.Namespace) -> Filters:
    return Filters(
        max_age=args.max_age,
        leagues=args.league,
        max_value_eur=args.max_value * 1e6 if args.max_value is not None else None,
        foot=args.foot,
        contract_until=args.contract_until,
    )


def main() -> int:
    args = parse_args()
    service = SimilarityService(args.year, args.min_minutes, args.history)
    features = service.features
    profile = " + ".join(service.profile_years)

    matches = service.find(args.name)
    if len(matches) != 1:
        found = ", ".join(matches.player_name.head(10)) or "yok"
        print(f"'{args.name}' için {len(matches)} eşleşme ({args.min_minutes}+ dk): {found}")
        return 1

    qi = matches.index[0]
    q = features.loc[qi]
    results = service.similar(qi, build_filters(args), args.top)
    print(f"Sorgu: {q.player_name} ({q.team_name}, {q.league}, {q.position_group}, "
          f"{int(q.age)} yaş, {int(q.minutesPlayed)} dk) · profil: {profile}\n")
    if results.empty:
        print("Filtrelere uyan oyuncu yok.")
        return 0
    print(results_table(results))

    if args.explain:
        print("\nAçıklama (mevki içi percentile, sorgu/aday):")
    for rank, (ci, row) in enumerate(results.head(args.explain).iterrows(), 1):
        print(f"{rank}. {row.player_name} — benzerlik {row.similarity:.3f}")
        print("\n".join(explanation_lines(service.explain(qi, ci))))

    if args.radar:
        ci = results.index[0]
        e = service.explain(qi, ci)
        e = e[e.on_radar]
        c = features.loc[ci]
        save_radar(list(e.label), e.query_pct.to_numpy(), e.candidate_pct.to_numpy(),
                   (q.player_name, c.player_name),
                   f"{q.player_name} vs {c.player_name} · benzerlik {results.similarity.iloc[0]:.2f}",
                   args.radar, note=f"profil: {profile}")
        print(f"\nRadar: {args.radar.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
