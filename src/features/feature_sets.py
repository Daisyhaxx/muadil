"""Mevki grubuna göre oyuncu profiline giren istatistikler.

Profil = oyun tarzı: rating, dakika, maç sayısı ve kartlar dahil değil.
Birbirinin neredeyse aynısı olan alanlardan biri seçildi (örn. totalPasses var, accuratePasses yok).
Sıra radardaki eksen sırasıdır: şut → yaratıcılık → pas → top taşıma → savunma → ikili mücadele.
"""

FORWARD = [
    "goals", "expectedGoals", "totalShots", "shotsFromOutsideTheBox", "headedGoals", "offsides",
    "expectedAssists", "keyPasses", "bigChancesCreated",
    "touches", "accuratePassesPercentage",
    "successfulDribbles", "wasFouled", "dispossessed",
    "possessionWonAttThird", "ballRecovery",
    "aerialDuelsWon", "aerialDuelsWonPercentage", "groundDuelsWon",
]

WINGER = [
    "goals", "expectedGoals", "totalShots", "shotsFromOutsideTheBox",
    "expectedAssists", "keyPasses", "bigChancesCreated", "totalCross", "accurateCrosses",
    "accurateFinalThirdPasses", "accuratePassesPercentage",
    "successfulDribbles", "successfulDribblesPercentage", "touches", "wasFouled", "possessionLost",
    "tackles", "ballRecovery", "possessionWonAttThird",
]

CENTRAL_MID = [
    "expectedGoals", "totalShots", "shotsFromOutsideTheBox",
    "expectedAssists", "keyPasses", "bigChancesCreated",
    "totalPasses", "accuratePassesPercentage", "accurateFinalThirdPasses", "accurateLongBalls",
    "successfulDribbles", "wasFouled", "possessionLost",
    "tackles", "interceptions", "ballRecovery", "possessionWonAttThird", "dribbledPast",
    "groundDuelsWon", "aerialDuelsWon",
]

FULLBACK = [
    "expectedAssists", "keyPasses", "totalCross", "accurateCrosses", "accurateFinalThirdPasses",
    "totalPasses", "accuratePassesPercentage", "accurateLongBalls",
    "successfulDribbles", "possessionLost",
    "tackles", "interceptions", "clearances", "ballRecovery", "possessionWonAttThird", "dribbledPast",
    "groundDuelsWon", "groundDuelsWonPercentage", "aerialDuelsWon", "aerialDuelsWonPercentage",
]

CENTER_BACK = [
    "expectedGoals",
    "totalPasses", "accuratePassesPercentage", "accurateLongBalls",
    "accurateOppositionHalfPasses", "accurateFinalThirdPasses",
    "successfulDribbles", "possessionLost",
    "tackles", "tacklesWonPercentage", "interceptions", "clearances", "outfielderBlocks",
    "ballRecovery", "dribbledPast",
    "groundDuelsWon", "groundDuelsWonPercentage", "aerialDuelsWon", "aerialDuelsWonPercentage",
]

GOALKEEPER = [
    "saves", "savedShotsFromInsideTheBox", "goalsConceded",
    "highClaims", "punches", "crossesNotClaimed", "runsOut", "successfulRunsOut",
    "totalPasses", "accuratePassesPercentage", "totalLongBalls", "accurateLongBalls",
]

BY_GROUP = {
    "forward": FORWARD,
    "winger": WINGER,
    "central_mid": CENTRAL_MID,
    "fullback": FULLBACK,
    "center_back": CENTER_BACK,
    "goalkeeper": GOALKEEPER,
}

STYLE_FIELDS = list(dict.fromkeys(f for fields in BY_GROUP.values() for f in fields))

# 90 dakikaya bölünmeyecek oran alanları
PERCENT_FIELDS = [f for f in STYLE_FIELDS if f.endswith("Percentage")]
COUNT_FIELDS = [f for f in STYLE_FIELDS if f not in PERCENT_FIELDS]


# Sadece kalecide anlamlı. Saha oyuncusunda ya gürültü (nadir kurtarış) ya da takım sinyali:
# goalsConceded = oyuncu sahadayken yenen gol, oyun tarzını değil takımın savunmasını ölçer.
GOALKEEPER_ONLY = [
    "saves", "savedShotsFromInsideTheBox", "goalsConceded", "highClaims", "punches",
    "crossesNotClaimed", "runsOut", "successfulRunsOut",
]


def fields_for(group: str) -> list[str]:
    """Radar ve açıklamada gösterilen mevkiye özel set (sıra = radar ekseni)."""
    return BY_GROUP[group]


def search_fields_for(group: str) -> list[str]:
    """Aramada kullanılan set: tüm stil alanları, saha oyuncularında kaleci alanları hariç.

    Sezonlar arası değerlendirmede mevkiye özel setten iyi (README, Bulgular).
    """
    if group == "goalkeeper":
        return STYLE_FIELDS
    return [f for f in STYLE_FIELDS if f not in GOALKEEPER_ONLY]
