#! /usr/bin/env python3

"""Pycalc is a simple calculator build using Pyqt5 based on the MVC design pattern"""
import sys
from functools import partial
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

__version__ = "0.1"
__author__ = "aghiles"
ERROR_MSG = "Error"

# creating the model as a single function
def evaluateExpression(expression):
    """evaluate the expression"""
    try:
        result = str(eval(expression))
    except ArithmeticError:
        result = ERROR_MSG
    return result


# creating a subclass to setup the GUI
class PyCalcUI(QMainWindow):
    """Pycalc main View UI"""

    def __init__(self):
        """view Initializer"""
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(350, 350)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QVBoxLayout()
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        """Create the display"""
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttons = {}
        buttonLayout = QGridLayout()
        buttons = {
            "0": (3, 1),
            "C": (3, 0),
            ".": (2, 4),
            "1": (2, 0),
            "2": (2, 1),
            "3": (2, 2),
            "4": (1, 0),
            "5": (1, 1),
            "6": (1, 2),
            "7": (0, 0),
            "8": (0, 1),
            "9": (0, 2),
            "+": (0, 3),
            "-": (0, 4),
            "*": (1, 3),
            "/": (1, 4),
            "=": (2, 3),
        }
        for btnTxt, pos in buttons.items():
            self.buttons[btnTxt] = QPushButton(btnTxt)
            self.buttons[btnTxt].setFixedSize(60, 60)
            buttonLayout.addWidget(self.buttons[btnTxt], pos[0], pos[1])
            self.generalLayout.addLayout(buttonLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def getDisplayText(self):
        return self.display.text()

    def clearDisplayText(self):
        self.setDisplayText("")


class PyCalcController:
    """
    PyCalc Controller class
    """

    def __init__(self, model, view):
        """Initializer of the cotroller class"""
        self._evaluate = model
        self._view = view
        self._connectSignals()

    def _calcResult(self):
        """evaluate expression"""
        result = self._evaluate(expression=self._view.getDisplayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExp):
        """build Expression"""
        if self._view.getDisplayText() == ERROR_MSG:
            self._view.clearDisplayText()

        expression = self._view.getDisplayText() + subExp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """connect signals between byttons and their functions"""
        for btnTxt, btn in self._view.buttons.items():
            if btnTxt not in {"C", "="}:
                btn.clicked.connect(partial(self._buildExpression, btnTxt))
        self._view.buttons["C"].clicked.connect(self._view.clearDisplayText)
        self._view.buttons["="].clicked.connect(self._calcResult)
        self._view.display.returnPressed.connect(self._calcResult)


# Client code
def main():
    """Main Function"""
    # create an instance of the window
    pyCalc = QApplication(sys.argv)
    # creating an instance of the UI
    view = PyCalcUI()
    view.show()
    # feeding the view to the controller
    PyCalcController(model=evaluateExpression, view=view)

    sys.exit(pyCalc.exec_())


if __name__ == "__main__":
    main()
