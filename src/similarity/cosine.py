"""Standardize edilmiş vektörler üstünde cosine benzerliği."""
import numpy as np
import pandas as pd


def standardize(matrix: pd.DataFrame) -> pd.DataFrame:
    """Z-skor. Havuzda sabit olan sütunlar bilgi taşımadığı için atılır."""
    std = matrix.std()
    keep = std[std > 0].index
    return (matrix[keep] - matrix[keep].mean()) / std[keep]


def cosine_to(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1) * np.linalg.norm(query)
    return matrix @ query / np.where(norms == 0, 1, norms)
