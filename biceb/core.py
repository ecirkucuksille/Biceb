"""Qt-free entry point for the existing biodiversity calculations."""

from dataclasses import dataclass
from typing import Callable

import pandas as pd

from Classes.DataFrameForBigWindow import DataFrameForBigWindow
from Classes.PrepareDataFrame import PrepareDataFrame


@dataclass(frozen=True)
class Analysis:
    code: str
    title_key: str
    group_key: str
    legacy_id: int
    kind: str = "table"


ANALYSES = (
    Analysis("richness", "richness", "alpha", 1),
    Analysis("margalef", "margalef", "alpha", 2),
    Analysis("chao", "chao", "alpha", 3),
    Analysis("dependent", "dependent", "alpha", 1, "rarefaction"),
    Analysis("independent", "independent", "alpha", 2, "rarefaction"),
    Analysis("shannon", "shannon", "indices", 4),
    Analysis("brillouin", "brillouin", "indices", 5),
    Analysis("simpson", "simpson", "indices", 6),
    Analysis("mcintosh", "mcintosh", "indices", 7),
    Analysis("berger", "berger", "indices", 8),
    Analysis("qstat", "qstat", "abundance", 9),
    Analysis("logseries", "logseries", "abundance", 10),
    Analysis("lognormal", "lognormal", "abundance", 11),
    Analysis("jackknife", "jackknife", "abundance", 12),
    Analysis("she", "she", "abundance", 13),
    Analysis("presence_pair", "presence_pair", "beta", 14),
    Analysis("presence_all", "presence_all", "beta", 16),
    Analysis("abundance_pair", "abundance_pair", "beta", 15),
    Analysis("community_variance", "community_variance", "beta", 17),
    Analysis("simpson_beta", "simpson_beta", "beta", 18),
    Analysis("shannon_beta", "shannon_beta", "beta", 19),
    Analysis("shannon_exp", "shannon_exp", "beta", 20),
)

BY_CODE = {analysis.code: analysis for analysis in ANALYSES}


def compute(
    code: str,
    frame: pd.DataFrame,
    selected_columns: list[int] | None = None,
    progress: Callable[[int], None] | None = None,
) -> pd.DataFrame:
    """Run an analysis on a snapshot of a validated input table."""
    analysis = BY_CODE[code]
    data = frame.copy(deep=True)
    if code.startswith("presence_"):
        data.iloc[:, 1:] = (data.iloc[:, 1:] > 0).astype(int)
    if analysis.kind == "rarefaction":
        return DataFrameForBigWindow.createDataFrame(data, analysis.legacy_id, progress)
    return PrepareDataFrame.createDataFrame(data, analysis.legacy_id, selected_columns or [])
