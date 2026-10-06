"""Input validation and spreadsheet I/O."""

from pathlib import Path

import numpy as np
import pandas as pd


class DataError(ValueError):
    """User supplied data cannot be analysed."""


def sheets(path: str | Path) -> list[str]:
    with pd.ExcelFile(path) as workbook:
        return workbook.sheet_names


def read_table(path: str | Path, sheet: str | None = None) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        try:
            data = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
        except UnicodeDecodeError:
            data = pd.read_csv(path, sep=None, engine="python", encoding="cp1254")
    elif suffix in {".xlsx", ".xls"}:
        data = pd.read_excel(path, sheet_name=sheet or 0)
    else:
        raise DataError("unsupported_format")
    return validate(data)


def validate(frame: pd.DataFrame) -> pd.DataFrame:
    """Require species names and a finite, nonnegative integer abundance matrix."""
    if frame is None or frame.shape[0] == 0 or frame.shape[1] < 2:
        raise DataError("empty_table")
    if frame.columns[1:].isna().any() or frame.columns[1:].duplicated().any():
        raise DataError("duplicate_columns")

    data = frame.copy(deep=True)
    species = data.iloc[:, 0]
    if species.isna().any() or species.astype(str).str.strip().eq("").any():
        raise DataError("missing_species")
    data[data.columns[0]] = species.astype(str).str.strip()
    if data.iloc[:, 0].duplicated().any():
        raise DataError("duplicate_species")

    for column in data.columns[1:]:
        values = pd.to_numeric(data[column], errors="coerce")
        array = values.to_numpy(dtype=float)
        if not np.isfinite(array).all():
            raise DataError(f"invalid_number|{column}")
        if (array < 0).any() or (array != np.floor(array)).any():
            raise DataError(f"invalid_abundance|{column}")
        if not array.any():
            raise DataError(f"zero_site|{column}")
        data[column] = values.astype("int64")
    return data


def export_excel(frame: pd.DataFrame, path: str | Path) -> Path:
    target = Path(path).with_suffix(".xlsx")
    frame.to_excel(target, index=False, engine="xlsxwriter")
    return target
