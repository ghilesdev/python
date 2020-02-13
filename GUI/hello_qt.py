# https://realpython.com/python-pyqt-gui-calculator/

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar


# Create an instance of Qapplication
# app = QApplication(sys.argv)  # use [] instead of sys.argv if no need of args

# create an instance of the widget GUI
# window = QWidget()
# window.setWindowTitle("pyQt app")
# window.setGeometry(100, 100, 280, 80)  # x, y, w, h
# window.move(100, 50)
# layout = QHBoxLayout()
# layout.addWidget(QPushButton("Left"))
# layout.addWidget(QPushButton("Center"))
# layout.addWidget(QPushButton("Right"))

# layout = QFormLayout()
# layout.addRow("Name:", QLineEdit())
# layout.addRow("Age:", QLineEdit())
# layout.addRow("Job:", QLineEdit())
# layout.addRow("Hobbies:", QLineEdit())
# window.setLayout(layout)
# window.setLayout(layout)


# hello_msg = QLabel("<h1> Main window </h1>", parent=window)
# hello_msg.move(60, 15)

# show the window
# window.show()

# run the application main loop
# sys.exit(app.exec_())

# dialog window
class Dialog(QDialog):
    """Dialog Box"""

    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle("Qdialog")
        qdilg = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("name: ", QLineEdit())
        form_layout.addRow("age: ", QLineEdit())
        form_layout.addRow("position: ", QLineEdit())
        qdilg.addLayout(form_layout)
        # btns = QDialogButtonBox()
        # btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        btns = QPushButton("add")
        btns.clicked.connect(get_infos)
        qdilg.addWidget(btns)
        self.setLayout(qdilg)


class Window(QMainWindow):
    """Main Window"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Qmain Window")
        self.setCentralWidget(QLabel("Central widget"))
        self._createMenu()
        self._createStatusBar()
        self._createToolBar()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction("&Exit", self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("status bar")
        self.setStatusBar(status)

    def _createToolBar(self):
        tool_bar = QToolBar()
        self.addToolBar(tool_bar)
        tool_bar.addAction("exit", self.close)


def get_infos():
    print("ok button clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
