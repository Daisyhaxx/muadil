"""Takım bağlamı: savunma aksiyonları rakibin topa sahip olma oranına göre düzeltilir (possession adjustment).

x' = x · (0,5 / (1 − p))^β;  p = takımın lig-sezon ortalaması topa sahip olma oranı (0–1).
Rakibi topu çok tutan takımın oyuncusu daha çok müdahale eder; bu oyuncunun değil takımın özelliği.

Standart PAdj β = 1 kullanır. Takım değiştiren oyuncularda ölçülen esneklik ~0,3 (savunma alanları, iki sezon
çiftinde kararlı); β = 1 aşırı düzeltiyor (`python -m src.eval.team_eval`, README). Topla oynanan alanlar
düzeltilmiyor: pas hacmi topa sahip olmayla artıyor ama orta, uzun top, çalım azalıyor; bu hacim değil oyun tarzı.
Takım verisi yoksa (p = NaN) değer değişmez.
"""
from collections.abc import Sequence

import pandas as pd

DEFENSIVE_FIELDS = [
    "tackles", "interceptions", "clearances", "outfielderBlocks", "ballRecovery",
    "possessionWonAttThird", "dribbledPast",
]
POSSESSION_ELASTICITY = 0.3  # β


def possession_adjusted(
    df: pd.DataFrame, fields: Sequence[str], beta: float = POSSESSION_ELASTICITY
) -> pd.DataFrame:
    """`fields` per-90 değerlerinin kopyası; savunma alanları `team_possession`'a göre ölçeklenmiş."""
    values = df[list(fields)].astype(float).copy()
    factor = ((0.5 / (1 - df.team_possession)) ** beta).fillna(1.0)
    defensive = [f for f in DEFENSIVE_FIELDS if f in values]
    values[defensive] = values[defensive].mul(factor, axis=0)
    return values
