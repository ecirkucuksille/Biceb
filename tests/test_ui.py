import pandas as pd
from numbers import Integral
from PySide6 import QtCore, QtWidgets

from biceb.app import FrameModel, MainWindow, ResultWindow
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
    assert model.setData(cell, "2,5", QtCore.Qt.ItemDataRole.EditRole)
    assert model.frame.iat[0, 1] == 2.5
    window.close()


def test_alpha_tree_and_chart_metric_selection(qt_app):
    window = MainWindow()
    alpha = window.tree.topLevelItem(0)
    beta = window.tree.topLevelItem(1)
    assert alpha.childCount() == 3
    assert beta.childCount() == 7
    richness = alpha.child(0)
    assert richness.childCount() == 5
    margalef = richness.child(1)
    margalef.setCheckState(0, QtCore.Qt.CheckState.Checked)
    assert "margalef" in window.checked_codes
    window.retranslate()
    assert "margalef" in window.checked_codes
    result = ResultWindow("margalef", pd.DataFrame({"Sonuçlar": ["Margalef(DMG)", "Menhinick(DMN)", "α*DMM"], "s1": [1, 2, 3]}), "tr")
    assert result.metric_box.count() == 3
    result.metric_box.setCurrentIndex(1)
    assert result.metric_box.currentData() == 1
    result.close()
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


def test_selected_alpha_indices_export_without_result_windows(qt_app, tmp_path, monkeypatch):
    from pathlib import Path

    window = MainWindow()
    sample = Path(__file__).resolve().parent.parent / "sampledata" / "Alfa_Bolluk.xlsx"
    window._replace_frame(read_table(sample))
    window.checked_codes.update({"richness", "margalef"})
    target = tmp_path / "selected.xlsx"
    monkeypatch.setattr(QtWidgets.QFileDialog, "getSaveFileName", lambda *_: (str(target), ""))
    window.export_selected_analyses()
    loop = QtCore.QEventLoop()
    window.active_thread.finished.connect(loop.quit)
    QtCore.QTimer.singleShot(10000, loop.quit)
    loop.exec()
    assert window.active_thread is None
    assert window.results == []
    assert pd.ExcelFile(target).sheet_names == ["richness", "margalef"]
    window.close()


import pytest


@pytest.fixture(scope="module")
def qt_app():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    yield app
