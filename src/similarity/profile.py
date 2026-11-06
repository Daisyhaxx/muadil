"""Arama profili: güncel sezon + önceki sezon, dakika × yenilik ağırlıklı ortalama (`src/features/history.py`).

Eval (results/history_eval.md): 2 sezonluk profil tek sezona göre lig içi MRR +0.027, geçmişi olanlarda +0.045.
3 sezon test edilmedi (22/23 verisi yok), bu yüzden varsayılan 1 önceki sezon.
Vektörler: her sezon kendi mevki grubunda standardize edilir, sonra ortalama alınır (eval ile aynı).
Gösterilen percentile'lar: aynı ağırlıklarla percentile ortalaması.
"""
import pandas as pd

from ..features.dataset import build_features, load_season
from ..features.feature_sets import STYLE_FIELDS, search_fields_for
from ..features.history import blend
from ..features.percentile import pct_columns
from .metric import standardize

HISTORY_SEASONS = 1
DECAY = 0.5  # önceki sezonun ağırlık çarpanı (dakikayla birlikte)


def previous_years(year: str, count: int) -> list[str]:
    """Örn. "25/26", 2 → ["24/25", "23/24"]."""
    start, end = (int(part) for part in year.split("/"))
    return [f"{start - k:02d}/{end - k:02d}" for k in range(1, count + 1)]


def load_history(year: str, count: int, min_minutes: int) -> dict[str, pd.DataFrame]:
    """Önceki sezonların özellik tabloları, yeniden eskiye. Verisi olmayan sezon atlanır."""
    history = {}
    for past in previous_years(year, count):
        try:
            history[past] = build_features(load_season(past), min_minutes)
        except FileNotFoundError:
            continue
    return history


def _align(rows: pd.DataFrame, past: pd.DataFrame, values: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Önceki sezon değerlerini güncel satırlara player_id + mevki grubuyla eşler.

    Oyuncunun o sezonda iki satırı varsa (iki ligde oynamış) en çok dakikalı olan alınır.
    """
    keyed = past[["player_id", "position_group", "minutesPlayed"]].join(values)
    keyed = keyed.sort_values("minutesPlayed").drop_duplicates(["player_id", "position_group"], keep="last")
    merged = rows[["player_id", "position_group"]].merge(keyed, how="left", on=["player_id", "position_group"])
    merged.index = rows.index
    return merged[values.columns], merged.minutesPlayed


def group_vectors(
    features: pd.DataFrame, history: list[pd.DataFrame], group: str, decay: float = DECAY
) -> pd.DataFrame:
    """Mevki grubunun arama vektörleri (satır indeksi = features indeksi). Filtrelerden önce, tüm havuzda."""
    columns = pct_columns(search_fields_for(group))
    rows = features[features.position_group == group]
    current = standardize(rows[columns])
    frames, minutes = [current], [rows.minutesPlayed]
    for past in history:
        past_rows = past[past.position_group == group]
        frame, mins = _align(rows, past_rows, standardize(past_rows[columns]))
        frames.append(frame)
        minutes.append(mins)
    return blend(frames, minutes, decay)


def blended_percentiles(features: pd.DataFrame, history: list[pd.DataFrame], decay: float = DECAY) -> pd.DataFrame:
    """Radar ve açıklamada gösterilen percentile'lar (`pct_<alan>`), vektörlerle aynı ağırlıklarla."""
    columns = pct_columns(STYLE_FIELDS)
    frames, minutes = [features[columns]], [features.minutesPlayed]
    for past in history:
        frame, mins = _align(features, past, past[columns])
        frames.append(frame)
        minutes.append(mins)
    return blend(frames, minutes, decay)
