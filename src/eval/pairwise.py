"""Sorgu × aday benzerlik matrisleri. Büyük değer = daha benzer.

NaN = ligde veri yok (örn. TFF'de xG). Cosine/Pearson'da 0 (ortalama) sayılır: çarpıma katkısı olmaz.
Öklid'de o alan o çift için atlanır (arama servisiyle aynı, `src/similarity/metric.py`).
"""
import numpy as np


def _unit_rows(m: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    return m / np.where(norms == 0, 1, norms)


def cosine(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    q, p = np.nan_to_num(q), np.nan_to_num(p)
    return _unit_rows(q) @ _unit_rows(p).T


def pearson(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Satır ortalaması çıkarılmış cosine: genel seviyeden bağımsız, sadece profilin şekli."""
    q, p = np.nan_to_num(q), np.nan_to_num(p)
    return cosine(q - q.mean(axis=1, keepdims=True), p - p.mean(axis=1, keepdims=True))


def neg_euclidean(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    """−RMS fark, sadece iki oyuncuda da verisi olan alanlar üstünden."""
    q_has, p_has = (~np.isnan(q)).astype(float), (~np.isnan(p)).astype(float)
    q0, p0 = np.nan_to_num(q), np.nan_to_num(p)
    squared = (q0**2) @ p_has.T + q_has @ (p0**2).T - 2 * q0 @ p0.T
    shared = q_has @ p_has.T
    return -np.sqrt(np.maximum(squared, 0) / np.maximum(shared, 1))


SIMILARITY = {"cosine": cosine, "pearson": pearson, "euclidean": neg_euclidean}
