from LinearCam.view.vision_view import GUI


class controller:
    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _connectSignals(self):
        path = self._view.readButton.clicked.connect(self._readPath)
        print(path)

    def _readPath(self):
        return self._view.pathToImage.getText()
