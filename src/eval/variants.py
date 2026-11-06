"""Karşılaştırılan yöntemler: feature seti × normalizasyon × benzerlik metriği."""
from dataclasses import dataclass
from itertools import product

from ..features.feature_sets import STYLE_FIELDS, fields_for, search_fields_for
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


# Arayüz ve CLI'nin kullandığı yöntem
BASELINE = Variant("search", "pct_league", "euclidean")
# 06.11.2026'ya kadar kullanılan yöntem
PREVIOUS = Variant("position", "pct_league", "cosine")

# README bulgularındaki eşleştirilmiş karşılaştırmalar: (etiket, a, b) → a − b
COMPARISONS = [
    ("Mevcut − eski (mevkiye özel · cosine)", BASELINE, PREVIOUS),
    ("Feature seti: tüm alanlar − mevkiye özel (lig içi · cosine)", Variant("common", "pct_league", "cosine"), PREVIOUS),
    ("Kaleci alanlarını tutmak: tüm alanlar − mevcut (Öklid)", Variant("common", "pct_league", "euclidean"), BASELINE),
    ("Normalizasyon: lig içi (Öklid) − per-90 z (cosine), tüm alanlar",
     Variant("common", "pct_league", "euclidean"), Variant("common", "per90_z", "cosine")),
    ("Metrik: Öklid − cosine (tüm alanlar, lig içi)",
     Variant("common", "pct_league", "euclidean"), Variant("common", "pct_league", "cosine")),
]


def all_variants() -> list[Variant]:
    return [Variant(*combo) for combo in product(FEATURE_SETS, NORMALIZATIONS, METRICS)]
