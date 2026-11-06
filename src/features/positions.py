"""Sofascore mevki kodu → mevki grubu. Ana mevki = positionsDetailed'ın ilk elemanı."""
import pandas as pd

DETAILED_TO_GROUP = {
    "GK": "goalkeeper",
    "DC": "center_back",
    "DL": "fullback", "DR": "fullback",
    "DM": "central_mid", "MC": "central_mid", "AM": "central_mid",
    "LW": "winger", "RW": "winger", "ML": "winger", "MR": "winger",
    "ST": "forward",
}

GROUP_LABELS = {
    "forward": "Forvet",
    "winger": "Kanat",
    "central_mid": "Merkez orta saha",
    "fullback": "Bek",
    "center_back": "Stoper",
    "goalkeeper": "Kaleci",
}

# Detaylı mevki yoksa kaba mevkiden (G/D/M/F)
COARSE_TO_GROUP = {"G": "goalkeeper", "D": "center_back", "M": "central_mid", "F": "forward"}


def position_group(detailed, coarse: str | None) -> str | None:
    if detailed is None or not len(detailed) or detailed[0] not in DETAILED_TO_GROUP:
        return COARSE_TO_GROUP.get(coarse)
    # Kanat bekler [ML, DL] / [MR, DR] diye kodlanıyor
    if detailed[0] in ("ML", "MR") and {"DL", "DR"} & set(detailed):
        return "fullback"
    return DETAILED_TO_GROUP[detailed[0]]


def add_position_group(df: pd.DataFrame) -> pd.DataFrame:
    groups = [position_group(d, c) for d, c in zip(df.positions_detailed, df.position)]
    return df.assign(position_group=groups)
