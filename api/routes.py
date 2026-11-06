"""API uç noktaları."""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.features.positions import GROUP_LABELS
from src.ingest.leagues import LEAGUE_NAMES
from src.similarity.filters import Filters
from src.similarity.service import SimilarityService

from .deps import get_service
from .schemas import CompareResponse, Meta, PlayerSummary, SimilarPlayer, SimilarResponse
from .serializers import common_and_different, contributions, player_summary

router = APIRouter(prefix="/api")
Service = Annotated[SimilarityService, Depends(get_service)]


def _row(service: SimilarityService, player_id: int) -> int:
    try:
        return service.row_for(player_id)
    except KeyError:
        raise HTTPException(404, f"Oyuncu yok ya da {service.min_minutes} dakikanın altında: {player_id}")


@router.get("/meta", response_model=Meta)
def meta(service: Service):
    present = set(service.features.league)
    return Meta(
        year=service.year,
        min_minutes=service.min_minutes,
        leagues={k: v for k, v in LEAGUE_NAMES.items() if k in present},
        position_groups=GROUP_LABELS,
    )


@router.get("/players", response_model=list[PlayerSummary])
def players(service: Service, q: Annotated[str, Query(min_length=2)], limit: int = 10):
    matches = service.find(q).nlargest(limit, "minutesPlayed")
    return [player_summary(row) for _, row in matches.iterrows()]


@router.get("/similar/{player_id}", response_model=SimilarResponse)
def similar(
    service: Service,
    player_id: int,
    top: Annotated[int, Query(ge=1, le=50)] = 10,
    max_age: int | None = None,
    league: Annotated[list[str] | None, Query()] = None,
    max_value: Annotated[float | None, Query(description="Milyon €")] = None,
    foot: str | None = None,
    contract_until: date | None = None,
):
    qi = _row(service, player_id)
    filters = Filters(
        max_age=max_age,
        leagues=league,
        max_value_eur=max_value * 1e6 if max_value is not None else None,
        foot=foot,
        contract_until=contract_until.isoformat() if contract_until else None,
    )
    results = []
    for ci, row in service.similar(qi, filters, top).iterrows():
        common, different = common_and_different(service.explain(qi, ci))
        results.append(SimilarPlayer(**player_summary(row).model_dump(), similarity=row.similarity,
                                     common=common, different=different))
    return SimilarResponse(query=player_summary(service.features.loc[qi]), results=results)


@router.get("/compare/{player_id}/{candidate_id}", response_model=CompareResponse)
def compare(service: Service, player_id: int, candidate_id: int):
    qi, ci = _row(service, player_id), _row(service, candidate_id)
    try:
        explanation = service.explain(qi, ci)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return CompareResponse(
        query=player_summary(service.features.loc[qi]),
        candidate=player_summary(service.features.loc[ci]),
        similarity=float(explanation.contribution.sum()),
        stats=contributions(explanation),
    )


@router.post("/reload", response_model=Meta)
def reload():
    """Yeni lig verisi inince servisi yeniden kurar."""
    get_service.cache_clear()
    return meta(get_service())
