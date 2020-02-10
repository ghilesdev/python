import math
import copy
import numpy as np


class Vertex(object):
    def __init__(self, _x=0, _y=0, _name=""):
        self.x = _x
        self.y = _y
        self.name = _name
        self.marked = None
        self.uniqueID = None
        self.type = None  # 'line', 'curve' or 'corner' Describes the vertex type within a polyline for example
        self.pathVect = None  # vector formed by vertex with previous vertex in a path (0, 0) if no previous vertex
        self.pathAngle = (
            None  # angle formed by the vertex with adjacent vertices in a path
        )
        self.edge = None  # edge object, containing all vertices that are in the same edge. It's actually a list of 2 edge objects max, beacause of corners, taht are part of two edges
        self.mark_setting = None
        self.is_original = False
        self.percentage = None

    def __str__(self):
        return f"[{self.x}, {self.y}, '{self.name}']"

    def __repr__(self):
        return f"Vertex({self.x}, {self.y}, '{self.name}')"

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, v)
        return result

    def vertexCoordinates(self):
        return [self.x, self.y]

    def getMiddle(self, vertexB):
        x = (self.x + vertexB.x) / 2
        y = (self.y + vertexB.y) / 2
        return Vertex(x, y)

    def symmetrize(self, symParams):  # transform to symmetric polyline by axis
        self.x = -self.x + 2 * symParams[1] if symParams[0] == "y" else self.x
        self.y = (
            -self.y + 2 * symParams[1] if symParams[0] == "x= Vertex(0,0)" else self.y
        )

    def is_equal(self, vertex, tolerance=0.1):
        if abs(self.x - vertex.x) <= tolerance and abs(self.y - vertex.y) <= tolerance:
            return True
        return False

    def rename(self, newName):
        self.name = newName
        return self

    def offsetVertex(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def intersection(
        self, u, v, A, B
    ):  # returns vertex at the intersection of lines defined by u and v vectors, respectively starting at A and B
        xdiff = Vertex(-u.x, -v.x)
        ydiff = Vertex(-u.y, -v.y)

        def det(a, b):
            return a.x * b.y - a.y * b.x

        div = det(xdiff, ydiff)
        if div == 0:
            return
        d = Vertex(det(A, A.addVector(u)), det(B, B.addVector(v)))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return Vertex(x, y)

    def segmentProj(
        self, A, B, tolerance=0.1
    ):  # project self (P) to segment formed by vertices A and B
        P = self
        if A.is_equal(B, tolerance):
            return A
        AB = B.vectorize(A)  # AB vector
        N = Vertex(-AB.y, AB.x)  # normal to AB
        return Vertex().intersection(AB, N, A, P)

    def segmentDist(
        self, A, B, tolerance=0.1
    ):  # distance to segment formed by vertices A and B
        H = self.segmentProj(A, B)  # normal projection on AB
        return self.dist(H)

    def onPolyline(
        self, poly, tolerance=0.1
    ):  # if self is on polyline p, returns a vertex index i after which to insert self on p
        if len(poly.vertices) < 2:
            return None
        for i in range(0, len(poly.vertices) - 1):
            if poly.vertices[i].dist(poly.vertices[i + 1]) < tolerance:
                continue
            elif self.dist(poly.vertices[i]) < tolerance:
                return i
            elif self.dist(poly.vertices[i + 1]) < tolerance:
                return i + 1

            if (
                self.vectorize(poly.vertices[i]).dotProd(
                    self.vectorize(poly.vertices[i + 1])
                )
                < 0
                and self.segmentDist(poly.vertices[i], poly.vertices[i + 1]) < tolerance
            ):
                return i
        return None

    def rotateVertex(self, angle, center=None):
        if center is None:
            center = Vertex(0, 0)
        angle = angle * math.pi / 180
        x = self.x - center.x
        y = self.y - center.y
        self.x = x * math.cos(angle) - y * math.sin(angle) + center.x
        self.y = x * math.sin(angle) + y * math.cos(angle) + center.y
        return self

    def dist(self, vertex):  # distance to vertex vertex
        return ((self.x - vertex.x) ** 2 + (self.y - vertex.y) ** 2) ** 0.5

    def vectorize(self, o):
        return Vertex(self.x - o.x, self.y - o.y)

    def norm(self):  # calculate vector norm
        return self.dist(Vertex(0, 0))

    def angleToVector(self, v):
        n = v.norm()
        n1 = self.norm()
        if self.norm == 0 or n == 0:
            return 0
        elif self.dotProd(v) > 0:
            return (
                np.arcsin(round(self.crossProd(v) / self.norm() / n, 5)) / np.pi * 180
            )  # rounding necessary here due to limits close to 0
        else:
            return (
                (np.pi - np.arcsin(round(self.crossProd(v) / self.norm() / n, 5)))
                / np.pi
                * 180
            )  # rounding necessary here

    def addVector(self, vector, inplace=False):
        if inplace:
            self.x = self.x + vector.x
            self.y = self.y + vector.y
        else:
            new = Vertex()
            new.x = self.x + vector.x
            new.y = self.y + vector.y
            return new

    def getNormal(self):  # returns normal vector to self, when self represents a vector
        return Vertex(-self.y, self.x)

    def crossProd(self, vector):  # returns (cross) vectorial product of self and vector
        return self.x * vector.y - self.y * vector.x

    def vectors_angle(self, vector):
        return math.acos(self.dotProd(vector) / (self.norm() * vector.norm())) * 360

    def cross_product(self, vector):
        return self.norm() * self.norm() * math.fabs(self.vectors_angle(vector))

    def dotProd(self, vector):  # returns (dot) scalar product of self and vectors
        return self.x * vector.x + self.y * vector.y

    def normalize(self):  # reduces vector to norm = 1
        if self.norm() != 0:
            n = self.norm()
            self.x = self.x * (1 / n)
            self.y = self.y * (1 / n)

    def scale(self, scale):
        new = Vertex()
        new.x = self.x * scale
        new.y = self.y * scale
        return new

    def scaleXY(self, xScale, yScale):
        self.x *= 1 + xScale
        self.y *= 1 + yScale

    def to10th(self):  # cast vertex to 10th of millimeter integers
        self.x = int(round(self.x * 10, 0))
        self.y = int(round(self.y * 10, 0))

    def toMilli(self):  # cast vertex to millimeter integers
        self.x = int(round(self.x * 10, 0))
        self.y = int(round(self.y * 10, 0))

    def setName(self, name, inplace=False):
        self.name = name
        if inplace:
            return self

    def filterCornerName(self, cornersNames):
        if not (self.name in [""] + cornersNames):
            self.setName("")
        return self

    def transform_into_segment(self, length=2):
        from tekyntools.geometryObjects.polyline import Polyline

        """
            Create horizontal segment of given length centered on input vertex
            
            parameters:
                center_vertex: (Vertex) center of the output segment
                length: (int) length of the output segment
                
            return:
                (Polyline) segment: horizontal segment of given length centered on self
        """
        half_length = length / 2
        right_vertex = Vertex(self.x + half_length, self.y)
        left_vertex = Vertex(self.x - half_length, self.y)
        return Polyline([left_vertex, right_vertex])

    def translateVertex(self, translation):
        def to_int(name):
            return int(name.replace("# ", ""))

        if self.name != "":
            name_value = to_int(self.name) + translation
            self.name = "# " + str(name_value)
        return self

    def set_vertex_as_original(self):
        self.is_original = True
        return self

    def deepcopy_vertex(self):
        return Vertex(self.x, self.y, self.name)
