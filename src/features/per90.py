"""Sayım istatistiklerini 90 dakikaya böler; oran alanları olduğu gibi kalır."""
import pandas as pd

from .feature_sets import COUNT_FIELDS


def to_per90(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # Gelmeyen sayım alanı = 0 (örn. şutu olmayan oyuncuda expectedGoals hiç gelmiyor)
    out[COUNT_FIELDS] = out[COUNT_FIELDS].fillna(0).div(out["minutesPlayed"] / 90, axis=0)
    return out
