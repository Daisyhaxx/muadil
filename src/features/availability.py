"""Lig-sezonda hiç gelmeyen alanlar: veri yok (NaN), 0 değil. Örn. TFF 1. Lig'de xG/xA.

Oyuncu bazındaki eksik değerin anlamı farklıdır: şutu olmayan oyuncuda expectedGoals gelmez (= 0),
dripling denemesi olmayanda başarı yüzdesi hesaplanamaz (= nötr).
"""
from collections.abc import Sequence

import pandas as pd

SOURCE_KEYS = ["league", "season_year"]


def unavailable(df: pd.DataFrame, fields: Sequence[str]) -> pd.DataFrame:
    """True = alan, oyuncunun lig-sezonunda hiçbir oyuncuda yok."""
    return df.groupby(SOURCE_KEYS)[list(fields)].transform("count") == 0
