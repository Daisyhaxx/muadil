"""Benzerliği istatistik bazında katkılara ayırır.

cos(q, c) = Σ q_i·c_i / (|q|·|c|) → i. istatistiğin katkısı q_i·c_i / (|q|·|c|), katkılar toplamı = benzerlik.
Pozitif katkı: ikisi de ortalamanın aynı tarafında (ortak özellik). Negatif: zıt taraflarda (fark).
"""
import numpy as np
import pandas as pd

from ..features.labels import label
from ..features.percentile import PREFIX


def explain(
    features: pd.DataFrame, vectors: pd.DataFrame, query_index: int, candidate_index: int
) -> pd.DataFrame:
    """Alan sırasıyla (radar sırası) döner; katkıya göre sıralamak için sort_values("contribution")."""
    q, c = vectors.loc[query_index], vectors.loc[candidate_index]
    norm = np.linalg.norm(q) * np.linalg.norm(c)
    fields = [col.removeprefix(PREFIX) for col in vectors.columns]
    return pd.DataFrame({
        "field": fields,
        "label": [label(f) for f in fields],
        "query_pct": features.loc[query_index, vectors.columns].to_numpy(dtype=float),
        "candidate_pct": features.loc[candidate_index, vectors.columns].to_numpy(dtype=float),
        "contribution": (q * c).to_numpy() / (norm or 1),
    })
