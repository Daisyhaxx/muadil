"""Az dakikalı oyuncular: per-90 değerleri mevki ortalamasına doğru, alan bazında çekilir.

x̂ = w · x + (1 − w) · μ,  w = m / (m + c · k)
m = dakika, μ = referans oyuncuların aynı lig-sezon + mevki ortalaması, k = alanın kararlılık noktası (dakika).

k, referans oyuncuların iki ardışık sezonundaki korelasyondan gelir: r = m / (m + k). Hava topu ~500 dk'da otururken
gol ~2300 dk ister. Alan bazlı olması şart: tek k bütün vektörü aynı oranda küçültür, cosine de ölçeği sildiği için
sıralama iyileşmez. c = ¼ çünkü sezonlar arası korelasyon oyuncunun gerçek değişimini de içerir, gürültüyü olduğundan
büyük gösterir (`python -m src.eval.shrinkage_eval`, README). Referans oyunculara dokunulmaz.
"""
from collections.abc import Sequence

import numpy as np
import pandas as pd

from .feature_sets import STYLE_FIELDS
from .percentile import GROUP_KEYS

STABILITY_SCALE = 0.25  # c
MIN_PAIRS = 30          # bir mevki grubunda k ölçmek için gereken oyuncu
CORRELATION_RANGE = (0.02, 0.98)


def _within_league(df: pd.DataFrame, fields: Sequence[str]) -> pd.DataFrame:
    """Oyuncu başına tek satır (en çok dakikalı), alanlar lig ortalamasından sapma olarak."""
    df = df.sort_values("minutesPlayed").drop_duplicates("player_id", keep="last")
    values = df[list(fields)].astype(float)
    deviations = values - values.groupby(df.league).transform("mean")
    return pd.concat([df[["player_id", "minutesPlayed"]], deviations], axis=1)


def _point(x: pd.Series, y: pd.Series, minutes: pd.Series) -> float:
    present = x.notna() & y.notna()
    if present.sum() < MIN_PAIRS or x[present].std() == 0 or y[present].std() == 0:
        return np.nan  # ölçülemedi: bu alan düzeltilmez
    r = np.clip(np.corrcoef(x[present], y[present])[0, 1], *CORRELATION_RANGE)
    return float(minutes[present].mean() * (1 - r) / r)


def stability_points(earlier: pd.DataFrame, later: pd.DataFrame, fields: Sequence[str] = STYLE_FIELDS) -> pd.DataFrame:
    """İki ardışık sezonun referans oyuncularından k (dakika). Satır = mevki grubu, sütun = alan."""
    points = {}
    for group, rows in earlier.groupby("position_group"):
        pairs = _within_league(rows, fields).merge(
            _within_league(later[later.position_group == group], fields), on="player_id", suffixes=("_a", "_b"))
        minutes = 2 / (1 / pairs.minutesPlayed_a + 1 / pairs.minutesPlayed_b)  # harmonik ortalama
        points[group] = {f: _point(pairs[f"{f}_a"], pairs[f"{f}_b"], minutes) for f in fields}
    return pd.DataFrame.from_dict(points, orient="index", columns=list(fields))


def shrink_low_minutes(
    df: pd.DataFrame, points: pd.DataFrame, reference: pd.Series, scale: float = STABILITY_SCALE,
    fields: Sequence[str] = STYLE_FIELDS,
) -> pd.DataFrame:
    """Referans dışı oyuncuların `fields` per-90 değerleri düzeltilmiş kopya. NaN (veri yok) NaN kalır."""
    fields = list(fields)
    values = df[fields].astype(float)
    target = values.where(reference).groupby([df[k] for k in GROUP_KEYS]).transform("mean")
    k = points.reindex(index=df.position_group, columns=fields).to_numpy() * scale
    minutes = df.minutesPlayed.to_numpy(dtype=float)[:, None]
    weight = np.where(np.isnan(k), 1.0, minutes / (minutes + k))
    weight[reference.to_numpy()] = 1.0
    shrunk = weight * values + (1 - weight) * target
    out = df.copy()
    out[fields] = shrunk.where(target.notna(), values)
    return out
