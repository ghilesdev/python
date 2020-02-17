from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys


class GUI(QMainWindow):
    """
        Main view of a visualisation application that takes images from
        a linear camera, automatically and manually with arduino communication
    """

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)
        self.setWindowTitle("Image Processor")
        # create a main widget then add to it a layout
        # add all the widgets to the layout
        # layout = QVBoxLayout()
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        # creating the main image viewer
        self.image_view = QLabel("image widget")
        self.pixmap = QPixmap("1.png")
        self.image_view.setPixmap(self.pixmap)
        self._createLayout()

    def _createLayout(self):
        # creating the buttons
        # TODO mettre tout les widgets en self.widget !!
        self.manualButton = QPushButton("Avance Manuel")
        self.autoButton = QPushButton("Automatique")
        self.readButton = QPushButton("ouvrir")

        # adding buttons to the layout
        self.layout.addWidget(self.manualButton, 1, 7, 1, 2)
        self.layout.addWidget(self.autoButton, 2, 7, 1, 2)
        self.layout.addWidget(self.readButton, 4, 7, 1, 2)

        # creating the inputs
        moveCommand = QLineEdit()
        moveCommand.setPlaceholderText("(mm)")
        pathToImage = QLineEdit()

        # adding the labels
        self.layout.addWidget(moveCommand, 0, 8)
        self.layout.addWidget(pathToImage, 3, 8)

        # creating labels
        moveCommandlabel = QLabel("move")
        pathToImagelabel = QLabel("path")

        # adding label
        self.layout.addWidget(moveCommandlabel, 0, 7)
        self.layout.addWidget(pathToImagelabel, 3, 7)

        # creating left side bar (show camera and arduino connection)
        arduinoLabel = QLabel("Arduino Status")
        arduinostatus = QLabel("Arduino connected")
        arduinostatus.setStyleSheet("color: green")
        cameraLabel = QLabel("Camera Status")
        camerastatus = QLabel("Camera connected")
        camerastatus.setStyleSheet("color: green")

        # adding the left side bar
        self.layout.addWidget(arduinoLabel, 0, 0)
        self.layout.addWidget(arduinostatus, 1, 0)
        self.layout.addWidget(cameraLabel, 3, 0)
        self.layout.addWidget(camerastatus, 4, 0)

        self.resize(self.pixmap.width(), self.pixmap.height())
        self.image_view.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_view, 0, 1, 5, 5)
        self.setCentralWidget(self.widget)


# commented this because the view is launched in
# ..main.py
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mainWindow = GUI()
#     mainWindow.show()
#     app.exec_()
