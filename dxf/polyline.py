import numpy as np
import pandas as pd
import copy
import pyclipper
from shapely.geometry import LineString
from simplification.cutil import simplify_coords

from tekyntools.geometryObjects.Edge import Edge
from tekyntools.geometryObjects.mathTools import *


class Polyline:
    def __init__(self, vertList=None):
        self.vertices = (
            [] if vertList == None else vertList
        )  # Mutable (such as list) cannot be default argument, therefore use None and set [] in this conditional init
        self.shapePolyline = []
        self.authAngles = []  # list of rotation angles authorized for the shape
        self.id = 0
        self.isClosed = True
        self.uniqueID = None  # id in tree created before the placement
        self.articleID = -1  # id of the article to which a polyline belongs in an order
        self.idShapeSeq = -1  # TODO ?? Difference with unique ID
        self.uniqueID = -1  # unique id of a polyline in an order
        self.width = 0
        self.height = 0
        self.offsetx = 0  # used in nfp calculation for holes placements
        self.offsety = 0  # used in nfp calculation for holes placements
        self.isMarking = 0  # polylines are affected to marking (1) or cut (0) at the end of the nester
        self.isShapePolyline = 0
        self.isSkeleton = 0  # used in cutSection to detect if the polyline is skeleton polyline or not
        self.symAxis = ""  # symmertry axis
        self.d = 0  # distance of symetry axis to origin
        self.is_strip = False
        # self.overlap = False
        self.overlaps_id = []
        self.size = ""
        self.is_rotated = False
        self.rot_angle = 0
        self.idShapeDb = None
        self.sequence = 0
        self.newRulesPolys = []
        self.ghost = False
        self.type = None

    def __str__(self):
        out = "Polyline :\n"
        for v in self.vertices:
            out += "vertex : x = %.1f; y = %.1f; " % (v.x, v.y)
            out += "RUL = %s; ID = %s \n" % (v.name, v.uniqueID)
        return out

    def __repr__(self):
        return f'Polyline([{", ".join([vertex.__repr__() for vertex in self.vertices])}])'

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
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __len__(self):
        return self.vertices.__len__()

    def __iter__(self):
        return self.vertices.__iter__()

    def __next__(self):
        return self.vertices.__next__()

    def __getitem__(self, y):
        return self.vertices.__getitem__(y)

    def append(self, vertex):
        self.vertices.append(vertex)

    def assignRul(
        self, rulVertex, tolerance=0.1
    ):  # assign a rule from a ruled vertex to the corresponding vertex in a polyline
        for v in self.vertices:
            if v.is_equal(rulVertex, tolerance):
                v.name = rulVertex.name
        return

    def assignRules(
        self, rulVertexList, tolerance=0.1
    ):  # assign a rule from a ruled vertex to the corresponding vertex in a polyline
        vertices = copy.deepcopy(self.vertices)
        n = len(vertices)
        names = {}
        removed_nb = 0
        for v in rulVertexList:
            if not pd.isnull(v):
                found = False
                i = 0
                while not found and i < n:
                    rulVertex = vertices[i]
                    found = v.is_equal(rulVertex, tolerance)
                    if found:
                        names[i + removed_nb] = v.name
                        vertices.pop(i)
                        removed_nb += 1
                    i += 1
        for i, name in names.items():
            self.vertices[i].setName(name)
        return self

    def area(self):
        return pyclipper.Area(self.polylineToTuple())

    def isHoarding(self, ratio=0.5):
        bounds = self.getBounds()
        height = bounds["top"] - bounds["bottom"]
        length = bounds["right"] - bounds["left"]
        boundsArea = height * length
        polyArea = self.area()
        return (polyArea / boundsArea) < ratio

    def symmetrize(self, symParams=None):  # transform to symmetric polyline by axis
        if symParams == None:
            symParams = self.getSymParams()
        for v in self.vertices:
            if symParams[0] == "y":
                v.x = -v.x + 2 * symParams[1]
            if symParams[0] == "x":
                v.y = -v.y + 2 * symParams[1]

    def getSymParams(self):  # returns symmetry axis and distance to 0 of a polyline
        if len(self.vertices) == 0:
            return ["y", 0]
        bounds = self.getBounds()
        dist_sym = 0
        if abs(self.vertices[0].x - self.vertices[-1].x) <= abs(
            self.vertices[0].y - self.vertices[-1].y
        ):
            self.symAxis = "y"
            side = self.vertices[0].x
            self.dist_sym = (
                bounds["left"]
                if abs(side - bounds["left"]) < abs(side - bounds["right"])
                else bounds["right"]
            )
        else:
            side = self.vertices[0].y
            self.symAxis = "x"
            self.dist_sym = (
                bounds["bottom"]
                if abs(side - bounds["bottom"]) < abs(side - bounds["top"])
                else bounds["top"]
            )
        return [self.symAxis, self.dist_sym]

    def roundPolylineVertices(self, decimal=0):
        self.vertices = [
            Vertex(round(v.x, decimal), round(v.y), decimal) for v in self.vertices
        ]

    def rebaseClosedPolyVertices(
        self, newStart, pop=True
    ):  # change starting vertex of a closed polyline to newStart
        l = len(self.vertices)
        if l > 2:
            self.vertices = (
                self.vertices[newStart:]
                + self.vertices[:newStart]
                + [self.vertices[newStart]]
            )
            if pop:
                self.vertices.pop(l - newStart)

    def polylineToTuple(self):
        poly_tuple = []
        for v in self.vertices:
            poly_tuple.append((v.x, v.y))
        return poly_tuple

    def polylineToTupleOpt(self):  ##special function for nfp worker
        return list(map(lambda v: (v.x * 10000000, v.y * 10000000), self.vertices))

    def polylineToTupleOpt1(self):  ##special function for nfp worker
        return list(map(lambda v: (v.x * -10000000, v.y * -10000000), self.vertices))

    def addVertex(self, vertex):
        self.vertices.append(vertex)

    def addVertices(self, vertex_list):  # to transform a list of [x, y] to a Polyline
        for v in vertex_list:
            self.addVertex(v)
        return self

    def getHeight(self):
        bounds = self.getBounds()
        return bounds["top"] - bounds["bottom"]

    def getLength(self):
        length = 0
        if not self.vertices:
            return 0
        vertex_last = self.vertices[0]
        for i in range(1, len(self.vertices)):
            vertex_current = self.vertices[i]
            length += vertex_last.dist(vertex_current)
            vertex_last = vertex_current
        return length

    def removeOldRuledVertices(self, tekyn_rule_code):
        self.vertices = list(
            filter(
                lambda v: v.name == ""
                or str(tekyn_rule_code) in v.name
                or v.type == "corner",
                self.vertices,
            )
        )

    def insertVertex(
        self, toInsert, pos=None, tolerance=0.01, replace=0
    ):  # insert vertex in a Polyline, either with a given position pos, or between the two closest vertices
        l = len(self.vertices)
        distances = []
        if pos == None:
            for i, v in enumerate(self.vertices):
                vnext = self.vertices[(i + 1) % l]
                dist = distance(toInsert, v, vnext)
                if onSegment(v, vnext, toInsert):
                    pos = i
                    break
                else:
                    distances.append(dist[1])
                pos = distances.index(min(distances))
        # print("pos: ", pos)
        if toInsert.is_equal(
            self.vertices[pos], tolerance
        ):  # avoid creating duplicates
            self.vertices[pos].name = toInsert.name
        # elif toInsert.is_equal(self.vertices[pos+1], tolerance):
        #     self.vertices[pos].name = toInsert.name
        else:
            self.vertices = (
                self.vertices[: pos + 1]
                + [copy.deepcopy(toInsert)]
                + self.vertices[pos + 1 :]
            )

    def listToPolyline(
        self, list, scale=1
    ):  # to transform a list of [x, y] to a Polyline
        for p in list:
            self.addVertex(Vertex(p[0] / scale, p[1] / scale))
        return self

    def polylineToList(self):
        list = [[vertex.x, vertex.y] for vertex in self.vertices]
        return list

    def cleanPolyline(self, epsilon):
        """
            Ramer–Douglas–Peucker algorithm to reduce number of vertices in polyline.
            More information here: https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
            :param epsilon:
            :return:
        """
        coords = self.polylineToList()
        clean_coords = simplify_coords(coords, epsilon)
        clean_poly = copy.deepcopy(self)
        clean_poly.vertices = Polyline().listToPolyline(clean_coords).vertices
        for remaining_vertex in clean_poly.vertices:
            for w in self.vertices:
                if remaining_vertex.is_equal(w, tolerance=0.01):
                    remaining_vertex.name = w.name
                    continue
        return clean_poly

    def offsetPolyline(
        self, offset, tolerance=0.1
    ):  # offsets polyline by a given value
        if offset == 0:
            return self
        miterlimit = offset
        p = (
            self.polylineToArrayOfPoints()
        )  # return a list of points, required input for pyclipper
        clipper = pyclipper.PyclipperOffset(miterlimit, tolerance)
        clipper.AddPath(p, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        offsetPath = clipper.Execute(
            offset
        )  # clipper returns only a list of int values to be matched back to self.vertices

        self.vertices = []
        if (
            len(offsetPath) == 1
        ):  # after offset, pyclipper may return several polylines, thus this test. else would be an error
            j = 0
            while j < len(offsetPath[0]):
                if j >= len(self.vertices):
                    self.vertices.append(
                        Vertex(offsetPath[0][j][0], offsetPath[0][j][1])
                    )
                else:
                    self.vertices[j] = Vertex(offsetPath[0][j][0], offsetPath[0][j][1])
                j += 1
            while j < len(
                self.vertices
            ):  # if offset has less vertex than original polyline (holes), delete extra vertices
                del self.vertices[j]
                j += 1
        self.vertices.append(copy.deepcopy(self.vertices[0]))

    def polylineToArrayOfPoints(
        self,
    ):  # returns an array containing only vertices in the simple [x, y] format
        points = []
        for v in self.vertices:
            points.append([v.x, v.y])
        return points

    def rotatePolyline(self, angle, center=Vertex(0, 0)):
        for v in self.vertices:
            v.rotateVertex(angle, center)
        self.getBounds()
        # return self

    def rebaseClosedPolylineVertices(
        self, newStart, pop=True
    ):  # change starting vertex of a closed polyline to newStart
        l = len(self.vertices)
        if l > 2:
            self.vertices = (
                self.vertices[newStart:]
                + self.vertices[:newStart]
                + [self.vertices[newStart]]
            )
            if pop:
                self.vertices.pop(l - newStart)

    def getPolylineTop(self):
        return max(self.vertices, key=lambda v: v.y).y

    def getBounds(self):
        if len(self.vertices) == 0:
            return {"left": 0, "right": 0, "bottom": 0, "top": 0}
        x_coords, y_coords = zip(*[(v.x, v.y) for v in self.vertices])
        left, right = min(x_coords), max(x_coords)
        bottom, top = min(y_coords), max(y_coords)
        # FIXME It is not a setter !!!! WTF Some time must be spent on verifying that we can removed
        self.width = abs(right - left)
        self.height = abs(top - bottom)
        return {"left": left, "right": right, "bottom": bottom, "top": top}

    def getBoundsRectanglePolyline(self, names=None):
        rectPoly = Polyline()
        bounds = self.getBounds()
        if names is None:
            names = [""] * 5
        v1 = Vertex(bounds["left"], bounds["top"], names[0])
        v2 = Vertex(bounds["left"], bounds["bottom"], names[1])
        v3 = Vertex(bounds["right"], bounds["bottom"], names[2])
        v4 = Vertex(bounds["right"], bounds["top"], names[3])
        v5 = Vertex(bounds["left"], bounds["top"], names[4])
        rectPoly.vertices = [v1, v2, v3, v4, v5]
        return rectPoly

    def mergePolylines(
        self, polyline, tolerance=1
    ):  # merges two polylines together by their common end if any # This can and should be refactorized.
        if self.vertices[0].is_equal(polyline.vertices[0], tolerance) and self.vertices[
            -1
        ].is_equal(polyline.vertices[-1], tolerance):
            new_list = self.vertices[:-1]
            new_list.extend(polyline.vertices[::-1])
            self.vertices = new_list
        elif self.vertices[0].is_equal(
            polyline.vertices[-1], tolerance
        ) and self.vertices[-1].is_equal(polyline.vertices[0], tolerance):
            self.vertices.extend(polyline.vertices[1:])
        elif self.vertices[0].is_equal(polyline.vertices[-1], tolerance):
            new_list = polyline.vertices.extend(self.vertices[1:])
            self.vertices = new_list
        elif self.vertices[0].is_equal(polyline.vertices[0], tolerance):
            new_list = polyline.vertices[::-1].extend(self.vertices[1:])
            self.vertices = new_list
        elif self.vertices[-1].is_equal(polyline.vertices[-1], tolerance):
            new_list = self.vertices[:-1]
            new_list.extend(polyline.vertices[::-1])
            self.vertices = new_list
        elif self.vertices[-1].is_equal(polyline.vertices[0], tolerance):
            new_list = self.vertices[:-1]
            new_list.extend(polyline.vertices[::-1])
            self.vertices = new_list
        else:
            new_list = self.vertices[:-1]
            new_list.extend(polyline.vertices[::-1])
            self.vertices = new_list

    def mergePolylineList(self, list):
        merge = Polyline()
        for p in list:
            merge.vertices.extend(p.vertices)
        return merge

    def getWidth(self):
        bounds = self.getBounds()
        self.width = abs(bounds["left"] - bounds["right"])
        return self.width

    def getHeight(self):
        bounds = self.getBounds()
        self.height = abs(bounds["bottom"] - bounds["top"])
        return self.height

    def popDuplicates(self, tolerance=0.5):
        # FIXME
        """
            Function to pop duplicate vertices and make sure the resulting polyline is still closed
        """
        i = 1
        closed = self.vertices[0].is_equal(self.vertices[-1], tolerance=0)
        while i < len(self.vertices):
            if self.vertices[i].is_equal(self.vertices[i - 1], tolerance):
                if self.vertices[i].name == "":
                    self.vertices.pop(i)
                else:
                    self.vertices.pop(i - 1)
                i -= 1
            i += 1
        if closed and not (
            self.vertices[0].is_equal(self.vertices[-1], tolerance=0)
        ):  # if closed polyline was opened in the process
            self.vertices.append(copy.deepcopy(self.vertices[0]))

    def rebasePolyline(self, deltaX, deltaY):  # TODO: redundant with next
        for v in self.vertices:
            v.x += deltaX
            v.y += deltaY

    def translatePoly(self, targetX, targetY):  # TODO: redundant with previous
        for vertex in self.vertices:
            vertex.x += targetX
            vertex.y += targetY

    def scalePolyline(self, scale):
        for v in self.vertices:
            v.x *= scale
            v.y *= scale
        return self

    def scaleXY(self, xScale, yScale):
        for v in self.vertices:
            v.x *= 1 + xScale
            v.y *= 1 + yScale
        return self

    def vertexInPolyline(
        self, _vertex, tolerance=0.001
    ):  # Return True if a vertex is inside a closed polyline
        if len(self.vertices) < 3:
            return None
        inside = False
        if hasattr(self, "offsetx"):
            offsetx = self.offsetx
        else:
            offsetx = 0
        if hasattr(self, "offsety"):
            offsety = self.offsety
        else:
            offsety = 0

        i = 0
        j = len(self.vertices) - 1
        while i < len(self.vertices):

            Vi = copy.deepcopy(self.vertices[i])
            Vi.offsetVertex(offsetx, offsety)
            Vj = copy.deepcopy(self.vertices[j])
            Vj.offsetVertex(offsetx, offsety)

            if _vertex.is_equal(Vi, tolerance):
                return None  # no result

            if onSegment(Vi, Vj, _vertex, tolerance):
                return None  # exactly on the segment

            if Vj.is_equal(Vi, tolerance):  # ignore very small lines
                pass
            else:
                intersect = ((Vi.y > _vertex.y) != (Vj.y > _vertex.y)) and (
                    _vertex.x
                    < (Vj.x - Vi.x) * (_vertex.y - Vi.y) / (Vj.y - Vi.y) + Vi.x
                )
                if intersect:
                    if inside == False:
                        inside = True
                    else:
                        inside = False
            j = i
            i += 1
        return inside

    def polylineProjectionDistance(
        self, b, direction, TOL=0.001
    ):  # distance between polylines a and b parallel to direction vector
        if hasattr(b, "offsetx"):
            Boffsetx = b.offsetx
        else:
            Boffsetx = 0
        if hasattr(b, "offsety"):
            Boffsety = b.offsety
        else:
            Boffsety = 0
        if hasattr(self, "offsetx"):
            Aoffsetx = self.offsetx
        else:
            Aoffsetx = 0
        if hasattr(self, "offsety"):
            Aoffsety = self.offsety
        else:
            Aoffsety = 0

        A = copy.deepcopy(self)
        B = copy.deepcopy(b)

        # close tjhe loop for polygons
        if A.vertices[0].x != A.vertices[-1].x or A.vertices[0].y != A.vertices[-1].y:
            A.append(A.vertices[0])

        if B.vertices[0].x != B.vertices[-1].x or B.vertices[0].y != B.vertices[-1].y:
            B.append(B.vertices[0])

        edgeA = A
        edgeB = B

        distance = None
        i = 0
        while i < len(edgeB.vertices):
            # the shortest/most negative projection of B onto A
            minprojection = None
            minp = None
            j = 0
            while j < len(edgeA.vertices) - 1:
                p = Vertex(
                    edgeB.vertices[i].x + Boffsetx, edgeB.vertices[i].y + Boffsety
                )
                s1 = Vertex(
                    edgeA.vertices[j].x + Aoffsetx, edgeA.vertices[j].y + Aoffsety
                )
                s2 = Vertex(
                    edgeA.vertices[j + 1].x + Aoffsetx,
                    edgeA.vertices[j + 1].y + Aoffsety,
                )

                if (
                    math.fabs((s2.y - s1.y) * direction.x - (s2.x - s1.x) * direction.y)
                    >= TOL
                ):
                    # project point, ignore edge boundaries
                    d = pointDistance(
                        p, s1, s2, direction
                    )  # distance from p to [s1s2] segment
                    if d != None and (minprojection == None or d < minprojection):
                        minprojection = d
                        minp = p
                j += 1
            if minprojection != None and (distance == None or minprojection > distance):
                distance = minprojection
            i += 1
        return distance

    def pIntersect(
        self, B
    ):  # test if polygons have at least one intersection using shapely
        c1 = self.polylineToTuple()
        c2 = B.polylineToTuple()
        p1 = LineString(c1)
        p2 = LineString(c2)
        return p1.intersects(p2)

    def sliceVertices(
        self, vList, keepBounds=True
    ):  # cuts out all vertices in vList from self and returns the list of resulting polyline segments
        # if keepBounds is True, slicing keeps the bounds of sliced sections
        sIdxList = []  # indices of vertices to slice in self
        for slice in vList:
            for i, v in enumerate(self.vertices):
                if v.is_equal(slice):
                    sIdxList.append(i)
        sIdxList.sort()

        verts = copy.deepcopy(self.vertices)
        sList = []  # list of remaining sections of self

        lastIdx = None
        for i, v in enumerate(verts[:-1]):
            if i in sIdxList:
                if (
                    lastIdx == None and i > 0
                ):  # end of first section if first vert is not a slice
                    if keepBounds:
                        sList.append(verts[: i + 1])
                    else:
                        sList.append(verts[:i])
                elif lastIdx != None and i - lastIdx > 1:  # end of a section
                    if keepBounds:
                        sList.append(verts[lastIdx : i + 1])
                    else:
                        sList.append(verts[lastIdx + 1 : i])
                lastIdx = i

        if lastIdx != None and sIdxList[-1] != len(verts) - 1:
            if keepBounds:
                sList.append(verts[lastIdx:])
            else:
                sList.append(verts[lastIdx + 1 :])

        if len(sList) > 1 and sList[0][0].is_equal(
            sList[-1][-1]
        ):  # If first and last section touch one another
            sList[-1] += sList[0][1:]
            sList.pop(0)

        pList = [Polyline(s) for s in sList]

        return pList

    def overlap(
        self, p, tolerance=0.01, rip=None
    ):  # returns list of common vertices of self and p, ...
        # if rip = 'source', 'other' or 'both', rips common vertices from self, p or both and returns list of remaining polylines
        commonVertices = []
        # Ensure common sections are delimited by vertices
        for v in self.vertices:
            j = v.onPolyline(p, tolerance)  # project common vertices from self to p
            if j != None:  # p crosses i vertex of self
                p.insertVertex(v, j, tolerance)
                commonVertices.append(v)
        for v in p.vertices:  # project common vertices from p to self
            j = v.onPolyline(self, tolerance)
            if j != None:  # p crosses i vertex of self
                self.insertVertex(v, j, tolerance)
                commonVertices.append(v)

        # Remove duplicates
        commonVertices.sort(
            key=lambda v: (v.x, v.y)
        )  # sort commonVertices by x then by y
        cv = Polyline(commonVertices)
        cv.popDuplicates()
        commonVertices = cv.vertices
        if rip == None:
            return

        # Rip common vertices
        if rip in ["source", "both"]:
            selfSections = self.sliceVertices(commonVertices)

        if rip in ["other", "both"]:
            pSections = p.sliceVertices(commonVertices)

        return selfSections, pSections

    def intersect(
        self, B, tolerance=0.001
    ):  # TODO: check whether to keep pIntersect or intersect
        if hasattr(self, "offsetx"):
            Aoffsetx = self.offsetx
        else:
            Aoffsetx = 0
        if hasattr(self, "offsety"):
            Aoffsety = self.offsety
        else:
            Aoffsety = 0

        if hasattr(B, "offsetx"):
            Boffsetx = B.offsetx
        else:
            Boffsetx = 0
        if hasattr(B, "offsety"):
            Boffsety = B.offsety
        else:
            Boffsety = 0

        A = copy.deepcopy(self)
        B = copy.deepcopy(B)

        i = 0
        while i < len(A.vertices) - 1:
            j = 0
            while j < len(B.vertices) - 1:
                a1 = Vertex(A.vertices[i].x + Aoffsetx, A.vertices[i].y + Aoffsety)
                a2 = Vertex(
                    A.vertices[i + 1].x + Aoffsetx, A.vertices[i + 1].y + Aoffsety
                )
                b1 = Vertex(B.vertices[j].x + Boffsetx, B.vertices[j].y + Boffsety)
                b2 = Vertex(
                    B.vertices[j + 1].x + Boffsetx, B.vertices[j + 1].y + Boffsety
                )
                if j == 0:
                    prevbindex = len(B.vertices) - 1
                else:
                    prevbindex = j - 1
                if i == 0:
                    prevaindex = len(A.vertices) - 1
                else:
                    prevaindex = i - 1
                if j + 1 == len(B.vertices) - 1:
                    nextbindex = 0
                else:
                    nextbindex = j + 2
                if i + 1 == len(A.vertices) - 1:
                    nextaindex = 0
                else:
                    nextaindex = i + 2

                # go even further back if we happen to hit on a loop end point
                if B.vertices[prevbindex] == B.vertices[j] or B.vertices[
                    prevbindex
                ].is_equal(B.vertices[j], tolerance):
                    if prevbindex == 0:
                        prevbindex = len(B.vertices) - 1
                    else:
                        prevbindex -= 1

                if A.vertices[prevaindex] == A.vertices[i] or A.vertices[
                    prevaindex
                ].is_equal(A.vertices[i], tolerance):
                    if prevaindex == 0:
                        prevaindex = len(A.vertices) - 1
                    else:
                        prevaindex -= 1
                # go even further forward if we happen to hit on a loop end point
                if B.vertices[nextbindex] == B.vertices[j + 1] or B.vertices[
                    nextbindex
                ].is_equal(B.vertices[j + 1], tolerance):
                    if nextbindex == len(B.vertices) - 1:
                        nextbindex = 0
                    else:
                        nextbindex += 1

                if A.vertices[nextaindex] == A.vertices[i + 1] or A.vertices[
                    nextaindex
                ].is_equal(A.vertices[i + 1], tolerance):
                    if nextaindex == len(A.vertices) - 1:
                        nextaindex = 0
                    else:
                        nextaindex += 1

                a0 = Vertex(
                    A.vertices[prevaindex].x + Aoffsetx,
                    A.vertices[prevaindex].y + Aoffsety,
                )
                b0 = Vertex(
                    B.vertices[prevbindex].x + Boffsetx,
                    B.vertices[prevbindex].y + Boffsety,
                )

                a3 = Vertex(
                    A.vertices[nextaindex].x + Aoffsetx,
                    A.vertices[nextaindex].y + Aoffsety,
                )
                b3 = Vertex(
                    B.vertices[nextbindex].x + Boffsetx,
                    B.vertices[nextbindex].y + Boffsety,
                )

                if onSegment(a1, a2, b1) or a1.is_equal(b1, tolerance):
                    # if a point is on a segment, it could intersect or it could not. Check via the neighboring points
                    b0in = A.vertexInPolyline(b0)
                    b2in = A.vertexInPolyline(b2)
                    if (b0in == True and b2in == False) or (
                        b0in == False and b2in == True
                    ):
                        return True
                elif onSegment(a1, a2, b2) or a2.is_equal(b2, tolerance):
                    # if a point is on a segment, it could intersect or it could not. Check via the neighboring points
                    b1in = A.vertexInPolyline(b1)
                    b3in = A.vertexInPolyline(b3)
                    if (b1in == True and b3in == False) or (
                        b1in == False and b3in == True
                    ):
                        return True
                elif onSegment(b1, b2, a1) or a1.is_equal(b2, tolerance):
                    # if a point is on a segment, it could intersect or it could not. Check via the neighboring points
                    a0in = B.vertexInPolyline(a0)
                    a2in = B.vertexInPolyline(a2)
                    if (a0in == True and a2in == False) or (
                        a0in == False and a2in == True
                    ):
                        return True
                elif onSegment(b1, b2, a2) or a2.is_equal(b1, tolerance):
                    # if a point is on a segment, it could intersect or it could not. Check via the neighboring points
                    a1in = B.vertexInPolyline(a1)
                    a3in = B.vertexInPolyline(a3)
                    if (a1in == True and a3in == False) or (
                        a1in == False and a3in == True
                    ):
                        return True
                else:
                    p = lineIntersect(b1, b2, a1, a2)
                    if p != None:
                        return True
                j += 1
            i += 1
        return False

    def to10th(self):  # cast all vertices to 10th of millimeter integers
        for v in self.vertices:
            v.to10th()

    def toMilli(self):  # cast all vertices to millimeter integers
        for v in self.vertices:
            v.toMilli()

    def isRectangle(self, tolerance=0.001):
        p = pyclipper.Pyclipper()
        p.AddPath(self.polylineToTuple(), poly_type=pyclipper.PT_CLIP)
        bb = p.GetBounds()

        i = 0
        while i < len(self.vertices):
            minX = self.getBounds()["left"]
            minY = self.getBounds()["bottom"]
            if (
                abs(self.vertices[i].x - minX) > tolerance
                and abs(self.vertices[i].x - (minX + math.fabs(bb.right - bb.left)))
                > tolerance
            ):
                return False

            if (
                abs(self.vertices[i].y - minY) > tolerance
                and abs(self.vertices[i].y - (minY + math.fabs(bb.top - bb.bottom)))
                > tolerance
            ):
                return False
            i += 1
        return True

    def updateUniqueIDs(self):
        ids = []
        for v in self.vertices:
            ids.append(0 if v.uniqueID is None else int(v.uniqueID))
        for i, v in enumerate(self.vertices):
            if v.uniqueID is None:
                v.uniqueID = str(max(ids) + 1)
                ids[i] = int(v.uniqueID)

    def getPathVects(self):
        """
        Assigns the list of vectors from previous vertex to vertex
        Assigns the list of norms between vertex and previous vertex
        :return:
        """
        if len(self.vertices) < 2:
            return
        vects = list(
            map(
                lambda v1, v2: v1.vectorize(v2),
                self.vertices,
                self.vertices[-1:] + self.vertices[:-1],
            )
        )
        if self.vertices[0].is_equal(self.vertices[-1]):
            # drop closing vector (0, 0) for a closed polyline
            del vects[0]
            vects = vects[-1:] + vects[:-1]
        else:
            # for open polylines, first vector is null
            vects[0] = Vertex(0, 0, "")

        # assign pathVect attribute to vertices in polyline
        for i, v in enumerate(self.vertices):
            v.pathVect = vects[i % len(vects)]

        norms = list(map(lambda v: v.norm(), [v.pathVect for v in self.vertices]))

        # assign pathNorm attribute to vertices in polyline
        for i, v in enumerate(self.vertices):
            v.pathNorm = norms[i % len(norms)]

    def getPathAngles(self, tolerance=0.5, decimals=3):
        """
        Returns the list of norms between vertex and previous vertex
        :param tolerance:
        :param decimals:
        :return:
        """
        if len(self.vertices) < 3:
            return ["corner"] * len(self.vertices)
        # pop 'duplicates' as mini-vectors create undue angles

        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")

        self.popDuplicates(tolerance)

        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")

        self.getPathVects()  # get path vectors and norms

        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")

        vects = [v.pathVect for v in self.vertices]
        norms = [v.pathNorm for v in self.vertices]
        angles = list(
            map(
                lambda v1, v2, n1, n2: 0
                if n1 == 0 or n2 == 0
                else np.arcsin(round(v1.crossProd(v2.scale(-1)) / n1 / n2, 5))
                / np.pi
                * 180
                if v1.dotProd(v2.scale(-1)) > 0
                else (np.pi - np.arcsin(round(v1.crossProd(v2.scale(-1)) / n1 / n2, 5)))
                / np.pi
                * 180,  # rounding necessary here
                vects[1:] + vects[:1],
                vects,
                norms[1:] + norms[:1],
                norms,
            )
        )

        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")
        angles = list(map(lambda x: round(x, decimals), angles))
        #                                        vects, vects[-1:]+vects[:-1], norms, norms[-1:]+norms[:-1]))
        for i, v in enumerate(
            self.vertices
        ):  # give pathAngles attribute to vertices in polyline
            v.pathAngle = angles[i % len(angles)]

        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")

        # give pathAngles attribute to vertices in polyline
        for i, v in enumerate(self.vertices):
            v.pathAngle = angles[i % len(angles)]

    def get_position_percentages(self, nb_decimals=1):
        def set_percentage(v, percentage):
            v.percentage = percentage
            return v

        distances = self.getPointToPointDistancesList()
        cum_distances = np.cumsum(distances)
        percentages = list(cum_distances / cum_distances[-1] * 100)
        percentages = list(map(lambda x: round(x, nb_decimals), percentages))
        self.vertices = list(
            map(
                lambda x: set_percentage(x[0], x[1]),
                list(zip(self.vertices, percentages)),
            )
        )
        return percentages

    def check_poly_is_closed(self):
        """
            This function tests wether the first and last vertex are equal and have corner type
            :return:
        """

        [first_vertex, last_vertex] = [self.vertices[i] for i in [0, -1]]
        valid = first_vertex.is_equal(last_vertex, tolerance=0.001)

        if not valid:
            print(
                "first_vertex: ", [first_vertex.x, first_vertex.y, first_vertex.type],
            )
            print(
                "last_vertex: ", [last_vertex.x, last_vertex.y, last_vertex.type],
            )
            return False
        return valid

    def describePolyline(self, discAngle=15, cornerAngle=25):
        if len(self.vertices) < 3:
            return ["corner"] * len(self.vertices)

        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")

        self.getPathAngles(decimals=2, tolerance=0.1)

        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")
        self.get_position_percentages(nb_decimals=2)

        angles = [v.pathAngle for v in self.vertices]
        corners = list(
            map(
                lambda a: "corner"
                if abs(a) < (180 - cornerAngle) or abs(a) > (180 + cornerAngle)
                else a,
                angles,
            )
        )
        firstCorner = corners.index("corner")

        corners = (
            corners[firstCorner:] + corners[:firstCorner]
        )  # rebase list to start at a corner

        angles = (
            angles[firstCorner:] + angles[:firstCorner]
        )  # rebase list to start at a corner
        deviation = np.cumsum(
            list(map(lambda a: 180 - a, angles))
        )  # cumulated incremental angle - last value is 360deg

        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")

        for i, v in enumerate(corners):
            if v == "corner":
                curCorner = i
                type = "line"
            elif (
                abs(deviation[i] - deviation[curCorner]) < discAngle
            ):  # discriminate between line and curve by deviation value from previous corner
                corners[i] = "line"
            elif abs(deviation[i] - deviation[curCorner]) >= discAngle:
                corners[i] = "curve"
            self.vertices[(i + firstCorner) % (len(self.vertices))].type = corners[
                i
            ]  # assign pathAngles attribute to vertices in polyline
        valid = self.check_poly_is_closed()
        if not valid:
            raise Exception("Polyline is not closed on corner")

    def nameUnnamedCorners(self):
        unnamedCorners = [
            (i, v)
            for (i, v) in enumerate(self.vertices)
            if v.name == "" and v.type == "corner"
        ]
        if unnamedCorners:
            namedCorners = [
                v.name for v in self.vertices if v.name != "" and v.type == "corner"
            ]
            namedCornersIndexes = [
                i
                for i, v in enumerate(self.vertices)
                if v.name != "" and v.type == "corner"
            ]
            minNamedCornersIndex = min(namedCornersIndexes)
            maxNamedCornersIndex = max(namedCornersIndexes)
            before = len([x for x in unnamedCorners if x[0] < minNamedCornersIndex])
            after = len([x for x in unnamedCorners if x[0] > maxNamedCornersIndex])

            namesAsInt = list(map(lambda x: int(x[2:]), namedCorners))

            reversedlist = copy.deepcopy(namesAsInt)
            reversedlist.reverse()
            ascendant = sorted(namesAsInt) == namesAsInt
            descendant = sorted(namesAsInt) == reversedlist
            if not (ascendant) and not (descendant):
                print("Error: Vertices are not ordered")
            if ascendant:
                missingNames = [
                    x
                    for x in range(
                        min(namesAsInt) - before, max(namesAsInt) + after + 1
                    )
                    if not x in namesAsInt
                ]
            elif descendant:
                missingNames = [
                    x
                    for x in range(
                        max(namesAsInt) + before, min(namesAsInt) - after - 1, -1
                    )
                    if not x in namesAsInt
                ]

            print("missingNames: ", missingNames)

            ### DEBUG ###
            print(
                "vertices BEFORE: ",
                list(map(lambda v: (v.x, v.y, v.name), self.vertices)),
            )
            for i, v in enumerate([v for (i, v) in unnamedCorners]):
                v.name = "# " + str(missingNames[i])
            print(
                "vertices AFTER: ",
                list(map(lambda v: (v.x, v.y, v.name), self.vertices)),
            )

    def ruleAllCorners(
        self, tolerance=0.5, cornerAngle=15
    ):  # find all corners that have no rule and try to assign them the rule of a close vertex
        # Find unnamed corners
        self.describePolyline(cornerAngle=cornerAngle)

        unnamedCorners = [
            i
            for i, v in enumerate(self.vertices)
            if v.name == "" and v.type == "corner"
        ]

        print("unnamedCorners: ", len(unnamedCorners))

        if len(unnamedCorners) > 0:
            l = len(self.vertices)
            print(
                "Some corners are not ruled: \n",
                [
                    [str(v), v.type, v.pathAngle]
                    for i in unnamedCorners
                    for v in self.vertices[(i - 1) % l : (i + 2) % l]
                ],
            )
        # Assign any rule at less than tolerance distance to unnamed corners:
        for i in unnamedCorners:
            print(
                "self.vertices[(i-1)%l].dist(self.vertices[i]): ",
                self.vertices[(i - 1) % l].dist(self.vertices[i]),
            )
            print(
                "self.vertices[(i+1)%l].dist(self.vertices[i]): ",
                self.vertices[(i + 1) % l].dist(self.vertices[i]),
            )
            if self.vertices[(i - 1) % l].dist(self.vertices[i]) < tolerance:
                print(
                    "merged corner %s with corner %s"
                    % (self.vertices[i], self.vertices[(i - 1) % l])
                )
                self.vertices[i].name = self.vertices[(i - 1) % l].name
                self.vertices[(i - 1) % l].name = ""
                if self.vertices[i].name == "":
                    self.vertices[i].name = "corner"
            elif self.vertices[(i + 1) % l].dist(self.vertices[i]) < tolerance:
                print(
                    "merged corner %s with corner %s"
                    % (self.vertices[i], self.vertices[(i + 1) % l])
                )
                self.vertices[i].name = self.vertices[(i + 1) % l].name
                self.vertices[(i + 1) % l].name = ""
                if self.vertices[i].name == "":
                    self.vertices[i].name = "corner"
            else:
                print(
                    "Could not merge unruled corner %s with adjacent vertices. PLease check tolerance %0.2f mm"
                    % (self.vertices[i], tolerance)
                )
                exit()

    # def getRuledVerts(polyline, tolerance = 0.5, cornerAngle = 15, cleanUp = True, rulCorner = True):    # get all ruled vertices from a polyline    TODO: move to polyline object

    def getBoundsCenter(self):
        bounds = self.getBounds()
        vA = Vertex(bounds["left"], bounds["top"])
        vB = Vertex(bounds["right"], bounds["bottom"])
        return vA.getMiddle(vB)

    def getCenterPolyVector(self, center):
        polyCenter = self.getBoundsCenter()
        vector = center.vectorize(polyCenter)
        return vector

    def applyCurveUnity(self):
        enumVertices = list(
            map(lambda v: [v.type, self.vertices.index(v)], self.vertices)
        )
        corners = list(filter(lambda vList: vList[0] == "corner", enumVertices))
        cornersIds = list(map(lambda x: x[1], corners))
        for idx in range(0, len(cornersIds) - 1):
            idCornerA = cornersIds[idx]
            idCornerB = cornersIds[idx + 1]
            segment = self.vertices[idCornerA + 1 : idCornerB]
            curves = list(filter(lambda v: v.type == "curve", segment))
            if curves:
                for v in self.vertices[idCornerA + 1 : idCornerB]:
                    v.type = "curve"

    def getRuledVerts(
        polyline,
        shape,
        polyType,
        tolerance=0.5,
        discAngle=15,
        cornerAngle=25,
        cleanUp=True,
        rulCorner=True,
    ):  # get all ruled vertices from a polyline    TODO: move to polyline object
        # if cleanUp is True, delete every named vertex too close to another
        # if rulCorner is True, find all corners that have no rule and try to assign them the rule of a close vertex
        # tolerance is the minimum distance between two ruled vertices
        p = Polyline()  # list returned of all ruled vertices

        ### DEBUG ###
        # if 'FONDPCHDO' in shape.fileName:
        print("\n\nshape name: ", shape.fileName)
        corners = [v for v in polyline.vertices if v.name != "" and v.type == "corner"]
        corner_names = list(map(lambda v: v.name, corners))
        print("corners: \n", corner_names)
        if rulCorner:
            polyline.ruleAllCorners(tolerance, cornerAngle)
        #############

        for i, v in enumerate(polyline.vertices):
            if v.name != "" or v.type == "corner":
                if (
                    cleanUp
                    and len(p.vertices) > 1
                    and p.vertices[-1].is_equal(v, tolerance)
                ):  # skip doubles
                    continue
                else:
                    polyline.name_ = v.name == ""
                    if polyline.name_:
                        v.name = "corner"
                    p.vertices += [v]
        p.getPathVects()  # vects have changed

        if len(p.vertices) > 1 and p.vertices[0].is_equal(
            p.vertices[-1], tolerance
        ):  # for closed polyline drop doubled last vertex
            p.vertices = p.vertices[:-1]

        p.applyCurveUnity()

        if polyType in ["cutPolyline", "shapePolyline"]:
            p.vertices = list(
                filter(lambda v: v.type == "corner", p.vertices)
            )  ### Keep only corners

        return p.vertices

    def keepOnlyCornersNames(self, cornerNames):
        self.vertices = list(
            map(lambda v: v.filterCornerName(cornerNames), self.vertices)
        )
        return self

    def getEdgeFromVertex(
        self, i, notches, rotation, sym
    ):  ## i is the index of the vertex in the polyline
        ## When the initial vertex is the corner, the case handling may be not robust

        vertList = [self.vertices[i]]
        l = len(self.vertices)
        if (
            self.vertices[i].type == "corner"
        ):  ## If the vertex is a corner, the handling may not be robust
            if self.vertices[(i - 1) % l].type == "corner":
                vertList.insert(0, self.vertices[(i - 1) % l])
            elif self.vertices[(i + 1) % l].type == "corner":
                vertList.append(self.vertices[(i + 1) % l])
            return vertList
        else:
            k = 1
            while self.vertices[i - k].type != "corner":
                vertList.insert(0, self.vertices[(i - k) % l])
                k += 1
            vertList.insert(0, self.vertices[(i - k) % l])
            k = 1
            while self.vertices[(i + k) % l].type != "corner":
                vertList.append(self.vertices[(i + k) % l])
                k += 1
            vertList.append(self.vertices[(i + k) % l])

        # Dark bug patch here... The notch vertices representation were not rotated/mirrored, because not existant in the context of the prod shape...
        if notches:
            for i, v in enumerate(vertList):
                for n in notches:
                    if n.is_equal(v):
                        new = copy.deepcopy(n)
                        if sym == "SYM":
                            new.symmetrize(self.getSymParams())
                        new.rotateVertex(rotation)
                        if sym == "SYM":
                            new.x = -new.x
                            new.y = -new.y
                        vertList[i] = new

        return vertList

    def processVerticesEdges(
        self, notches=None, rotation=0, sym=""
    ):  ## Creates edges objects
        if (
            not self.vertices
        ):  # or self.vertices[0].edge: ## If poly has not any vertices, or the function has already been applied
            return
        if not self.vertices[0].type:
            self.describePolyline()

        edgeList = []
        for v in self.vertices:
            v.edge = None
        for i, v in enumerate(self.vertices):
            for edge in edgeList:
                if v in edge.vertices:
                    v.edge = edge
                    break
            if not v.edge:
                newEdge = Edge()
                newEdge.vertices = self.getEdgeFromVertex(i, notches, rotation, sym)
                v.edge = newEdge
                edgeList.append(newEdge)
        return edgeList

    def offsetPolySegment(self, spacing, rotation):
        if rotation:
            vA = self.vertices[0]
            vB = self.vertices[-1]
        else:
            vA = self.vertices[-1]
            vB = self.vertices[0]
        polyVect = vA.vectorize(vB)
        polyVect.normalize()
        normVect = polyVect.getNormal()
        normVect = normVect.scale(spacing)
        self.rebasePolyline(deltaX=normVect.x, deltaY=normVect.y)
        return self

    def getPolyRuleNames(
        self, name=""
    ):  ### name is a parameter allowing the user to filter vertices by a particular string name. If name = "# ", only names with "# " in it will be returned
        rulNames = list(
            map(lambda v: v.name, list(filter(lambda v: name in v.name, self.vertices)))
        )
        return rulNames

    def applySpacing(self, spacing):
        confirmSpacing = False
        if self.vertices:
            iteration = 0
            edges = self.processVerticesEdges()
            while not confirmSpacing and iteration < 2:
                rotation = self.getPolyRotation()
                if iteration > 0:
                    rotation = not (rotation)
                    print("Warning: rotation direction has changed")
                polySegmentsList = list(
                    map(lambda edge: Polyline(edge.vertices), edges)
                )
                offsetSegmentsList = list(
                    map(
                        lambda p: p.offsetPolySegment(
                            spacing=spacing, rotation=rotation
                        ),
                        copy.deepcopy(polySegmentsList),
                    )
                )  ### Offset those segments
                newVertices = []
                for poly in offsetSegmentsList:
                    newVertices += poly.vertices
                newPolyline = Polyline(newVertices)
                # print("newPolyline.area(): ", math.fabs(newPolyline.area()))
                # print("self.area(): ", math.fabs(self.area()))
                confirmSpacing = math.fabs(newPolyline.area()) > math.fabs(self.area())
                iteration += 1
            if confirmSpacing:
                self.vertices = newVertices
                # print("\n\n self.vertices BEFORE: ", list(map(lambda v: [v.x, v.y, v.name], self.vertices)))
                self.vertices = []
                for v in newPolyline.vertices:
                    self.vertices.append(copy.deepcopy(v))
                # print("\n self.vertices AFTER: ", list(map(lambda v: [v.x, v.y, v.name], self.vertices)))
            else:
                print("Warning: Spacing could not be applied to polyline")

    def getPolyRotation(self):
        n = len(self.vertices)
        if n >= 4:
            v1 = self.vertices[0]
            v2 = self.vertices[int(n / 4)]
            v3 = self.vertices[int(2 * n / 4)]
            v4 = self.vertices[int(3 * n / 4)]
            center = self.getBoundsCenter()
            vectList = [v.vectorize(center) for v in [v1, v2, v3, v4]]
            rotationVects = []
            for v_idx in range(0, n - 1):
                try:
                    vA = vectList[v_idx]
                    vB = vectList[v_idx + 1]
                    rotationVects.append(vA.angleToVector(vB))
                except:
                    pass
            rotation = not (sum([r < 0 for r in rotationVects]))
            # print(rotationVects)
            return rotation
        else:
            print(self.vertices)
            print("Not enough vertices to specify polyline rotation")
            exit()

    def renameHomonymousVertices(self, shapesFrame, newRulesCode):
        def getAllRuleNames(shapesFrame):
            ruleNamesList = []
            shapesFrame.applymap(
                lambda s: s.getShapeRuleNames(ruleNamesList, name="# ",)
            )
            return ruleNamesList

        allRuleNames = getAllRuleNames(shapesFrame)  # All the existing rule names
        allRulesValues = list(map(lambda x: int(x[2:]), allRuleNames))
        oldRuleValues = list(filter(lambda x: x < newRulesCode, allRulesValues))
        maxRuleNameValue = max(oldRuleValues)

        polyRules = list(
            map(lambda v: v.name, list(filter(lambda v: "# " in v.name, self.vertices)))
        )

        if polyRules:
            polyRuleValues = list(map(lambda x: int(x[2:]), polyRules))
            if polyRuleValues:
                closedOnCorner = polyRuleValues[0] == polyRuleValues[-1]
            else:
                print("polyRules: ", polyRules)
                print("polyRuleValues: ", polyRuleValues)

            if closedOnCorner:
                duplicate = not (
                    len(polyRuleValues[:-1]) == len(list(set(polyRuleValues[:-1])))
                )
                ### Warning ! The only possibility for having twice the same rule value is when the polyline is closed on a ruled point
            else:
                duplicate = not (
                    len(polyRuleValues[:-1]) == len(list(set(polyRuleValues[:-1])))
                )

            # print("duplicate: ", duplicate)
            if duplicate:  # Change rules values
                newRuleValues = range(
                    maxRuleNameValue + 1, maxRuleNameValue + 1 + len(polyRuleValues)
                )
                newRules = list(map(lambda x: "# " + str(x), newRuleValues))

                rul_idx = 0
                for v in self.vertices:
                    if v.name in polyRules:
                        v.setName(newRules[rul_idx])
                        rul_idx += 1
        return self

    def rebaseToFirstCornerVertex(self):
        # TODO Alaa dude test function
        # Test that number of vertices remains the same
        # Test that polyline length remains the same
        # Test that first corner type is 'corner'
        """
        Funciton deisgned to rebase polyline to first vertex which has attribute type =='corner"
        :return: None
        """
        verticesCorners = np.array(list(map(lambda v: v.type, self.vertices)))

        if list(verticesCorners):
            rebaseIdx = list(verticesCorners == "corner").index(True)
            self.rebaseClosedPolylineVertices(rebaseIdx)
        else:
            print("self.vertices: ", self.vertices)
            print("verticesCorners is empty ")
            from tekyntools.dxfTools.dxfWriter import listPolylineToDxf

            listPolylineToDxf(
                [self],
                path="tets_chino_polylines\\no_corner.dxf",
                reverse=False,
                flat=True,
            )
            # exit()
        # print("Poly closed on corner: ", self.vertices[0].name == self.vertices[-1].name != "")

        if self.vertices and self.vertices[0] is self.vertices[-1]:
            self.vertices[-1] = copy.deepcopy(self.vertices[-1])

    def cropPoly(self, cropBounds):
        [Xmin, Xmax, Ymin, Ymax] = list(cropBounds.values())
        self.vertices = list(
            filter(lambda v: Xmin <= v.x <= Xmax and Ymin <= v.y <= Ymax, self.vertices)
        )
        return self

    def closeOpenPoly(self):
        if self.vertices[0] != self.vertices[-1]:
            self.vertices[-1] != self.vertices[0]
        return self

    def getFriendshipRate(self, polyList, laize, decimals=3):
        poly = copy.deepcopy(self)
        cutPolyBin = copy.deepcopy(polyList)
        bounds = poly.getBounds()
        bounds["right"] = laize
        bounds["left"] = 0
        polyHeight = bounds["top"] - bounds["bottom"]
        polyZone = list(map(lambda p: p.cropPoly(bounds), cutPolyBin))
        polyZone = list(filter(lambda p: len(p.vertices) >= 3, polyZone))

        ### TODO finish open polylines ###
        # openPolylines = list(filter(lambda p: p.vertices[0] != p.vertices[-1], polyZone))
        ##################################

        polyZone = list(map(lambda p: p.closeOpenPoly(), polyZone))
        filledArea = sum(list(map(lambda p: math.fabs(p.area()), polyZone)))
        zoneArea = laize * polyHeight
        polyArea = math.fabs(poly.area())
        friendshipRate = (filledArea - polyArea) / (zoneArea - polyArea)
        return round(friendshipRate, decimals)

    def getThiknessRate(self):
        self.getBounds()
        height = self.height
        width = self.width
        return height / width

    def insideRectBounds(self, bounds):
        polyBounds = self.getBounds()
        [Xmin, Xmax, Ymin, Ymax] = polyBounds.values()
        [XlimMin, XlimMax, YlimMin, YlimMax] = bounds.values()
        return Xmin > XlimMin and Xmax < XlimMax and Ymin > YlimMin and Ymax < YlimMax

    def getPointToPointDistancesList(self):
        def tupleDistance(tuple, decimals=2):
            return round(tuple[1].dist(tuple[0]), decimals)

        verticesList = self.vertices
        list1 = verticesList + [verticesList[-1]]
        list2 = [verticesList[0]] + verticesList
        couplePointsList = zip(list1, list2)
        distList = list(map(tupleDistance, couplePointsList))
        return distList

    def forceClose(self, epsilon=5):
        distances = self.getPointToPointDistancesList()
        cumDistances = np.cumsum(distances)
        mask = cumDistances < epsilon
        vA_id = sum(mask)
        vB_id = vA_id + 1
        vA = self.vertices[vA_id]
        vA_dist = cumDistances[vA_id]
        vB = self.vertices[vB_id]
        dist_to_reach = vA_dist - epsilon
        vectAB = vB.vectorize(vA)
        vectAB.normalize()
        vectAB.scale(dist_to_reach)
        vNew = vA.addVector(vectAB)
        newEnd = copy.deepcopy(self.vertices[: vA_id + 1]) + [vNew]
        self.vertices += newEnd

    def get_corners(self):
        return list(filter(lambda v: v.type == "corner", self.vertices))

    def reset_vertices_names(self):
        self.vertices = [v.setName("", inplace=True) for v in self.vertices]
        return self

    def get_first_vertex(self):
        if self.vertices:
            return self.vertices[0]
        else:
            raise ValueError("Empty polyline has no vertex")

    def get_last_vertex(self):
        if self.vertices:
            return self.vertices[-1]
        else:
            raise ValueError("Empty polyline has no vertex")

    def is_point(self):
        """
            Returns whether all points of the polyline are located at the same spot
            :return: (bool)
        """
        vertex_a = self.get_first_vertex()
        is_point = True  # Single vertices polyline will not enter the loop
        for idx, vertex_b in enumerate(self.vertices[1:]):
            is_point = vertex_a.is_equal(vertex_b, tolerance=0)
            if not is_point:
                return False
            vertex_a = vertex_b
        return is_point

    def get_corners(self):
        return [v for v in self.vertices if v.type == "corner"]

    def get_corners_names(self):
        return [v.name for v in self.vertices if v.type == "corner"]

    def translatePolyRuleNames(self, translation):
        self.vertices = list(
            map(lambda v: v.translateVertex(translation=translation), self.vertices)
        )

    def filterUnnamedVertices(self):
        self.vertices = list(filter(lambda v: v.name != "", self.vertices))
        return self

    def filterOldVertices(self, rul_code):
        self.vertices = list(
            filter(
                lambda v: str(rul_code) in v.name or v.type == "corner", self.vertices
            )
        )
        return self

    def get_ruled_vertices(self, any=False, rul_code="# "):
        if any:
            return list(filter(lambda v: v.name != "", self.vertices))
        else:
            return list(filter(lambda v: rul_code in v.name, self.vertices))

    def getRuledVerts(
        self, polyType, tolerance=0.5,
    ):
        """
        Get all ruled vertices from a Polyline
        :param shape:
        :param polyType:
        :param tolerance: minimum distance between two ruled vertices
        :return:
        """

        p = copy.deepcopy(self)

        # for closed Polyline drop doubled last vertex
        if len(p.vertices) > 1 and p.vertices[0].is_equal(p.vertices[-1], tolerance):
            p.vertices = p.vertices[:-1]

        p.applyCurveUnity()

        ### Keep only corners
        if polyType in ["cutPolyline", "shapePolyline"]:
            p.vertices = list(filter(lambda v: v.type == "corner", p.vertices))

        return p.vertices

    def unnameAllVertices(self):
        self.vertices = list(
            map(lambda v: v.setName(name="", inplace=True), self.vertices)
        )

    def get_corners_names(self):
        corners = list(filter(lambda v: v.type == "corner", self.vertices))
        return list(map(lambda v: v.name, corners))

    def rerulAllCorners(self, minIdx, rulCode="# "):
        corners = list(filter(lambda v: v.type == "corner", self.vertices))
        nextIdx = minIdx
        for corner in corners:
            nextIdx += 1
            name = rulCode + str(nextIdx)
            corner.setName(name=name)
        return nextIdx

    def deepcopy_polyline(self):
        return Polyline(list(map(lambda v: v.deepcopy_vertex(), self.vertices)))

    def set_vertices_old(self):
        self.vertices = list(map(lambda v: v.set_vertex_old(), self.vertices))
        return self

    def set_vertices_as_original(self):
        self.vertices = list(map(lambda v: v.set_vertex_as_original(), self.vertices))

    def remove_original_vertices(self, keep_corners=False):
        if keep_corners:
            self.vertices = list(
                filter(lambda v: not v.is_original or v.type == "corner", self.vertices)
            )
        else:
            self.vertices = list(filter(lambda v: not v.is_original, self.vertices))
        return self

    def remove_duplicate_following_points(self):
        ids_to_delete = []
        for id_ in range(len(self.vertices) - 1):
            v0, v1 = self.vertices[id_], self.vertices[id_ + 1]
            if v0.is_equal(v1):
                ids_to_delete.append(id_)
        self.vertices = [
            v for idx, v in enumerate(self.vertices) if idx not in ids_to_delete
        ]

    def has_duplicate_points(self):
        has_duplicate = False
        id_ = 0
        while not has_duplicate and id_ < len(self.vertices) - 1:
            has_duplicate = self.vertices[id_].is_equal(self.vertices[id_ + 1])
            id_ += 1
        return has_duplicate

    def get_accu_lengths(self) -> list:
        accu_lengths = [0]
        vA = self.vertices[0]
        for idx, vB in enumerate(self.vertices[1:]):
            accu_lengths.append(accu_lengths[-1] + vA.dist(vB))
            vA = vB
        return accu_lengths

    def get_accu_lengths_opti(self) -> list:
        """
            # TODO Replace accu_list = [0] + list(accu) by insert
        """
        import numpy as np

        accu = np.cumsum(
            [a.dist(b) for a, b in zip(self.vertices[1:], self.vertices[:-1])]
        )
        accu_list = [0] + accu.tolist()
        return accu_list

    def is_in_clockwise_order(self) -> bool:
        """
        Function returns whether polyline vertices are in clockwise order
        :return(bool): True if vertices are in clockwise order, else False
        """
        try:
            vertexA = self.vertices[0]
        except KeyError:
            return
        edges_products = []
        for idx, vertexB in enumerate(self.vertices[1:]):
            edges_products.append((vertexB.x - vertexA.x) * (vertexB.y + vertexA.y))
            vertexA = vertexB
        return sum(edges_products) > 0

    def find_nearest_vertex_idx_in_polyline(self, reference_vertex):
        """
        Function to find nearest vertex from a reference vertex in a given Polyline
        :param self:
        :param reference_vertex:
        :return:
        """
        distances = [vertex.dist(reference_vertex) for vertex in self.vertices]
        try:
            nearest_idx = min(enumerate(distances), key=lambda x: x[1])[0]
        except KeyError("Empty Polyline"):
            return
        return nearest_idx

    def find_nearest_vertex_in_polyline_by_percentage(self, percentage):
        """
        Function to find nearest vertex from a percentage position in a given Polyline
        :param self:
        :param percentage:
        :return:
        """
        position_percentages = self.get_position_percentages()
        position_percentages = [
            math.fabs(position - percentage) for position in position_percentages
        ]
        try:
            nearest_position = min(
                enumerate(position_percentages), key=lambda x: x[1],
            )[0]
        except KeyError("Empty Polyline"):
            return
        return self.vertices[nearest_position]

    def filter_rule_names(self, rule_names):
        self.vertices = [
            vertex for vertex in self.vertices if vertex.name in rule_names
        ]

    def get_first_and_last_vertices_name(self):
        return [self.vertices[0].name, self.vertices[-1].name]

    def get_round_trip_ids(self, threshold_angle: int) -> list([int]):
        """
        Function finding vertices causing the polyline to turn twice in a row, creating a "Z" shape no the polyline
        Example of round trip vertices: [Vertex(0, 0), Vertex(0,1), Vertex(0.2, 0), Vertex(0.2, 1)
        :param threshold_angle: (int) Minimum value of absolute path angles values for the "Z" to be considered a roundtrip
        :return: (list([int]))
        """
        self.describePolyline()
        path_angles = [math.fabs(v.pathAngle - 180) for v in self.vertices]
        first_angle = path_angles[0]
        ids_to_delete = []
        for idx, second_angle in enumerate(path_angles[1:]):
            if first_angle > threshold_angle and second_angle > threshold_angle:
                ids_to_delete.append(idx)
            first_angle = second_angle
        return ids_to_delete

    def remove_round_trips(self, threshold_angle: int):
        """
        Function removing vertices causing the polyline to turn twice in a row, creating a "Z" shape no the polyline
        Example of round trip vertices: [Vertex(0, 0), Vertex(0,1), Vertex(0.2, 0), Vertex(0.2, 1)
        :param threshold_angle: (int) Minimum value of absolute path angles values for the "Z" to be considered a roundtrip
        :return: None
        """
        ids_to_delete = self.get_round_trip_ids(threshold_angle=threshold_angle)
        for idx in ids_to_delete:
            first_name = self.vertices[idx].name
            second_name = self.vertices[idx + 1].name
            if first_name == "":
                self.vertices.pop(idx)
            elif second_name == "":
                self.vertices.pop(idx + 1)
            else:
                raise Exception(
                    f"There is a round trip  on two ruled vertices {first_name} and {second_name}"
                )

    def get_long_round_trips(self, threshold_angle):
        self.describePolyline()
        corners = self.get_corners()
        # If two corners in a row are near from 0 --> delete all points between these corners
        if len(corners) < 2:
            return
        first_corner = corners[0]
        ids_to_delete = []
        for idx, second_corner in enumerate(corners[1:]):
            if first_corner.pathAngle < math.fabs(
                180 - threshold_angle
            ) and second_corner.pathAngle < math.fabs(180 - threshold_angle):
                ids_to_delete.append(idx)
            first_corner = second_corner
        return ids_to_delete

    def remove_long_round_trips(self, threshold_angle):
        ids_to_delete = self.get_long_round_trips(threshold_angle=threshold_angle)
        while ids_to_delete:
            for idx in ids_to_delete:
                self.describePolyline()
                corners = self.get_corners()
                first_corner = corners[idx]
                second_corner = corners[idx + 1]
                first_idx = self.vertices.index(first_corner)
                second_idx = self.vertices.index(second_corner)
                del self.vertices[first_idx:second_idx]
                ids_to_delete = self.get_long_round_trips(
                    threshold_angle=threshold_angle
                )
