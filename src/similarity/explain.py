"""Benzerliği istatistik bazında katkılara ayırır.

benzerlik = 1 − Σ (q_i − c_i)² / (2n) = Σ katkı_i,  katkı_i = (1 − (q_i − c_i)² / 2) / n.
q, c = birim vektörler (RMS = 1, `metric.py`); benzerlik = cosine.
Pozitif katkı: iki oyuncu o istatistikte yakın. Negatif: aradaki fark √2'den büyük (vektör ölçeğinde).
Veri olmayan alanın katkısı 0; n = iki oyuncuda da verisi olan alan sayısı (`metric.py` ile aynı).

"Ortak yönler" yakın olanlar arasından ikisinin de belirgin olduğu (ortalamanın aynı tarafında, uzağında)
istatistiklerdir: sıralama q_i·c_i ile. İkisi de ortalama olan yakınlık bilgi vermediği için öne çıkmaz.
"""
import numpy as np
import pandas as pd

from ..features.feature_sets import fields_for
from ..features.labels import label
from ..features.percentile import pct_columns

COMMON_COUNT = 5
DIFFERENT_COUNT = 3


def _radar_first(fields: list[str], radar: list[str]) -> list[str]:
    """Radar alanları radar sırasıyla önde, kalanlar arkada."""
    order = {f: i for i, f in enumerate(radar)}
    return sorted(fields, key=lambda f: order.get(f, len(radar)))


def explain(
    percentiles: pd.DataFrame, vectors: pd.DataFrame, group: str, query_index: int, candidate_index: int
) -> pd.DataFrame:
    """Aramada kullanılan her alan için bir satır; `on_radar` = mevkiye özel radar setinde mi.

    vectors: arama vektörleri, sütun = alan adı (`profile.group_vectors`).
    percentiles: gösterilecek `pct_<alan>` değerleri (profil: güncel + önceki sezon ortalaması).
    """
    radar = fields_for(group)
    fields = _radar_first(list(vectors.columns), radar)
    columns = pct_columns(fields)
    q = vectors.loc[query_index, fields].to_numpy(dtype=float)
    c = vectors.loc[candidate_index, fields].to_numpy(dtype=float)
    gaps = (q - c) ** 2
    missing = np.isnan(gaps)  # iki oyuncudan birinin liginde veri yok → alan atlanır, katkı 0
    n = np.count_nonzero(~missing)
    return pd.DataFrame({
        "field": fields,
        "label": [label(f) for f in fields],
        "on_radar": [f in radar for f in fields],
        "query_pct": percentiles.loc[query_index, columns].to_numpy(dtype=float),
        "candidate_pct": percentiles.loc[candidate_index, columns].to_numpy(dtype=float),
        "contribution": np.where(missing, 0.0, (1 - gaps / 2) / n),
        "shared": np.nan_to_num(q * c),
    })


def common_and_different(
    explanation: pd.DataFrame, common: int = COMMON_COUNT, different: int = DIFFERENT_COUNT
) -> tuple[pd.DataFrame, pd.DataFrame]:
    close = explanation[(explanation.contribution > 0) & (explanation.shared > 0)]
    apart = explanation[explanation.contribution < 0]
    return close.nlargest(common, "shared"), apart.nsmallest(different, "contribution")
