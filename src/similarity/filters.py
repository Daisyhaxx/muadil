"""Arama sonuçlarına uygulanan filtreler. Benzerlik uzayını değiştirmez, sadece sonuçları eler."""
from dataclasses import dataclass

import pandas as pd


@dataclass
class Filters:
    max_age: int | None = None             # bu yaş dahil
    leagues: list[str] | None = None
    max_value_eur: float | None = None
    foot: str | None = None                # Left / Right / Both
    contract_until: str | None = None      # bu tarihten önce bitenler, örn. "2027-06-30"

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        mask = pd.Series(True, index=df.index)
        if self.max_age is not None:
            mask &= df.age <= self.max_age
        if self.leagues:
            mask &= df.league.isin(self.leagues)
        if self.max_value_eur is not None:
            mask &= df.market_value <= self.max_value_eur
        if self.foot:
            mask &= df.preferred_foot.str.lower() == self.foot.lower()
        if self.contract_until:
            mask &= df.contract_until <= pd.Timestamp(self.contract_until)
        return df[mask]
