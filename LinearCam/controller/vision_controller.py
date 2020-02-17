class controller:
    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _connectSignals(self):
        self._view.readButton.clicked.connect(self._readPath)

        # print(path)

    def _readPath(self):
        """
            read the path of the image and sets it to the pixmap parameter
        """
        print("clicked")
        path = self._view.pathToImage.text()
        self._view.pathToImagelabel.setText(path)
        print(path)
