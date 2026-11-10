"""Arama servisi: özellik tablosunu ve profili bir kez kurar, mevki vektörlerini önbellekler. CLI ve API ortak kullanır."""
import pandas as pd

from ..features.dataset import FLOOR_MINUTES, MIN_MINUTES, build_features, load_season, prepare_season
from ..features.shrinkage import stability_points
from .confidence import confidence
from .engine import search
from .explain import explain
from .filters import Filters
from .lookup import find_players
from .profile import DECAY, HISTORY_SEASONS, blended_percentiles, effective_minutes, group_vectors, load_history


class SimilarityService:
    def __init__(self, year: str = "25/26", min_minutes: int = FLOOR_MINUTES, history_seasons: int = HISTORY_SEASONS):
        self.year = year
        self.decay = DECAY
        reference = max(min_minutes, MIN_MINUTES)
        raw = load_season(year)
        self.history = load_history(year, history_seasons, reference)
        past = list(self.history.values())
        # Önceki sezon yoksa kararlılık ölçülemez; az dakikalılar düzeltilemeyeceği için alınmaz
        stability = stability_points(past[0], prepare_season(raw, reference)) if past else None
        self.min_minutes = min_minutes if past else reference
        features = build_features(raw, reference, floor=self.min_minutes, stability=stability)
        effective = effective_minutes(features, past, self.decay)
        self.features = features.assign(effective_minutes=effective, confidence=confidence(effective))
        self.percentiles = blended_percentiles(self.features, past, self.decay)
        self._vectors: dict[str, pd.DataFrame] = {}

    @property
    def profile_years(self) -> list[str]:
        """Profile giren sezonlar, yeniden eskiye."""
        return [self.year, *self.history]

    def vectors(self, group: str) -> pd.DataFrame:
        if group not in self._vectors:
            self._vectors[group] = group_vectors(self.features, list(self.history.values()), group, self.decay)
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
        return explain(self.percentiles, self.vectors(group), group, index, candidate_index)

    def similarity(self, index: int, candidate_index: int) -> float:
        return float(self.explain(index, candidate_index).contribution.sum())
