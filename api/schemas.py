"""API cevap modelleri."""
from datetime import date

from pydantic import BaseModel


class PlayerSummary(BaseModel):
    player_id: int
    name: str
    team: str
    league: str
    position_group: str
    positions: list[str]
    age: int | None
    minutes: int
    market_value: float | None  # €
    preferred_foot: str | None
    contract_until: date | None


class StatContribution(BaseModel):
    field: str
    label: str
    query_pct: float      # 0–1, mevki içi percentile
    candidate_pct: float
    contribution: float   # toplamı = benzerlik


class SimilarPlayer(PlayerSummary):
    similarity: float
    common: list[StatContribution]
    different: list[StatContribution]


class SimilarResponse(BaseModel):
    query: PlayerSummary
    results: list[SimilarPlayer]


class CompareResponse(BaseModel):
    query: PlayerSummary
    candidate: PlayerSummary
    similarity: float
    stats: list[StatContribution]  # radar sırası


class Meta(BaseModel):
    year: str
    min_minutes: int
    leagues: dict[str, str]          # yalnızca verisi olan ligler
    position_groups: dict[str, str]
