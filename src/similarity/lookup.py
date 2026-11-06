"""İsimle oyuncu bulma (büyük/küçük harf ve aksan duyarsız: "kokcu" → Orkun Kökçü)."""
import unicodedata

import pandas as pd


def normalize(text: str) -> str:
    text = text.replace("ı", "i").replace("İ", "I")
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold().strip()


def find_players(df: pd.DataFrame, name: str) -> pd.DataFrame:
    target = normalize(name)
    names = df.player_name.map(normalize)
    exact = df[names == target]
    return exact if len(exact) else df[names.str.contains(target, regex=False)]
