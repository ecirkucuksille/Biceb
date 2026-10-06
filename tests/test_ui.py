import pandas as pd
from numbers import Integral
from PySide6 import QtCore, QtWidgets

from biceb.app import FrameModel, MainWindow
from biceb.data import read_table
from biceb.i18n import tr


def test_language_switch_and_edit_validation(qt_app):
    window = MainWindow()
    window.language_box.setCurrentIndex(0)
    assert window.windowTitle() == tr("tr", "app_title")
    window.language_box.setCurrentIndex(1)
    assert window.windowTitle() == tr("en", "app_title")

    model = FrameModel(pd.DataFrame({"Species": ["A"], "Site": [2]}), editable=True)
    cell = model.index(0, 1)
    assert not model.setData(cell, "-2", QtCore.Qt.ItemDataRole.EditRole)
    assert model.setData(cell, "3", QtCore.Qt.ItemDataRole.EditRole)
    assert model.frame.iat[0, 1] == 3
    assert isinstance(model.frame.iat[0, 1], Integral)
    window.close()


def test_background_analysis_creates_result_on_ui_thread(qt_app):
    from pathlib import Path

    window = MainWindow()
    sample = Path(__file__).resolve().parent.parent / "sampledata" / "Alfa_Bolluk.xlsx"
    window._replace_frame(read_table(sample))
    window.selected_code = "richness"
    window.run_analysis()
    loop = QtCore.QEventLoop()
    window.active_thread.finished.connect(loop.quit)
    QtCore.QTimer.singleShot(5000, loop.quit)
    loop.exec()
    assert window.active_thread is None
    assert len(window.results) == 1
    assert window.results[0].source.loc[0, "OA1"] == 13
    window.close()


import pytest


@pytest.fixture(scope="module")
def qt_app():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    yield app
