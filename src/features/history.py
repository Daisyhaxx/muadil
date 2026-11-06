"""Çok sezonlu profil: oyuncunun sezon vektörlerinin dakika (× yenilik) ağırlıklı ortalaması.

Vektörler her sezonun kendi havuzunda standardize edilmiş olmalı; sezonlar arası karıştırılan tek şey ortalama.
Bir sezonda NaN olan alan (örn. TFF'de xG) o sezon için atlanır, ağırlık diğer sezonlara kalır.
"""
from collections.abc import Sequence

import pandas as pd


def blend(frames: Sequence[pd.DataFrame], minutes: Sequence[pd.Series], decay: float) -> pd.DataFrame:
    """frames[0] = en yeni sezon, sonrakiler geriye doğru; hepsi player_id indeksli, aynı sütunlar.

    Sezon k'nin ağırlığı = dakika × decay**k. Sonuç frames[0]'ın oyuncuları için.
    """
    players = frames[0].index
    total = pd.DataFrame(0.0, index=players, columns=frames[0].columns)
    weight = total.copy()
    for k, (frame, mins) in enumerate(zip(frames, minutes)):
        frame = frame.reindex(players)
        w = mins.reindex(players).fillna(0) * decay**k
        total += frame.fillna(0).mul(w, axis=0)
        weight += frame.notna().mul(w, axis=0)
    return total / weight.where(weight > 0)
