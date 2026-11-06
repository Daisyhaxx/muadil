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
    on_radar: bool               # mevkiye özel radar setinde mi (aramada tüm alanlar kullanılıyor)
    query_pct: float | None      # 0–1, mevki içi percentile; None = ligde veri yok (örn. TFF'de xG)
    candidate_pct: float | None
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
    stats: list[StatContribution]  # aramadaki tüm alanlar; radar alanları radar sırasıyla önde
    common: list[StatContribution]
    different: list[StatContribution]


class Meta(BaseModel):
    year: str
    min_minutes: int
    leagues: dict[str, str]          # yalnızca verisi olan ligler
    position_groups: dict[str, str]
    profile_years: list[str]         # profile giren sezonlar, yeniden eskiye (örn. ["25/26", "24/25"])
    profile_decay: float             # önceki sezonun ağırlık çarpanı (dakikayla birlikte)
