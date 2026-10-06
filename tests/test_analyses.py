from pathlib import Path

import pandas as pd
import pytest

from biceb.core import ANALYSES, compute
from biceb.data import read_table
from Classes.GeneralComputations import GeneralComputations


ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def alpha_sample():
    return read_table(ROOT / "sampledata" / "Alfa_Bolluk.xlsx")


def test_known_alpha_results(alpha_sample):
    richness = compute("richness", alpha_sample)
    assert richness.loc[0, "OA1"] == 13
    assert richness.loc[1, "OA1"] == 139
    shannon = compute("shannon", alpha_sample)
    assert shannon.loc[0, "OA1"] == pytest.approx(2.40972, abs=1e-5)
    simpson = compute("simpson", alpha_sample)
    assert simpson.loc[0, "OA1"] == pytest.approx(0.90275, abs=1e-5)


def test_first_site_can_be_rarefaction_reference():
    frame = pd.DataFrame({"Species": ["A", "B", "C"], "Small": [1, 0, 1], "Large": [2, 1, 2]})
    result = compute("dependent", frame)
    assert result.loc[0, "Small E(S)"] == 1
    assert result.loc[0, "Large E(S)"] == pytest.approx(0.7, abs=1e-5)
    assert result.loc[1, "Large E(S)"] == pytest.approx(0.4, abs=1e-5)
    independent = compute("independent", frame)
    assert independent.loc[1, "Large E(Sn)"] == pytest.approx(1.8, abs=1e-5)
    assert independent.loc[1, "Large σ(Sn)"] == pytest.approx(0.4, abs=1e-5)


def test_reference_site_reports_presence_not_abundance(alpha_sample):
    result = compute("dependent", alpha_sample)
    # OA2 is the smallest site in this workbook; S2 has five individuals there.
    assert alpha_sample.loc[1, "OA2"] == 5
    assert result.loc[1, "OA2 E(S)"] == 1


def test_invalid_rarefaction_input_raises():
    calculator = GeneralComputations(pd.DataFrame({"Species": ["A"], "Site": [1]}))
    with pytest.raises(ValueError):
        calculator.getrarevalue(3, 2, 1)


def test_all_registered_analyses_run_on_reference_data(alpha_sample):
    for analysis in ANALYSES:
        result = compute(analysis.code, alpha_sample)
        assert isinstance(result, pd.DataFrame), analysis.code
        assert len(result) > 0, analysis.code
