from tekyntools.geometryObjects.vertex import Vertex


class Notch(Vertex):
    def __init__(
        self,
        notchShape="TRI",
        width=10.0,
        height=5.0,
        direction=0,
        ghost=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.notchShape = notchShape
        self.width = width
        self.height = height
        self.direction = direction
        self.ghost_sizes = []

        self.ghost = ghost
        self.ghost_sizes = []

    def is_ghost(self):
        return self.ghost
