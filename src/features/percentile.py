"""Her istatistiği aynı lig-sezon + mevki grubu içinde percentile'a (0–1) çevirir.

Sonuç `pct_<alan>` sütunlarına yazılır; per-90 değerler açıklama için korunur.
"""
from collections.abc import Sequence

import numpy as np
import pandas as pd

from .availability import unavailable

GROUP_KEYS = ["league", "season_year", "position_group"]
PREFIX = "pct_"


def pct_columns(fields: Sequence[str], prefix: str = PREFIX) -> list[str]:
    return [prefix + f for f in fields]


def _placed_in_reference(
    others: pd.DataFrame, basis: pd.DataFrame, keys: list[str], fields: list[str]
) -> pd.DataFrame:
    """Referans dışı oyuncuların referans dağılımındaki yeri; referansın kendi sıraları değişmez."""
    groups = dict(iter(basis.groupby(keys)))
    placed = pd.DataFrame(np.nan, index=others.index, columns=fields)
    for key, rows in others.groupby(keys):
        reference = groups.get(key)
        if reference is None:
            continue
        for field in fields:
            scale = np.sort(reference[field].dropna().to_numpy(dtype=float))
            values = rows[field].to_numpy(dtype=float)
            if len(scale):
                ranks = np.searchsorted(scale, values, side="right") / len(scale)
                placed.loc[rows.index, field] = np.where(np.isnan(values), np.nan, ranks)
    return placed


def add_percentiles(
    df: pd.DataFrame, fields: Sequence[str], keys: Sequence[str] = GROUP_KEYS, prefix: str = PREFIX,
    reference: pd.Series | None = None,
) -> pd.DataFrame:
    """`reference` verilirse sıralama sadece bu oyuncular arasında yapılır, diğerleri onların ölçeğine yerleşir."""
    keys, fields = list(keys), list(fields)
    basis = df if reference is None else df[reference]
    ranks = basis.groupby(keys)[fields].rank(pct=True)
    if len(basis) < len(df):
        others = df.drop(basis.index)
        ranks = pd.concat([ranks, _placed_in_reference(others, basis, keys, fields)]).reindex(df.index)
    # Hesaplanamayan oran (örn. hiç dripling denemesi yok) → nötr.
    # Lig-sezonda hiç olmayan alan (örn. TFF'de xG) → NaN kalır, radarda "veri yok".
    ranks = ranks.fillna(0.5).mask(unavailable(df, fields))
    ranks.columns = pct_columns(fields, prefix)
    return pd.concat([df, ranks], axis=1)
