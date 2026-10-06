"""A restrained botanical visual system shared by all windows."""

STYLE = """
QMainWindow, QDialog { background: #f3f7f6; color: #18313b; }
QWidget { font-family: 'DejaVu Sans', 'Segoe UI', sans-serif; font-size: 10pt; color: #18313b; }
QFrame#Hero { background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #073b46,stop:1 #126968); border-radius: 18px; }
QFrame#Hero QLabel { color: #ffffff; background: transparent; }
QFrame#Hero QLabel#Logo { background: transparent; border: 2px solid #d8f4ec; border-radius: 33px; }
QLabel#Brand { font-size: 23pt; font-weight: 800; letter-spacing: 2px; }
QLabel#Tagline { color: #d8f4ec; font-size: 11pt; }
QFrame#Panel, QFrame#Card { background: #ffffff; border: 1px solid #dce9e6; border-radius: 14px; }
QLabel#Section { font-size: 14pt; font-weight: 700; }
QLabel#Metric { font-size: 20pt; font-weight: 700; color: #0e665e; }
QLabel#Muted { color: #6c8187; }
QPushButton { background: #ffffff; border: 1px solid #cdded9; border-radius: 9px; padding: 9px 14px; font-weight: 600; }
QPushButton:hover { background: #e8f4ef; border-color: #7cbaab; }
QPushButton:pressed { background: #d6ece5; }
QPushButton:disabled { color: #99a9ad; background: #edf2f0; }
QPushButton#Primary { background: #0e766b; color: #ffffff; border: 1px solid #0e766b; }
QPushButton#Primary:hover { background: #0a5f57; }
QPushButton#Primary:disabled { background: #91b8b0; border-color: #91b8b0; color: #eff7f4; }
QTreeWidget, QTableView { background: #ffffff; border: none; selection-background-color: #d9eee8; selection-color: #173a3a; gridline-color: #e5edeb; alternate-background-color: #f8fbfa; }
QTreeWidget::item { height: 30px; padding-left: 5px; }
QTreeWidget::item:selected { background: #d9eee8; border-radius: 5px; }
QHeaderView::section { background: #e9f3ef; color: #31554e; padding: 8px; border: none; border-bottom: 1px solid #d5e5e0; font-weight: 700; }
QComboBox, QLineEdit, QSpinBox { background: #ffffff; border: 1px solid #cdded9; border-radius: 8px; padding: 7px; }
QComboBox:hover, QLineEdit:focus, QSpinBox:focus { border-color: #0e766b; }
QStatusBar { background: #eaf3f0; color: #40625b; }
QProgressBar { border: none; border-radius: 5px; background: #dcebe6; text-align: center; }
QProgressBar::chunk { background: #2caf93; border-radius: 5px; }
"""
