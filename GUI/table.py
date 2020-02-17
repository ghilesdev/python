from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class ImageProcess(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ImageProcess()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
