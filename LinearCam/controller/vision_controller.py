import serial


class controller(object):
    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _connectSignals(self):
        self._view.readButton.clicked.connect(self._readPath)
        self._view.manualButton.clicked.connect(self._sendSerial)

        # print(path)

    def _readPath(self):
        """
            read the path of the image and sets it to the pixmap parameter
        """
        print("clicked")
        path = self._view.pathToImage.text()
        self._view.pathToImagelabel.setText(path)
        print(path)

    def _sendSerial(self):
        dist = self._view.moveCommand.text()
        print(dist)
        ser = serial.Serial("/dev/ttyUSB0")
        print(ser.name)
        ser.write("MOVECONV" + str(dist))
        ser.close()
