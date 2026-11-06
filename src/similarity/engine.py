"""Benzer oyuncu arama: aynı mevki grubu içinde cosine, sonra filtreler."""
import pandas as pd

from ..features.feature_sets import fields_for
from ..features.percentile import pct_columns
from .cosine import cosine_to, standardize
from .filters import Filters


def group_vectors(features: pd.DataFrame, group: str) -> pd.DataFrame:
    """Mevki grubunun standardize vektörleri. Filtrelerden önce, tüm havuzda hesaplanır."""
    pool = features[features.position_group == group]
    return standardize(pool[pct_columns(fields_for(group))])


def search(
    features: pd.DataFrame, vectors: pd.DataFrame, query_index: int, filters: Filters, top: int = 10
) -> pd.DataFrame:
    similarity = cosine_to(vectors.loc[query_index].to_numpy(), vectors.to_numpy())
    results = features.loc[vectors.index].assign(similarity=similarity)
    results = results[results.player_id != features.at[query_index, "player_id"]]
    return filters.apply(results).nlargest(top, "similarity")
