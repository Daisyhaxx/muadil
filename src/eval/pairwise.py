"""Sorgu × aday benzerlik matrisleri. Büyük değer = daha benzer.

NaN = ligde veri yok (örn. TFF'de xG): o alan o çift için atlanır (arama servisiyle aynı, `src/similarity/metric.py`).
Cosine, servisteki gibi hesaplanır: satırlar birim vektöre (RMS = 1) çevrilir, sonra Öklid. Veri eksik değilse
sıralama klasik cosine ile birebir aynı.
"""
import numpy as np

from ..similarity.metric import unit_rows


def neg_euclidean(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    """−RMS fark, sadece iki oyuncuda da verisi olan alanlar üstünden."""
    q_has, p_has = (~np.isnan(q)).astype(float), (~np.isnan(p)).astype(float)
    q0, p0 = np.nan_to_num(q), np.nan_to_num(p)
    squared = (q0**2) @ p_has.T + q_has @ (p0**2).T - 2 * q0 @ p0.T
    shared = q_has @ p_has.T
    return -np.sqrt(np.maximum(squared, 0) / np.maximum(shared, 1))


def cosine(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    return neg_euclidean(unit_rows(q), unit_rows(p))


def _center_rows(m: np.ndarray) -> np.ndarray:
    present = np.count_nonzero(~np.isnan(m), axis=1)
    return m - (np.nansum(m, axis=1) / np.maximum(present, 1))[:, None]


def pearson(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Satır ortalaması çıkarılmış cosine: genel seviyeden bağımsız, sadece profilin şekli."""
    return cosine(_center_rows(q), _center_rows(p))


SIMILARITY = {"cosine": cosine, "pearson": pearson, "euclidean": neg_euclidean}
