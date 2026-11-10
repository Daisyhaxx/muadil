"""Ligler arası karşılaştırılabilir değerler: log per-90, lig farkının yarısı çıkarılmış. Aramanın vektörleri bundan.

x' = log(1 + x) − α · (μ_lig − μ_havuz)
μ_lig = aynı lig-sezon + mevki grubunun ortalaması, μ_havuz = aynı sezon + mevki grubunun (tüm ligler) ortalaması.
Sayım alanları log ölçeğine alınır (çarpık dağılım, oranlar); oran alanları (%) olduğu gibi kalır.

α = 1: ligin seviyesi tamamen silinir (lig içi percentile gibi). α = 0: ham seviye kalır; aynı ligin oyuncuları
birbirine yakın düşer (lig parmak izi). α = 0,5'te filtresiz aramada sonuçların lig dağılımı havuzla aynı ve lig
değiştirenler en az α = 1 kadar iyi bulunuyor (`python -m src.eval.league_eval`, README).
"""
import numpy as np
import pandas as pd

from .feature_sets import PERCENT_FIELDS
from .percentile import GROUP_KEYS, pct_columns

PREFIX = "adj_"
POOL_KEYS = ["season_year", "position_group"]
LEAGUE_WEIGHT = 0.5  # α


def add_league_adjusted(
    df: pd.DataFrame, values: pd.DataFrame, alpha: float = LEAGUE_WEIGHT, prefix: str = PREFIX,
    reference: pd.Series | None = None,
) -> pd.DataFrame:
    """`values` (per-90, sütun = alan adı, df ile aynı indeks) → df'e `<prefix><alan>` sütunları.

    Grup anahtarları df'ten alınır. NaN (ligde veri yok, örn. TFF'de xG) NaN kalır.
    `reference` verilirse ortalamalar sadece bu oyunculardan hesaplanır.
    """
    fields = list(values.columns)
    x = values.astype(float).copy()
    counts = [f for f in fields if f not in PERCENT_FIELDS]
    x[counts] = np.log1p(x[counts])
    basis = x if reference is None else x.where(reference)
    league_mean = basis.groupby([df[k] for k in GROUP_KEYS]).transform("mean")
    pool_mean = basis.groupby([df[k] for k in POOL_KEYS]).transform("mean")
    adjusted = x - alpha * (league_mean - pool_mean)
    adjusted.columns = pct_columns(fields, prefix)
    return pd.concat([df, adjusted], axis=1)
