"""İşlenmiş lig-sezon tablolarını yükler ve özellik tablosunu kurar."""
import pandas as pd

from .. import paths
from .feature_sets import STYLE_FIELDS
from .per90 import to_per90
from .percentile import add_percentiles
from .positions import add_position_group

SOFASCORE_DIR = paths.PROCESSED_DIR / "sofascore"
MIN_MINUTES = 900


def load_season(year: str) -> pd.DataFrame:
    """Bir sezonun çekilmiş tüm liglerini tek tabloda birleştirir."""
    files = sorted(SOFASCORE_DIR.glob(f"*_{year.replace('/', '-')}.parquet"))
    if not files:
        raise FileNotFoundError(f"{year} için tablo yok: {SOFASCORE_DIR}")
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)


def add_age(df: pd.DataFrame, on: pd.Timestamp | None = None) -> pd.DataFrame:
    on = on or pd.Timestamp.today().normalize()
    years = (on - df.date_of_birth).dt.days / 365.25
    return df.assign(age=years.floordiv(1))


def build_features(raw: pd.DataFrame, min_minutes: int = MIN_MINUTES) -> pd.DataFrame:
    df = raw[raw.minutesPlayed >= min_minutes].reset_index(drop=True)
    df = add_position_group(df)
    df = add_age(df)
    df = to_per90(df)
    return add_percentiles(df, STYLE_FIELDS)
