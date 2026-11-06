"""Sayım istatistiklerini 90 dakikaya böler; oran alanları olduğu gibi kalır."""
import pandas as pd

from .availability import unavailable
from .feature_sets import COUNT_FIELDS


def to_per90(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # Oyuncuda gelmeyen alan = 0 (örn. şutu olmayanda expectedGoals gelmiyor).
    # Lig-sezonda hiç gelmeyen alan = veri yok, NaN kalır (örn. TFF 1. Lig'de xG/xA).
    counts = out[COUNT_FIELDS].fillna(0).mask(unavailable(out, COUNT_FIELDS))
    out[COUNT_FIELDS] = counts.div(out["minutesPlayed"] / 90, axis=0)
    return out
