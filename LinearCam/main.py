import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from LinearCam.view.vision_view import GUI
from LinearCam.controller.vision_controller import controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = GUI()
    mainWindow.show()
    controller(view=mainWindow)
    app.exec_()
