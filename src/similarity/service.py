"""Arama servisi: özellik tablosunu bir kez kurar, mevki vektörlerini önbellekler. CLI ve API ortak kullanır."""
import pandas as pd

from ..features.dataset import MIN_MINUTES, build_features, load_season
from .engine import group_vectors, search
from .explain import explain
from .filters import Filters
from .lookup import find_players


class SimilarityService:
    def __init__(self, year: str = "25/26", min_minutes: int = MIN_MINUTES):
        self.year = year
        self.min_minutes = min_minutes
        self.features = build_features(load_season(year), min_minutes)
        self._vectors: dict[str, pd.DataFrame] = {}

    def vectors(self, group: str) -> pd.DataFrame:
        if group not in self._vectors:
            self._vectors[group] = group_vectors(self.features, group)
        return self._vectors[group]

    def group_of(self, index: int) -> str:
        return self.features.at[index, "position_group"]

    def row_for(self, player_id: int) -> int:
        """Oyuncunun satırı; sezonda iki ligde oynadıysa en çok dakikalı olanı."""
        rows = self.features[self.features.player_id == player_id]
        if rows.empty:
            raise KeyError(player_id)
        return int(rows.minutesPlayed.idxmax())

    def find(self, name: str) -> pd.DataFrame:
        return find_players(self.features, name)

    def similar(self, index: int, filters: Filters, top: int = 10) -> pd.DataFrame:
        return search(self.features, self.vectors(self.group_of(index)), index, filters, top)

    def explain(self, index: int, candidate_index: int) -> pd.DataFrame:
        group = self.group_of(index)
        if self.group_of(candidate_index) != group:
            raise ValueError("İki oyuncu farklı mevki gruplarında")
        return explain(self.features, self.vectors(group), index, candidate_index)

    def similarity(self, index: int, candidate_index: int) -> float:
        return float(self.explain(index, candidate_index).contribution.sum())
