"""Sorgu × aday benzerlik matrisleri. Büyük değer = daha benzer."""
import numpy as np


def _unit_rows(m: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    return m / np.where(norms == 0, 1, norms)


def cosine(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    return _unit_rows(q) @ _unit_rows(p).T


def pearson(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Satır ortalaması çıkarılmış cosine: genel seviyeden bağımsız, sadece profilin şekli."""
    return cosine(q - q.mean(axis=1, keepdims=True), p - p.mean(axis=1, keepdims=True))


def neg_euclidean(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    squared = (q**2).sum(axis=1)[:, None] + (p**2).sum(axis=1)[None, :] - 2 * q @ p.T
    return -np.sqrt(np.maximum(squared, 0))


SIMILARITY = {"cosine": cosine, "pearson": pearson, "euclidean": neg_euclidean}
