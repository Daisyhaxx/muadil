"""Arama sonuçlarının metin çıktısı: sonuç tablosu + benzerlik açıklaması."""
import pandas as pd

from .explain import common_and_different

COLUMNS = ["player_name", "team_name", "league", "age", "positions_detailed",
           "minutesPlayed", "market_value_m", "similarity"]


def results_table(df: pd.DataFrame) -> str:
    view = df.assign(
        market_value_m=(df.market_value / 1e6).round(1),
        positions_detailed=df.positions_detailed.map(lambda p: ",".join(p) if p is not None else ""),
        age=df.age.astype("Int64"),
        similarity=df.similarity.round(3),
    )
    return view[COLUMNS].to_string(index=False)


def _pct(value: float) -> str:
    return "—" if pd.isna(value) else f"{value * 100:.0f}"


def _items(rows: pd.DataFrame) -> str:
    return " · ".join(f"{r.label} {_pct(r.query_pct)}/{_pct(r.candidate_pct)}"
                      for r in rows.itertuples())


def explanation_lines(explanation: pd.DataFrame) -> list[str]:
    """Percentile'lar sorgu/aday sırasıyla verilir."""
    common, different = common_and_different(explanation)
    lines = [f"   Ortak: {_items(common)}"]
    if len(different):
        lines.append(f"   Fark:  {_items(different)}")
    return lines
