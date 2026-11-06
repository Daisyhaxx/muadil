"""Her istatistiği aynı lig-sezon + mevki grubu içinde percentile'a (0–1) çevirir.

Sonuç `pct_<alan>` sütunlarına yazılır; per-90 değerler açıklama için korunur.
"""
from collections.abc import Sequence

import pandas as pd

from .availability import unavailable

GROUP_KEYS = ["league", "season_year", "position_group"]
PREFIX = "pct_"


def pct_columns(fields: Sequence[str], prefix: str = PREFIX) -> list[str]:
    return [prefix + f for f in fields]


def add_percentiles(
    df: pd.DataFrame, fields: Sequence[str], keys: Sequence[str] = GROUP_KEYS, prefix: str = PREFIX
) -> pd.DataFrame:
    ranks = df.groupby(list(keys))[list(fields)].rank(pct=True)
    # Hesaplanamayan oran (örn. hiç dripling denemesi yok) → nötr.
    # Lig-sezonda hiç olmayan alan (örn. TFF'de xG) → NaN kalır, radarda "veri yok".
    ranks = ranks.fillna(0.5).mask(unavailable(df, fields))
    ranks.columns = pct_columns(fields, prefix)
    return pd.concat([df, ranks], axis=1)
