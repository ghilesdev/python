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
        layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(layout)
        # creating the main image viewer
        image_view = QLabel("image widget")
        pixmap = QPixmap("1.png")
        image_view.setPixmap(pixmap)

        # creating the buttons
        manualButton = QPushButton("Avance Manuel")
        autoButton = QPushButton("Automatique")
        readButton = QPushButton("ouvrir")

        # adding buttons to the layout
        layout.addWidget(manualButton, 1, 7, 1, 2)
        layout.addWidget(autoButton, 2, 7, 1, 2)
        layout.addWidget(readButton, 4, 7, 1, 2)

        # creating the inputs
        moveCommand = QLineEdit()
        pathToImage = QLineEdit()

        # adding the labels
        layout.addWidget(moveCommand, 0, 8)
        layout.addWidget(pathToImage, 3, 8)

        # creating labels
        moveCommandlabel = QLabel("move")
        pathToImagelabel = QLabel("path")

        # adding label
        layout.addWidget(moveCommandlabel, 0, 7)
        layout.addWidget(pathToImagelabel, 3, 7)

        # creating left side bar (show camera and arduino connection)
        arduinoLabel = QLabel("Arduino Status")
        arduinostatus = QLabel("Arduino connected")
        arduinostatus.setStyleSheet("color: green")
        cameraLabel = QLabel("Camera Status")
        camerastatus = QLabel("Camera connected")
        camerastatus.setStyleSheet("color: green")

        # adding the left side bar
        layout.addWidget(arduinoLabel, 0, 0)
        layout.addWidget(arduinostatus, 1, 0)
        layout.addWidget(cameraLabel, 3, 0)
        layout.addWidget(camerastatus, 4, 0)

        self.resize(pixmap.width(), pixmap.height())
        image_view.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_view, 0, 1, 5, 5)
        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = GUI()
    mainWindow.show()
    app.exec_()
