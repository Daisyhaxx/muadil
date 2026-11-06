"""Standardize vektörler arasında Öklid uzaklığına dayalı benzerlik.

benzerlik = 1 − d² / (2n); d = Öklid uzaklığı, n = alan sayısı.
Standardize vektörlerde rastgele iki oyuncu için E[d²] ≈ 2n, yani benzerlik ≈ 0; aynı profil = 1.
Ölçek cosine'e yakın; sıralama Öklid uzaklığıyla birebir aynı.

Veri yok (NaN, örn. TFF'de xG): o alan o oyuncu çifti için atlanır, n = iki oyuncuda da verisi olan alan sayısı.
"""
import numpy as np
import pandas as pd


def standardize(matrix: pd.DataFrame) -> pd.DataFrame:
    """Z-skor. Havuzda sabit olan sütun → 0 (herkes ortalama). NaN (veri yok) korunur.

    Sezonda hiç gelmeyen alan (örn. 24/25'te outfielderBlocks) tamamen NaN kalır; çok sezonlu profilde
    o alan diğer sezondan gelir, tek sezonda benzerlikte atlanır. Eval de bu fonksiyonu kullanır.
    """
    matrix = matrix.astype(float)
    std = matrix.std()
    z = (matrix - matrix.mean()) / std.where(std > 0)
    z.loc[:, std == 0] = 0.0
    return z


def similarity_to(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    gaps = (matrix - query) ** 2
    present = np.count_nonzero(~np.isnan(gaps), axis=1)
    return 1 - np.nansum(gaps, axis=1) / (2 * present)
