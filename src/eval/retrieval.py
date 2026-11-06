"""Sezonlar arası retrieval testi: sezon N profiliyle ara, aynı oyuncunun N+1 kaydı kaçıncı sırada?

Sorgu = iki sezonda da 900+ dk oynayan oyuncu. Aday havuzu = N+1'deki aynı mevki grubundaki herkes
(`rank`) ya da sadece hedefin ligindekiler (`league_rank`). Sorgunun N kaydı havuzda yok.
Vektörler her sezonun kendi mevki grubu içinde standardize edilir.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..features.dataset import MIN_MINUTES, build_features, load_season
from ..features.feature_sets import STYLE_FIELDS
from ..features.percentile import add_percentiles
from .pairwise import SIMILARITY
from .variants import SEASON_PREFIX, Variant


def season_table(year: str, min_minutes: int = MIN_MINUTES) -> pd.DataFrame:
    """Oyuncu başına tek satır (sezonda iki ligde oynadıysa en çok dakikalı olan)."""
    df = build_features(load_season(year), min_minutes)
    df = add_percentiles(df, STYLE_FIELDS, keys=["season_year", "position_group"], prefix=SEASON_PREFIX)
    return df.sort_values("minutesPlayed", ascending=False).drop_duplicates("player_id")


def standardize(df: pd.DataFrame, columns: list[str]) -> np.ndarray:
    """Z-skor. Eksik değer ve havuzda sabit olan sütun → 0 (nötr)."""
    m = df[columns].astype(float)
    m = m.fillna(m.mean())
    std = m.std()
    return ((m - m.mean()) / std.where(std > 0)).fillna(0).to_numpy()


@dataclass
class SeasonPair:
    year: str
    next_year: str
    season: pd.DataFrame
    next_season: pd.DataFrame

    @property
    def label(self) -> str:
        return f"{self.year} → {self.next_year}"


def target_ranks(pair: SeasonPair, variant: Variant) -> pd.DataFrame:
    """Her sorgu için hedefin sırası (1 = en benzer). Eşit benzerlikte hedef öne alınır."""
    parts = []
    for group, pool in pair.next_season.groupby("position_group"):
        cols = variant.columns(group)
        season = pair.season[pair.season.position_group == group]
        is_query = season.player_id.isin(pool.player_id).to_numpy()
        queries = season[is_query]

        sim = SIMILARITY[variant.metric](standardize(season, cols)[is_query], standardize(pool, cols))
        position = pd.Series(np.arange(len(pool)), index=pool.player_id.to_numpy())
        target = position.loc[queries.player_id].to_numpy()
        following = pool.iloc[target]
        ahead = sim > sim[np.arange(len(target)), target][:, None]
        # Havuz sadece hedefin N+1 ligi: lig seviyesinin (tempo, xG yokluğu ...) ayırt ediciliği elenir
        in_league = following.league.to_numpy()[:, None] == pool.league.to_numpy()[None, :]

        parts.append(pd.DataFrame({
            "pair": pair.label,
            "player_id": queries.player_id.to_numpy(),
            "position_group": group,
            "changed_league": queries.league.to_numpy() != following.league.to_numpy(),
            "changed_team": queries.team_id.to_numpy() != following.team_id.to_numpy(),
            "pool_size": len(pool),
            "rank": 1 + ahead.sum(axis=1),
            "league_pool_size": in_league.sum(axis=1),
            "league_rank": 1 + (ahead & in_league).sum(axis=1),
        }))
    return pd.concat(parts, ignore_index=True)
