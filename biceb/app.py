"""Cross-platform Qt desktop interface for BİÇEB."""

import logging
import sys
from pathlib import Path

import pandas as pd
from PySide6 import QtCore, QtGui, QtWidgets

from biceb import __version__
from biceb.core import ANALYSES, BY_CODE, compute
from biceb.data import DataError, export_excel, read_table, sheets, validate
from biceb.i18n import RESULT_TERMS_EN, error_text, tr
from biceb.logging_config import configure_logging
from biceb.theme import STYLE


ROOT = Path(__file__).resolve().parent
RESOURCES = ROOT / "resources"
LOGGER = logging.getLogger("biceb.app")


def icon() -> QtGui.QIcon:
    return QtGui.QIcon(str(RESOURCES / "biodiversity.ico"))


def translated_result(frame: pd.DataFrame, language: str) -> pd.DataFrame:
    if language != "en":
        return frame
    result = frame.rename(columns=RESULT_TERMS_EN).copy()
    if len(result.columns):
        first = result.columns[0]
        result[first] = result[first].map(lambda value: RESULT_TERMS_EN.get(value, value) if isinstance(value, str) else value)
    return result


class FrameModel(QtCore.QAbstractTableModel):
    invalid_input = QtCore.Signal(str)
    changed = QtCore.Signal()

    def __init__(self, frame: pd.DataFrame, editable: bool = False, language: str = "tr", parent=None):
        super().__init__(parent)
        self.frame = frame
        self.editable = editable
        self.language = language

    def rowCount(self, parent=QtCore.QModelIndex()):
        return 0 if parent.isValid() else len(self.frame)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 0 if parent.isValid() else len(self.frame.columns)

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        value = self.frame.iat[index.row(), index.column()]
        if role in (QtCore.Qt.ItemDataRole.DisplayRole, QtCore.Qt.ItemDataRole.EditRole):
            return str(value)
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() > 0:
            return QtCore.Qt.AlignmentFlag.AlignCenter
        if role == QtCore.Qt.ItemDataRole.ForegroundRole and index.column() == 0:
            return QtGui.QColor("#0e665e")
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Orientation.Horizontal:
            if self.editable and section == 0:
                return tr(self.language, "species")
            return str(self.frame.columns[section])
        return str(section + 1)

    def flags(self, index):
        flags = super().flags(index)
        if self.editable and index.isValid():
            flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        return flags

    def setData(self, index, value, role=QtCore.Qt.ItemDataRole.EditRole):
        if not self.editable or not index.isValid() or role != QtCore.Qt.ItemDataRole.EditRole:
            return False
        candidate = str(value).strip()
        if index.column() == 0:
            if not candidate:
                self.invalid_input.emit("missing_species")
                return False
            if candidate in self.frame.iloc[:, 0].drop(index.row()).values:
                self.invalid_input.emit("duplicate_species")
                return False
            parsed = candidate
        else:
            try:
                parsed = int(candidate)
                if parsed < 0 or candidate not in (str(parsed), f"+{parsed}"):
                    raise ValueError
            except ValueError:
                self.invalid_input.emit(f"invalid_abundance|{self.frame.columns[index.column()]}")
                return False
        self.frame.iat[index.row(), index.column()] = parsed
        self.dataChanged.emit(index, index, [QtCore.Qt.ItemDataRole.DisplayRole])
        self.changed.emit()
        return True


class AnalysisWorker(QtCore.QObject):
    completed = QtCore.Signal(object)
    failed = QtCore.Signal(str)
    progress = QtCore.Signal(int)

    def __init__(self, code: str, frame: pd.DataFrame, selected: list[int]):
        super().__init__()
        self.code = code
        self.frame = frame
        self.selected = selected

    @QtCore.Slot()
    def run(self):
        try:
            result = compute(self.code, self.frame, self.selected, self.progress.emit)
            self.completed.emit(result)
        except Exception as exc:
            LOGGER.exception("Analysis %s failed", self.code)
            self.failed.emit(str(exc))


class MetricCard(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("Muted")
        self.value = QtWidgets.QLabel("—")
        self.value.setObjectName("Metric")
        layout.addWidget(self.label)
        layout.addWidget(self.value)


class ResultWindow(QtWidgets.QMainWindow):
    def __init__(self, code: str, frame: pd.DataFrame, language: str, parent=None):
        super().__init__(parent)
        self.code = code
        self.source = frame
        self.language = language
        self.setWindowIcon(icon())
        self.resize(1050, 700)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(14)
        self.title = QtWidgets.QLabel()
        self.title.setObjectName("Section")
        self.subtitle = QtWidgets.QLabel()
        self.subtitle.setObjectName("Muted")
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

        panel = QtWidgets.QFrame()
        panel.setObjectName("Panel")
        panel_layout = QtWidgets.QVBoxLayout(panel)
        panel_layout.setContentsMargins(10, 10, 10, 10)
        self.table = QtWidgets.QTableView()
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)
        panel_layout.addWidget(self.table)
        layout.addWidget(panel, 1)

        actions = QtWidgets.QHBoxLayout()
        self.copy_button = QtWidgets.QPushButton()
        self.copy_button.clicked.connect(self.copy)
        self.export_button = QtWidgets.QPushButton()
        self.export_button.clicked.connect(self.export)
        self.chart_button = QtWidgets.QPushButton()
        self.chart_button.setObjectName("Primary")
        self.chart_button.clicked.connect(self.show_chart)
        actions.addWidget(self.copy_button)
        actions.addWidget(self.export_button)
        actions.addStretch()
        actions.addWidget(self.chart_button)
        layout.addLayout(actions)
        self.status = self.statusBar()
        self.retranslate(language)

    def retranslate(self, language: str):
        self.language = language
        self.setWindowTitle(tr(language, "result") + " · " + tr(language, self.code))
        self.title.setText(tr(language, self.code))
        self.subtitle.setText(tr(language, "result_subtitle"))
        self.copy_button.setText(tr(language, "copy"))
        self.export_button.setText(tr(language, "export"))
        self.chart_button.setText(tr(language, "chart"))
        self.display = translated_result(self.source, language)
        self.model = FrameModel(self.display, parent=self)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def copy(self):
        QtWidgets.QApplication.clipboard().setText(self.display.to_csv(index=False, sep="\t"))
        self.status.showMessage(tr(self.language, "copy_done"), 5000)

    def export(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, tr(self.language, "export"), "", tr(self.language, "save_filter"))
        if not filename:
            return
        try:
            path = export_excel(self.display, filename)
            LOGGER.info("Exported analysis %s to %s", self.code, path)
            self.status.showMessage(tr(self.language, "export_done", path=path), 6000)
        except Exception as exc:
            LOGGER.exception("Could not export analysis %s", self.code)
            QtWidgets.QMessageBox.warning(self, tr(self.language, "error"), tr(self.language, "export_error", detail=exc))

    def show_chart(self):
        try:
            import matplotlib
            matplotlib.use("QtAgg")
            from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
            from matplotlib.figure import Figure

            numeric = self.source.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
            if numeric.empty or not numeric.notna().any().any():
                raise ValueError(tr(self.language, "chart_unavailable"))
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle(tr(self.language, self.code) + " · " + tr(self.language, "chart"))
            dialog.resize(900, 580)
            figure = Figure(figsize=(9, 5), layout="constrained")
            canvas = FigureCanvasQTAgg(figure)
            axis = figure.subplots()
            if self.code == "dependent":
                labels = [str(value) for value in self.source.iloc[:25, 0]]
                values = pd.to_numeric(self.source.iloc[:25, 1], errors="coerce")
                axis.bar(labels, values, color="#168475")
                axis.set_xlabel(tr(self.language, "species"))
            elif self.code == "independent":
                x = pd.to_numeric(self.source.iloc[:, 0], errors="coerce")
                y_columns = [column for column in self.source.columns[1:] if "σ" not in str(column)]
                for column in y_columns[:12]:
                    axis.plot(x, pd.to_numeric(self.source[column], errors="coerce"), label=str(column), linewidth=2)
                axis.set_xlabel(tr(self.language, "axis_n"))
                axis.legend(fontsize=8, ncol=2)
            elif self.code == "she":
                x = [str(value) for value in self.source.columns[1:]]
                for _, row in self.source.iloc[:4].iterrows():
                    axis.plot(x, pd.to_numeric(row.iloc[1:], errors="coerce"), marker="o", label=str(row.iloc[0]))
                axis.legend()
                axis.set_xlabel(tr(self.language, "axis_sites"))
            else:
                values = numeric.iloc[0]
                axis.bar([str(label) for label in values.index[:25]], values.iloc[:25], color="#168475")
                axis.set_xlabel(tr(self.language, "axis_sites"))
            axis.set_ylabel(tr(self.language, "axis_value"))
            axis.set_title(tr(self.language, self.code), loc="left", fontweight="bold")
            axis.grid(axis="y", alpha=0.2)
            axis.tick_params(axis="x", labelrotation=35)
            box = QtWidgets.QVBoxLayout(dialog)
            box.addWidget(canvas)
            canvas.draw()
            dialog.exec()
        except Exception as exc:
            LOGGER.exception("Could not draw chart for %s", self.code)
            QtWidgets.QMessageBox.warning(self, tr(self.language, "error"), str(exc))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings("BICEB", "BICEB")
        default_language = "tr" if QtCore.QLocale.system().name().startswith("tr") else "en"
        self.language = self.settings.value("language", default_language)
        self._qt_translator = None
        self._install_qt_translation()
        self.frame = None
        self.file_path = None
        self.selected_code = "richness"
        self.results = []
        self.active_thread = None
        self.active_worker = None
        self.active_code = None
        self._close_when_finished = False
        self.setWindowIcon(icon())
        self.resize(1280, 820)
        self.setMinimumSize(900, 600)
        self._build_ui()
        self.retranslate()

    def _build_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        outer = QtWidgets.QVBoxLayout(central)
        outer.setContentsMargins(20, 20, 20, 16)
        outer.setSpacing(16)

        hero = QtWidgets.QFrame()
        hero.setObjectName("Hero")
        hero_layout = QtWidgets.QHBoxLayout(hero)
        hero_layout.setContentsMargins(23, 17, 23, 17)
        logo = QtWidgets.QLabel()
        logo.setObjectName("Logo")
        pixmap = QtGui.QPixmap(str(RESOURCES / "images.png"))
        logo.setPixmap(pixmap.scaled(66, 66, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        hero_layout.addWidget(logo)
        title_layout = QtWidgets.QVBoxLayout()
        self.brand = QtWidgets.QLabel()
        self.brand.setObjectName("Brand")
        self.tagline = QtWidgets.QLabel()
        self.tagline.setObjectName("Tagline")
        title_layout.addWidget(self.brand)
        title_layout.addWidget(self.tagline)
        hero_layout.addLayout(title_layout)
        hero_layout.addStretch()
        self.language_box = QtWidgets.QComboBox()
        self.language_box.addItem("Türkçe", "tr")
        self.language_box.addItem("English", "en")
        self.language_box.setCurrentIndex(0 if self.language == "tr" else 1)
        self.language_box.currentIndexChanged.connect(self.change_language)
        hero_layout.addWidget(self.language_box)
        self.guide_button = QtWidgets.QPushButton()
        self.guide_button.clicked.connect(self.open_guide)
        hero_layout.addWidget(self.guide_button)
        self.open_button = QtWidgets.QPushButton()
        self.open_button.setObjectName("Primary")
        self.open_button.clicked.connect(self.open_data)
        hero_layout.addWidget(self.open_button)
        outer.addWidget(hero)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(16)
        sidebar = QtWidgets.QFrame()
        sidebar.setObjectName("Panel")
        sidebar.setFixedWidth(280)
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 16, 12, 12)
        self.analyses_label = QtWidgets.QLabel()
        self.analyses_label.setObjectName("Section")
        sidebar_layout.addWidget(self.analyses_label)
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(13)
        self.tree.itemSelectionChanged.connect(self.select_analysis)
        self.tree.itemDoubleClicked.connect(lambda *_: self.run_analysis())
        sidebar_layout.addWidget(self.tree)
        body.addWidget(sidebar)

        content = QtWidgets.QVBoxLayout()
        content.setSpacing(14)
        cards = QtWidgets.QHBoxLayout()
        cards.setSpacing(12)
        self.species_card = MetricCard()
        self.sites_card = MetricCard()
        self.individuals_card = MetricCard()
        for card in (self.species_card, self.sites_card, self.individuals_card):
            cards.addWidget(card)
        content.addLayout(cards)

        panel = QtWidgets.QFrame()
        panel.setObjectName("Panel")
        panel_layout = QtWidgets.QVBoxLayout(panel)
        panel_layout.setContentsMargins(15, 15, 15, 15)
        panel_layout.setSpacing(10)
        table_head = QtWidgets.QHBoxLayout()
        self.preview_label = QtWidgets.QLabel()
        self.preview_label.setObjectName("Section")
        table_head.addWidget(self.preview_label)
        table_head.addStretch()
        self.file_label = QtWidgets.QLabel()
        self.file_label.setObjectName("Muted")
        table_head.addWidget(self.file_label)
        panel_layout.addLayout(table_head)
        edit_bar = QtWidgets.QHBoxLayout()
        self.add_species_button = QtWidgets.QPushButton()
        self.add_species_button.clicked.connect(self.add_species)
        self.add_site_button = QtWidgets.QPushButton()
        self.add_site_button.clicked.connect(self.add_site)
        self.remove_button = QtWidgets.QPushButton()
        self.remove_button.clicked.connect(self.remove_selected)
        edit_bar.addWidget(self.add_species_button)
        edit_bar.addWidget(self.add_site_button)
        edit_bar.addWidget(self.remove_button)
        edit_bar.addStretch()
        panel_layout.addLayout(edit_bar)
        self.table = QtWidgets.QTableView()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        panel_layout.addWidget(self.table, 1)
        self.empty = QtWidgets.QLabel()
        self.empty.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.empty.setWordWrap(True)
        self.empty.setMinimumHeight(100)
        self.empty.setObjectName("Muted")
        panel_layout.addWidget(self.empty)
        content.addWidget(panel, 1)

        bottom = QtWidgets.QFrame()
        bottom.setObjectName("Panel")
        bottom_layout = QtWidgets.QHBoxLayout(bottom)
        bottom_layout.setContentsMargins(16, 12, 16, 12)
        selection_layout = QtWidgets.QVBoxLayout()
        self.selected_label = QtWidgets.QLabel()
        self.selected_label.setObjectName("Muted")
        self.selected_title = QtWidgets.QLabel()
        self.selected_title.setObjectName("Section")
        selection_layout.addWidget(self.selected_label)
        selection_layout.addWidget(self.selected_title)
        bottom_layout.addLayout(selection_layout)
        bottom_layout.addStretch()
        self.run_button = QtWidgets.QPushButton()
        self.run_button.setObjectName("Primary")
        self.run_button.clicked.connect(self.run_analysis)
        bottom_layout.addWidget(self.run_button)
        content.addWidget(bottom)
        self.hint = QtWidgets.QLabel()
        self.hint.setObjectName("Muted")
        self.hint.setWordWrap(True)
        content.addWidget(self.hint)
        body.addLayout(content, 1)
        outer.addLayout(body, 1)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setFixedWidth(180)
        self.progress.hide()
        self.statusBar().addPermanentWidget(self.progress)

    def retranslate(self):
        language = self.language
        self.setWindowTitle(tr(language, "app_title"))
        self.brand.setText(tr(language, "app_name"))
        self.tagline.setText(tr(language, "tagline"))
        self.guide_button.setText(tr(language, "guide"))
        self.open_button.setText(tr(language, "open"))
        self.analyses_label.setText(tr(language, "analyses"))
        self.preview_label.setText(tr(language, "preview"))
        self.add_species_button.setText(tr(language, "add_species"))
        self.add_site_button.setText(tr(language, "add_site"))
        self.remove_button.setText(tr(language, "remove_selected"))
        self.species_card.label.setText(tr(language, "species"))
        self.sites_card.label.setText(tr(language, "sites"))
        self.individuals_card.label.setText(tr(language, "individuals"))
        self.selected_label.setText(tr(language, "selected"))
        self.selected_title.setText(tr(language, self.selected_code))
        self.run_button.setText(tr(language, "run"))
        self.hint.setText(tr(language, "hint"))
        self.file_label.setText(self.file_path.name if self.file_path else tr(language, "no_file"))
        self.empty.setText(tr(language, "start_title") + "\n" + tr(language, "start_text"))
        self._populate_tree()
        if self.frame is not None:
            self.model.language = language
            self.model.headerDataChanged.emit(QtCore.Qt.Orientation.Horizontal, 0, 0)
        for result in self.results:
            result.retranslate(language)

    def _populate_tree(self):
        self.tree.blockSignals(True)
        self.tree.clear()
        for group in ("alpha", "indices", "abundance", "beta"):
            parent = QtWidgets.QTreeWidgetItem([tr(self.language, group)])
            parent.setFlags(parent.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
            self.tree.addTopLevelItem(parent)
            for analysis in ANALYSES:
                if analysis.group_key == group:
                    child = QtWidgets.QTreeWidgetItem([tr(self.language, analysis.title_key)])
                    child.setData(0, QtCore.Qt.ItemDataRole.UserRole, analysis.code)
                    parent.addChild(child)
                    if analysis.code == self.selected_code:
                        self.tree.setCurrentItem(child)
            parent.setExpanded(True)
        self.tree.blockSignals(False)

    def change_language(self):
        self.language = self.language_box.currentData()
        self.settings.setValue("language", self.language)
        self._install_qt_translation()
        self.retranslate()

    def _install_qt_translation(self):
        app = QtWidgets.QApplication.instance()
        if self._qt_translator is not None:
            app.removeTranslator(self._qt_translator)
        translator = QtCore.QTranslator(self)
        translation_path = QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.LibraryPath.TranslationsPath)
        if translator.load(f"qtbase_{self.language}", translation_path):
            app.installTranslator(translator)
            self._qt_translator = translator
        else:
            self._qt_translator = None

    def select_analysis(self):
        item = self.tree.currentItem()
        if item is not None:
            code = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if code:
                self.selected_code = code
                self.selected_title.setText(tr(self.language, code))

    def _show_error(self, message: str):
        QtWidgets.QMessageBox.warning(self, tr(self.language, "error"), message)

    def _refresh_metrics(self):
        if self.frame is None:
            return
        self.species_card.value.setText(str(len(self.frame)))
        self.sites_card.value.setText(str(len(self.frame.columns) - 1))
        self.individuals_card.value.setText(f"{int(self.frame.iloc[:, 1:].to_numpy().sum()):,}".replace(",", " "))

    def _replace_frame(self, frame: pd.DataFrame):
        self.frame = frame.reset_index(drop=True)
        self.model = FrameModel(self.frame, editable=True, language=self.language, parent=self)
        self.model.invalid_input.connect(lambda code: self._show_error(error_text(self.language, code)))
        self.model.changed.connect(self._refresh_metrics)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        self.empty.hide()
        self._refresh_metrics()

    def add_species(self):
        if self.frame is None:
            self._show_error(tr(self.language, "select_data"))
            return
        name, accepted = QtWidgets.QInputDialog.getText(self, tr(self.language, "add_species"), tr(self.language, "name_prompt"))
        name = name.strip()
        if not accepted:
            return
        if not name or name in self.frame.iloc[:, 0].values:
            self._show_error(tr(self.language, "duplicate_species"))
            return
        row = pd.DataFrame([[name] + [0] * (len(self.frame.columns) - 1)], columns=self.frame.columns)
        self._replace_frame(pd.concat([self.frame, row], ignore_index=True))

    def add_site(self):
        if self.frame is None:
            self._show_error(tr(self.language, "select_data"))
            return
        name, accepted = QtWidgets.QInputDialog.getText(self, tr(self.language, "add_site"), tr(self.language, "name_prompt"))
        name = name.strip()
        if not accepted:
            return
        if not name or name in self.frame.columns:
            self._show_error(tr(self.language, "duplicate_columns"))
            return
        frame = self.frame.copy()
        frame[name] = 0
        self._replace_frame(frame)

    def remove_selected(self):
        if self.frame is None:
            self._show_error(tr(self.language, "select_data"))
            return
        indexes = self.table.selectedIndexes()
        if not indexes:
            return
        columns = sorted({index.column() for index in indexes if index.column() > 0})
        rows = sorted({index.row() for index in indexes if index.column() == 0})
        if len(rows) >= len(self.frame) or len(columns) >= len(self.frame.columns) - 1:
            self._show_error(tr(self.language, "cannot_remove"))
            return
        frame = self.frame.drop(index=rows, columns=list(self.frame.columns[columns])) if columns else self.frame.drop(index=rows)
        self._replace_frame(frame)

    def open_data(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, tr(self.language, "open"), "", tr(self.language, "open_filter"))
        if not filename:
            return
        try:
            sheet = None
            if Path(filename).suffix.lower() in {".xls", ".xlsx"}:
                names = sheets(filename)
                if len(names) > 1:
                    sheet, accepted = QtWidgets.QInputDialog.getItem(self, tr(self.language, "choose_sheet"), tr(self.language, "choose_sheet"), names, 0, False)
                    if not accepted:
                        return
            frame = read_table(filename, sheet)
            self.file_path = Path(filename)
            self._replace_frame(frame)
            self.file_label.setText(self.file_path.name)
            self.statusBar().showMessage(tr(self.language, "status_loaded", name=self.file_path.name), 6000)
            LOGGER.info("Opened %s: %d species, %d sites", filename, len(frame), len(frame.columns) - 1)
        except Exception as exc:
            LOGGER.exception("Could not open %s", filename)
            detail = error_text(self.language, str(exc)) if isinstance(exc, DataError) else str(exc)
            self._show_error(tr(self.language, "open_error", detail=detail))

    def _selected_columns(self) -> list[int]:
        return sorted({index.column() for index in self.table.selectedIndexes() if index.column() > 0})

    def run_analysis(self):
        if self.active_thread is not None:
            return
        if self.frame is None:
            self._show_error(tr(self.language, "select_data"))
            return
        code = self.selected_code
        selected = self._selected_columns() if code in {"presence_pair", "abundance_pair"} else []
        if len(selected) not in {0, 2} or (code in {"presence_pair", "abundance_pair"} and len(self.frame.columns) < 3):
            self._show_error(tr(self.language, "choose_two"))
            return
        try:
            snapshot = validate(self.frame)
        except DataError as exc:
            self._show_error(error_text(self.language, str(exc)))
            return
        self.run_button.setEnabled(False)
        self.open_button.setEnabled(False)
        self.table.setEnabled(False)
        self.add_species_button.setEnabled(False)
        self.add_site_button.setEnabled(False)
        self.remove_button.setEnabled(False)
        self.progress.setValue(0)
        self.progress.show()
        self.statusBar().showMessage(tr(self.language, "status_running", name=tr(self.language, code)))
        thread = QtCore.QThread(self)
        worker = AnalysisWorker(code, snapshot, selected)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress.connect(self.progress.setValue)
        worker.completed.connect(self._analysis_done_current)
        worker.failed.connect(self._analysis_failed)
        worker.completed.connect(thread.quit)
        worker.failed.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._worker_finished)
        self.active_thread = thread
        self.active_worker = worker
        self.active_code = code
        thread.start()

    @QtCore.Slot(object)
    def _analysis_done_current(self, result: pd.DataFrame):
        code = self.active_code
        window = ResultWindow(code, result, self.language, self)
        window.show()
        self.results.append(window)
        self.statusBar().showMessage(tr(self.language, "status_done", name=tr(self.language, code)), 6000)
        LOGGER.info("Analysis %s completed", code)

    @QtCore.Slot(str)
    def _analysis_failed(self, detail: str):
        self._show_error(tr(self.language, "analysis_error", detail=detail))

    def _worker_finished(self):
        self.active_thread = None
        self.active_worker = None
        self.active_code = None
        self.run_button.setEnabled(True)
        self.open_button.setEnabled(True)
        self.table.setEnabled(True)
        self.add_species_button.setEnabled(True)
        self.add_site_button.setEnabled(True)
        self.remove_button.setEnabled(True)
        self.progress.hide()
        if self._close_when_finished:
            self.close()

    def closeEvent(self, event):
        if self.active_thread is not None:
            self._close_when_finished = True
            event.ignore()
            return
        super().closeEvent(event)

    def open_guide(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(tr(self.language, "guide_title"))
        dialog.resize(650, 400)
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(13)
        title = QtWidgets.QLabel(tr(self.language, "guide_title"))
        title.setObjectName("Section")
        layout.addWidget(title)
        for key in ("guide_intro", "guide_step_1", "guide_step_2", "guide_step_3"):
            label = QtWidgets.QLabel(tr(self.language, key))
            label.setWordWrap(True)
            layout.addWidget(label)
        layout.addStretch()
        buttons = QtWidgets.QHBoxLayout()
        pdf_button = QtWidgets.QPushButton(tr(self.language, "legacy_guide"))
        pdf_button.clicked.connect(self._open_historical_guide)
        close_button = QtWidgets.QPushButton(tr(self.language, "close"))
        close_button.setObjectName("Primary")
        close_button.clicked.connect(dialog.accept)
        buttons.addWidget(pdf_button)
        buttons.addStretch()
        buttons.addWidget(close_button)
        layout.addLayout(buttons)
        dialog.exec()

    def _open_historical_guide(self):
        path = RESOURCES / "userguide.pdf"
        if not QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(path))):
            self._show_error(tr(self.language, "open_error", detail=str(path)))


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("BİÇEB")
    app.setApplicationVersion(__version__)
    app.setOrganizationName("BICEB")
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    location = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppLocalDataLocation)
    log_path = configure_logging(Path(location) / "logs")
    LOGGER.info("BİÇEB %s starting; log file: %s", __version__, log_path)
    window = MainWindow()
    window.show()
    return app.exec()
