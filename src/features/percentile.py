"""Her istatistiği aynı lig-sezon + mevki grubu içinde percentile'a (0–1) çevirir.

Sonuç `pct_<alan>` sütunlarına yazılır; per-90 değerler açıklama için korunur.
"""
from collections.abc import Sequence

import pandas as pd

GROUP_KEYS = ["league", "season_year", "position_group"]
PREFIX = "pct_"


def pct_columns(fields: Sequence[str], prefix: str = PREFIX) -> list[str]:
    return [prefix + f for f in fields]


def add_percentiles(
    df: pd.DataFrame, fields: Sequence[str], keys: Sequence[str] = GROUP_KEYS, prefix: str = PREFIX
) -> pd.DataFrame:
    ranks = df.groupby(list(keys))[list(fields)].rank(pct=True)
    # Hesaplanamayan oran (örn. hiç dripling denemesi yok) → nötr
    ranks = ranks.fillna(0.5)
    ranks.columns = pct_columns(fields, prefix)
    return pd.concat([df, ranks], axis=1)
