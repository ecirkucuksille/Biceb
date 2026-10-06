from pathlib import Path

import pandas as pd
import pytest

from biceb.data import DataError, export_excel, read_table, validate


ROOT = Path(__file__).resolve().parent.parent


def test_sample_workbook_and_export_round_trip(tmp_path):
    frame = read_table(ROOT / "sampledata" / "Alfa_Bolluk.xlsx")
    assert frame.shape == (20, 9)
    assert frame.iloc[0, 0] == "S1"
    assert frame["OA1"].sum() == 139
    exported = export_excel(frame, tmp_path / "output.xls")
    assert exported.suffix == ".xlsx"
    assert pd.read_excel(exported).equals(frame)
    csv_path = tmp_path / "sample.csv"
    frame.to_csv(csv_path, index=False, encoding="utf-8-sig")
    assert read_table(csv_path).equals(frame)


@pytest.mark.parametrize(
    "data,code",
    [
        ({"Species": ["A"], "Site": [-1]}, "invalid_abundance"),
        ({"Species": ["A"], "Site": [0]}, "zero_site"),
        ({"Species": ["A"], "Site": ["bad"]}, "invalid_number"),
        ({"Species": ["A", "A"], "Site": [1, 2]}, "duplicate_species"),
    ],
)
def test_invalid_input_is_rejected(data, code):
    with pytest.raises(DataError, match=code):
        validate(pd.DataFrame(data))


def test_legacy_xls_is_readable():
    frame = read_table(ROOT / "sampledata" / "Alfa_Bolluk.xls")
    assert frame.shape[0] > 0
