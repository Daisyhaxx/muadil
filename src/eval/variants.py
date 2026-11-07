"""Karşılaştırılan yöntemler: feature seti × normalizasyon × benzerlik metriği."""
from dataclasses import dataclass
from itertools import product

from ..features.feature_sets import STYLE_FIELDS, fields_for, search_fields_for
from ..features.league_adjust import PREFIX as ADJUSTED_PREFIX
from ..features.percentile import PREFIX, pct_columns

# Lig ayrımı olmadan sezon + mevki grubu içinde percentile
SEASON_PREFIX = "pcts_"

# ad → (etiket, mevki grubu → alanlar)
FEATURE_SETS = {
    "position": ("Mevkiye özel", fields_for),
    "common": ("Ortak (tüm alanlar)", lambda group: STYLE_FIELDS),
    "search": ("Ortak − kaleci alanları", search_fields_for),
}
# ad → (etiket, sütun ön eki); ön eksiz = ham per-90 değer
NORMALIZATIONS = {
    "pct_league": ("Lig içi percentile", PREFIX),
    "pct_season": ("Ligler arası percentile", SEASON_PREFIX),
    "per90_z": ("Per-90 z-skor", ""),
    "log_adj": ("Log per-90, lig farkı ½", ADJUSTED_PREFIX),
}
METRICS = {"cosine": "Cosine", "pearson": "Pearson", "euclidean": "Öklid"}


@dataclass(frozen=True)
class Variant:
    feature_set: str
    normalization: str
    metric: str

    def columns(self, group: str) -> list[str]:
        fields = FEATURE_SETS[self.feature_set][1](group)
        return pct_columns(fields, NORMALIZATIONS[self.normalization][1])

    @property
    def labels(self) -> tuple[str, str, str]:
        return (FEATURE_SETS[self.feature_set][0], NORMALIZATIONS[self.normalization][0],
                METRICS[self.metric])


# Arayüz ve CLI'nin kullandığı yöntem (07.11.2026'dan beri)
BASELINE = Variant("search", "log_adj", "cosine")
# 06.11.2026 – 07.11.2026
PREVIOUS = Variant("search", "pct_league", "euclidean")
# İlk sürüm (06.11.2026'ya kadar)
FIRST = Variant("position", "pct_league", "cosine")

# README bulgularındaki eşleştirilmiş karşılaştırmalar: (etiket, a, b) → a − b
COMPARISONS = [
    ("Mevcut − önceki (lig içi percentile · Öklid)", BASELINE, PREVIOUS),
    ("Mevcut − ilk sürüm (mevkiye özel · lig içi percentile · cosine)", BASELINE, FIRST),
    ("Normalizasyon: log lig farkı ½ − lig içi percentile (cosine)",
     BASELINE, Variant("search", "pct_league", "cosine")),
    ("Normalizasyon: log lig farkı ½ − per-90 z (cosine)", BASELINE, Variant("search", "per90_z", "cosine")),
    ("Metrik: cosine − Öklid (log lig farkı ½)", BASELINE, Variant("search", "log_adj", "euclidean")),
    ("Metrik: cosine − Öklid (lig içi percentile)", Variant("search", "pct_league", "cosine"), PREVIOUS),
    ("Feature seti: 35 alan − mevkiye özel (log lig farkı ½ · cosine)",
     BASELINE, Variant("position", "log_adj", "cosine")),
    ("Kaleci alanlarını tutmak: tüm alanlar − mevcut", Variant("common", "log_adj", "cosine"), BASELINE),
]


def all_variants() -> list[Variant]:
    return [Variant(*combo) for combo in product(FEATURE_SETS, NORMALIZATIONS, METRICS)]
