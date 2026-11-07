"""İşlenmiş lig-sezon tablolarını yükler ve özellik tablosunu kurar."""
import pandas as pd

from .. import paths
from .feature_sets import STYLE_FIELDS
from .league_adjust import LEAGUE_WEIGHT, add_league_adjusted
from .per90 import to_per90
from .percentile import add_percentiles
from .positions import add_position_group
from .team_adjust import POSSESSION_ELASTICITY, possession_adjusted

SOFASCORE_DIR = paths.PROCESSED_DIR / "sofascore"
TEAMS_DIR = paths.PROCESSED_DIR / "sofascore_teams"
TEAM_KEYS = ["league", "season_year", "team_id"]
MIN_MINUTES = 900


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


def build_features(
    raw: pd.DataFrame,
    min_minutes: int = MIN_MINUTES,
    league_weight: float = LEAGUE_WEIGHT,
    possession_beta: float = POSSESSION_ELASTICITY,
) -> pd.DataFrame:
    df = raw[raw.minutesPlayed >= min_minutes].reset_index(drop=True)
    df = add_position_group(df)
    df = add_age(df)
    df = to_per90(df)
    df = add_percentiles(df, STYLE_FIELDS)  # radar ve açıklamada gösterilen: ham per-90'dan
    # Arama vektörleri: savunma alanları takım bağlamına göre, sonra log + lig farkı ½
    search_values = possession_adjusted(df, STYLE_FIELDS, possession_beta)
    return add_league_adjusted(df, search_values, league_weight)
