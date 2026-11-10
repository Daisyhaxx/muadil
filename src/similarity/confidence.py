"""Profilin güveni: efektif dakika (güncel sezon + önceki sezon × 0,5) arttıkça oyuncu sonraki sezon daha iyi bulunuyor.

Eşikler ölçümden (`python -m src.eval.shrinkage_eval`): başarı dakikayla düzenli artıyor, README'de tablo var.
"""
import numpy as np
import pandas as pd

MEDIUM_MINUTES = 900
HIGH_MINUTES = 1800


def confidence(effective_minutes: pd.Series) -> pd.Series:
    """low / medium / high."""
    levels = pd.cut(effective_minutes, [-np.inf, MEDIUM_MINUTES, HIGH_MINUTES, np.inf], right=False,
                    labels=["low", "medium", "high"])
    return levels.astype(str)
