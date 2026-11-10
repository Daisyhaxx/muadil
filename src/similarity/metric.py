"""Benzerlik: birim vektörler arasında Öklid uzaklığından, sonuç cosine benzerliği.

Vektör = standardize (z-skor) değerler, sonra her satır RMS = 1 olacak şekilde ölçeklenir (`unit_rows`).
benzerlik = 1 − d² / (2n); d = Öklid uzaklığı, n = alan sayısı. RMS = 1 iken bu tam olarak cosine benzerliği:
rastgele iki oyuncu ≈ 0, aynı yönde profil = 1. Profilin büyüklüğü (oyuncunun ortalamadan genel olarak ne kadar
ayrıştığı) değil yönü (tarzı) karşılaştırılır; lig değiştiren oyuncuda büyüklük değişiyor, yön daha kararlı (README).

Veri yok (NaN, örn. TFF'de xG): o alan o oyuncu çifti için atlanır, n = iki oyuncuda da verisi olan alan sayısı.
"""
import numpy as np
import pandas as pd


def standardize(matrix: pd.DataFrame, reference: pd.Series | None = None) -> pd.DataFrame:
    """Z-skor. Havuzda sabit olan sütun → 0 (herkes ortalama). NaN (veri yok) korunur.

    Sezonda hiç gelmeyen alan (örn. 24/25'te outfielderBlocks) tamamen NaN kalır; çok sezonlu profilde
    o alan diğer sezondan gelir, tek sezonda benzerlikte atlanır. Eval de bu fonksiyonu kullanır.
    `reference` verilirse ortalama ve sapma sadece bu satırlardan gelir (az dakikalılar ölçeği değiştirmez).
    """
    matrix = matrix.astype(float)
    basis = matrix if reference is None else matrix[reference]
    std = basis.std()
    z = (matrix - basis.mean()) / std.where(std > 0)
    z.loc[:, std == 0] = 0.0
    return z


def unit_rows(matrix: np.ndarray) -> np.ndarray:
    """Her satırı RMS = 1 olacak şekilde ölçekler (verisi olan alanlar üstünden). Sıfır satır olduğu gibi kalır."""
    matrix = np.asarray(matrix, dtype=float)
    present = np.count_nonzero(~np.isnan(matrix), axis=1)
    rms = np.sqrt(np.nansum(matrix**2, axis=1) / np.maximum(present, 1))
    return matrix / np.where(rms > 0, rms, 1)[:, None]


def similarity_to(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    gaps = (matrix - query) ** 2
    present = np.count_nonzero(~np.isnan(gaps), axis=1)
    return 1 - np.nansum(gaps, axis=1) / (2 * present)
