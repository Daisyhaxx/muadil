"""Arama sonuçlarının metin çıktısı: sonuç tablosu + benzerlik açıklaması."""
import pandas as pd

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


def explanation_lines(explanation: pd.DataFrame, common: int = 5, different: int = 3) -> list[str]:
    """Percentile'lar sorgu/aday sırasıyla verilir."""
    ranked = explanation.sort_values("contribution", ascending=False)
    lines = [f"   Ortak: {_items(ranked.head(common))}"]
    diffs = ranked[ranked.contribution < 0].tail(different).iloc[::-1]
    if len(diffs):
        lines.append(f"   Fark:  {_items(diffs)}")
    return lines
