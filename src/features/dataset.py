"""İşlenmiş lig-sezon tablolarını yükler ve özellik tablosunu kurar."""
import pandas as pd

from .. import paths
from .feature_sets import STYLE_FIELDS
from .league_adjust import LEAGUE_WEIGHT, add_league_adjusted
from .per90 import to_per90
from .percentile import add_percentiles
from .positions import add_position_group
from .shrinkage import shrink_low_minutes
from .team_adjust import POSSESSION_ELASTICITY, possession_adjusted

SOFASCORE_DIR = paths.PROCESSED_DIR / "sofascore"
TEAMS_DIR = paths.PROCESSED_DIR / "sofascore_teams"
TEAM_KEYS = ["league", "season_year", "team_id"]
MIN_MINUTES = 900     # referans: ölçek (ortalama, std, percentile) bu oyunculardan gelir
FLOOR_MINUTES = 450   # aramaya girebilecek en az dakika; 450–899 dk düzeltilerek girer (`shrinkage.py`)


def _read_year(directory, year: str) -> pd.DataFrame:
    files = sorted(directory.glob(f"*_{year.replace('/', '-')}.parquet"))
    if not files:
        raise FileNotFoundError(f"{year} için tablo yok: {directory}")
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)


def load_teams(year: str) -> pd.DataFrame:
    """Takım başına bir satır: `TEAM_KEYS` + `team_possession` (0–1)."""
    teams = _read_year(TEAMS_DIR, year)
    return teams[TEAM_KEYS].assign(team_possession=teams.averageBallPossession / 100)


def load_season(year: str) -> pd.DataFrame:
    """Bir sezonun çekilmiş tüm ligleri tek tabloda, takımın topa sahip olma oranıyla (`team_possession`)."""
    players = _read_year(SOFASCORE_DIR, year)
    return players.merge(load_teams(year), how="left", on=TEAM_KEYS, validate="many_to_one")


def add_age(df: pd.DataFrame, on: pd.Timestamp | None = None) -> pd.DataFrame:
    on = on or pd.Timestamp.today().normalize()
    years = (on - df.date_of_birth).dt.days / 365.25
    return df.assign(age=years.floordiv(1))


def prepare_season(raw: pd.DataFrame, min_minutes: int) -> pd.DataFrame:
    """Dakika eşiği, mevki grubu, yaş ve per-90 değerler."""
    df = raw[raw.minutesPlayed >= min_minutes].reset_index(drop=True)
    return to_per90(add_age(add_position_group(df)))


def build_features(
    raw: pd.DataFrame,
    min_minutes: int = MIN_MINUTES,
    league_weight: float = LEAGUE_WEIGHT,
    possession_beta: float = POSSESSION_ELASTICITY,
    floor: int | None = None,
    stability: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """`min_minutes`+ oyuncular referanstır (`is_reference`): ölçek onlardan gelir, değerleri değişmez.

    `floor` verilirse tablo o dakikaya kadar iner; aradaki oyuncular `stability` ile düzeltilip referans ölçeğine oturur.
    """
    df = prepare_season(raw, min_minutes if floor is None else floor)
    reference = df.minutesPlayed >= min_minutes
    if stability is not None:
        df = shrink_low_minutes(df, stability, reference)
    df = add_percentiles(df, STYLE_FIELDS, reference=reference)  # radar ve açıklamada gösterilen: per-90'dan
    # Arama vektörleri: savunma alanları takım bağlamına göre, sonra log + lig farkı ½
    search_values = possession_adjusted(df, STYLE_FIELDS, possession_beta)
    return add_league_adjusted(df, search_values, league_weight, reference=reference).assign(is_reference=reference)
