"""DataFrame satırlarını API modellerine çevirir (NaN/NaT → None)."""
import pandas as pd

from src.similarity.explain import common_and_different as split_explanation

from .schemas import PlayerSummary, StatContribution


def _value(x):
    return None if pd.isna(x) else x


def player_summary(row: pd.Series) -> PlayerSummary:
    positions = row.positions_detailed
    contract = _value(row.contract_until)
    age = _value(row.age)
    return PlayerSummary(
        player_id=int(row.player_id),
        name=row.player_name,
        team=row.team_name,
        league=row.league,
        position_group=row.position_group,
        positions=list(positions) if positions is not None else [],
        age=int(age) if age is not None else None,
        minutes=int(row.minutesPlayed),
        effective_minutes=int(row.effective_minutes),
        confidence=row.confidence,
        market_value=_value(row.market_value),
        preferred_foot=_value(row.preferred_foot),
        contract_until=contract.date() if contract is not None else None,
    )


def contributions(explanation: pd.DataFrame) -> list[StatContribution]:
    return [StatContribution(**{k: _value(r[k]) for k in StatContribution.model_fields})
            for r in explanation.to_dict("records")]


def common_and_different(explanation: pd.DataFrame) -> tuple[list, list]:
    common, different = split_explanation(explanation)
    return contributions(common), contributions(different)
