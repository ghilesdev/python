import os
import ezdxf
import copy
import uuid
import math
from tekyntools.geometryObjects.polyline import Polyline
from tekyntools.geometryObjects.vertex import Vertex
from tekyntools.sizing.getSize import GetSize

from tekyntools.sizing.sizeModifier import sizeModifier
from tekyntools.shapeModifier.createSizeMarks import markSize

ABS = 0
ORD = 1
RUL = 2

# LAYERS IN SHAPES OBJECTS:
# 1    Shape polyline      (only polylines)
# 2    Cut polyline        (only polylines)
# 3    Shape islands       (only polylines)
# 4    Cut islands         (only polylines)
# 5    Markings            (polylines and vertex)
# 6    Text Markings       (only vertex)
# 7    Notches                (ony vertex)
# 8    GrainPolyline        (only polylines)
# 9    NonPermanantMarking  (only polylines)


class Shape(object):
    def __init__(self, filePath=""):
        self.filePath = filePath  # shape file name is "shapeID.dxf"
        self.fileName = os.path.basename(filePath)  # file name of the shape
        self.shapePolyline = (
            Polyline()
        )  # table containing the shape polyline vertex (LAYER 1)
        self.cutPolyline = (
            Polyline()
        )  # table containing the cut polyline vertex (LAYER 2)
        self.grainPolyline = (
            Polyline()
        )  # table containing the fabric direction polyline vertex (LAYER 7)
        self.islandsShapes = (
            []
        )  # table of island shapes polylines (several polylines) (LAYER 3)
        self.islandsCuts = (
            []
        )  # table of island cuts polylines (several polylines) (LAYER 4)
        self.dicMarkings = {5: [], 8: [], 13: []}
        self.markings = (
            []
        )  # table of text block markings (x, y, value) (LAYER 5) geometry à marquer
        self.nonPermanantMarkings = []
        self.markingsPoly = Polyline()
        self.markingsLengthDict = dict()
        self.sizeMarks = (
            []
        )  # list of vertice names (with direction) where there is size_marks
        self.allPolyLayers = [
            "shapePolyline",
            "cutPolyline",
            "islandsShapes",
            "islandsCuts",
            "markings",
            "grainPolyline",
            "nonPermanantMarkings",
        ]  # list containing all polyline types in a shape object, used for cycling the entire shape
        self.allVertexLayers = ["notches", "sizeMarks"]
        self.unusedLayer = {}

        self.islandsCount = 0  # number of islands
        self.textMarkings = []
        self.sizePoints = []  # TODO: what is that? difference with sizeMarks?

        self.symmetry = ""  # whether the shape is symmetric (1 shape) (SYM), mirror (2 shapes) (MIR), both (BOT) or plain ('')
        self.symAxis = ""  # symmertry axis
        self.d = 0  # distance of symetry axis to origin

        self.size = ""  # size of the shape. If empty, do not size the shape

        self.rotAngle = 0  # rotation angle
        self.rotCenter = Vertex(0, 0)  # rotation center
        self.frame = [
            0,
            0,
            0,
            0,
        ]  # table containing for the the rectangular frame in which the polylines block is included
        self.width = 0
        self.height = 0
        self.notches = (
            []
        )  # List of tuples of the notches with the vertex and the notch type
        self.notchesPoly = Polyline()

        self.isClosed = (
            True  # True -> is a closed polylines ; False -> is a open polylines
        )
        self.articleID = -1  # identifiant
        self.idShapeDb = -1
        self.uniqueID = -1

        self.uniqueIDHex = uuid.uuid4().hex  # Used in AHF

        self.number = 1  # Shape multiplier

        self.fusing = (
            0  # Enum to specify if the shape needs to be fused and its technique number
        )
        self.fabric = "Default fabric"  # Fabric category

        self.isConcat = False  # Whether the shape is a concatVerts candidate
        self.concatVerts = {
            "entry1": None,
            "entry2": None,
            "exit1": None,
            "exit2": None,
        }  # Dict containing Vertices on cutPolyline, used for concatVerts
        self.authAngles = []
        self.plcUniqueId = None
        self.ghost_notches = {}

    def __str__(self):
        out = "Shape Info:\n"
        out += "\tSymmetry property: " + self.symmetry + "\n"
        out += (
            "\tShape frame:\n\t\tLower left: ("
            + str(self.frame[0])
            + ","
            + str(self.frame[1])
            + ")\n\t\tUpper right: ("
            + str(self.frame[2])
            + ","
            + str(self.frame[3])
            + ")\n"
        )
        out += "\tNumber of islands: " + str(self.islandsCount) + "\n"
        out += "Shape outline (layer 1):\n"
        for coord in self.shapePolyline.vertices:
            out += (
                "\tx: "
                + str(coord.x)
                + " y: "
                + str(coord.y)
                + " rule: "
                + str(coord.name)
                + "\n"
            )
        out += "Shape cut line (layer 2):\n"
        for coord in self.cutPolyline.vertices:
            out += (
                "\tx: "
                + str(coord.x)
                + " y: "
                + str(coord.y)
                + " rule: "
                + str(coord.name)
                + "\n"
            )
        out += "Island shapes outlines (layer 3):\n"
        i = 0
        out += "Notches: \n "
        # for coord in self.notches.vertices:
        #     out += "\tx: " + str(coord.x) + " y: " + str(coord.y) + " rule: " + str(coord.name) + "\n"
        if self.islandsShapes != []:
            while i < self.islandsCount:
                out += "Island shape " + str(i + 1) + ":\n"
                for coord in self.islandsShapes[i]:
                    out += (
                        "\tx: "
                        + str(coord[ABS])
                        + " y: "
                        + str(coord[ORD])
                        + " rule: "
                        + str(coord[RUL])
                        + "\n"
                    )
                i += 1
        out += "Island shapes cut lines (layer 4):\n"
        i = 0
        if self.islandsCuts != []:
            while i < self.islandsCount:
                out += "Island shape " + str(i + 1) + ":\n"
                for coord in self.islandsCuts[i]:
                    out += (
                        "\tx: "
                        + str(coord[ABS])
                        + " y: "
                        + str(coord[ORD])
                        + " rule: "
                        + str(coord[RUL])
                        + "\n"
                    )
                i += 1
        out += "Markings (layer 5):\n"
        for p in self.markings:
            out += "new poly\n"
            for coord in p.vertices:
                out += (
                    "\tx: "
                    + str(coord.x)
                    + " y: "
                    + str(coord.y)
                    + " text: "
                    + str(coord.name)
                    + "\n"
                )
        return out

    def setShapeStart(self):
        self.shapeStart = self.cutPolyline.getBounds()["bottom"]

    def setShapeEnd(self):
        self.shapeEnd = self.cutPolyline.getBounds()["top"]

    def setAuthorizedAngle(self, step):
        if step == 0:
            step = 360
        self.authAngles = list(range(0, 360, int(step)))

    def isEqual(
        self, s
    ):  # Check whether the shapes are the same (same size, same shape)
        return self.size == s.size and self.idShapeDb == s.idShapeDb

    def area(self):
        return abs(self.cutPolyline.area())

    def symmetrize(
        self,
    ):  # if 'HALF', shape is the half of a symetrical piece, if 'SYME'
        if (
            self.symmetry == "SYM" or self.symmetry == "MIR"
        ):  # sym axis has no influence here, can be both
            self.symmetrizeAllAttr()
            self.rotAngle = (self.rotAngle + 180) % 360

    def offset(self, dx=0, dy=0):
        self.applyFunctionToAllVertices(lambda v: v.offsetVertex(dx, dy))

    def applyFunctionToAllPoly(self, f, grain=False):  # Apply function to all polylines
        for layer in self.allPolyLayers:
            content = eval("self." + layer)
            if type(content) == list:
                for polyline in content:
                    f(polyline)
            else:
                if (layer != "grainPolyline") or (layer == "grainPolyline" and grain):
                    f(content)

    def applyFunctionToAllVertices(self, f):  # Apply function to all vertices
        layers = self.allPolyLayers
        # for layer in self.allPolyLayers:
        for layer in layers:
            content = eval("self." + layer)
            if type(content) == list:
                for polyline in content:
                    if len(polyline.vertices) != 0:
                        for v in polyline.vertices:
                            f(v)
            else:
                if len(content.vertices) != 0:
                    for v in content.vertices:
                        f(v)
        for v in self.sizePoints:
            f(v)
        for v in self.notches:
            f(v)
        for v in self.concatVerts:
            if self.concatVerts[v]:
                f(self.concatVerts[v])

    def scaleXY(self, xScale, yScale):
        for layer in self.allPolyLayers:
            content = eval("self." + layer)
            if type(content) == type([]):
                for polyline in content:
                    if len(polyline.vertices) != 0:
                        polyline.scaleXY(xScale, yScale)
            else:
                if len(content.vertices) != 0:
                    content.scaleXY(xScale, yScale)

    def symmetrizeAllAttr(self):
        symParams = self.getSymParams()
        for layer in self.allPolyLayers:
            content = eval("self." + layer)
            if type(content) == type([]):
                for polyline in content:
                    if len(polyline.vertices) != 0:
                        polyline.symmetrize(symParams)
            else:
                if len(content.vertices) != 0:
                    content.symmetrize(symParams)

        for v in self.sizePoints:
            v.symmetrize(symParams)
        for v in self.notches:
            v.symmetrize(symParams)
        for sizeM in self.sizeMarks:
            v = Vertex(sizeM["coords"][0], sizeM["coords"][1])
            v.symmetrize(symParams)
            sizeM["coords"] = (v.x, v.y)

    def mergeShapes(
        self, shape
    ):  #    merges two shapes with exactly the same structure
        for layer in self.allPolyLayers:
            content1 = eval("self." + layer)
            content2 = eval("shape." + layer)
            if type(content1) == type([]):
                for i, polyline in enumerate(content1):
                    if len(polyline.vertices) != 0:
                        content1[i].mergePolylines(content2[i])
            else:
                if len(content1.vertices) != 0:
                    content1.mergePolylines(content2)

    def getSymParams(self):
        symParams = self.cutPolyline.getSymParams()
        self.symAxis = symParams[0]  # symmertry axis
        self.d = symParams[1]  # distance of symetry axis to origin
        return symParams

    def translateShape(self, vector):
        self.applyFunctionToAllVertices(lambda p: p.addVector(vector, inplace=True))

    def rotateShape(self, angle=None, center=Vertex(0, 0), grain=False):
        if angle is None:
            angle = self.rotAngle
        if angle % 360 == 0:
            return
        self.applyFunctionToAllPoly(
            lambda p: p.rotatePolyline(angle, center), grain=True
        )

        for v in self.sizePoints:
            v.rotateVertex(angle, center)
        for v in self.notches:
            v.rotateVertex(angle, center)
        for v in self.concatVerts:
            if self.concatVerts[v]:
                self.concatVerts[v].rotateVertex(angle, center)

    def checkConcat(self):  # check whether concatVerts vertices are defined
        if (
            self.concatVerts["entry1"]
            and self.concatVerts["entry2"]
            and self.concatVerts["exit1"]
            and self.concatVerts["exit2"]
        ):
            self.isConcat = True
        else:
            self.isConcat = False
        return self.isConcat

    def setConcat(self):
        self.checkConcat()
        return self

    def concatenateShapes(self, shapeToConcat, count, tolerance=0.1):
        # define translation vector and rotation angle
        vector = self.concatVerts["exit1"].vectorize(
            shapeToConcat.concatVerts["entry1"]
        )  # translation vector
        vector = Vertex(0, -600 * (count + 1))
        v1 = self.concatVerts["exit2"].vectorize(self.concatVerts["exit1"])
        v2 = shapeToConcat.concatVerts["entry2"].vectorize(
            shapeToConcat.concatVerts["entry1"]
        )
        angle = v2.angleToVector(v1)  # (v1, v2) angle
        self.concatVerts["entry1"]

        # Place shapeToConcat next to self
        shapeToConcat.translateShape(vector)
        shapeToConcat.rotateShape(-angle, self.concatVerts["exit1"])

        # Merge all layers of both shapes
        shapeConcatenated = copy.deepcopy(self)
        for layer in self.allPolyLayers + self.allVertexLayers:
            layer1 = eval("shapeConcatenated." + layer)
            layer2 = eval("shapeToConcat." + layer)
            if type(layer1) == list:
                layer1 += layer2

        # Merge cutPolylines
        p1 = shapeConcatenated.cutPolyline
        p2 = shapeToConcat.cutPolyline

        p1List, p2List = p1.overlap(
            p2, rip="both"
        )  # remove overlap from both cutPolylines

        if len(p1List) == 1 and len(p2List) == 1:
            p1 = p1List[0]
            p2 = p2List[0]
            if p1.vertices[-1].is_equal(p2.vertices[0]):
                p1.vertices += p2.vertices[1:]
            else:
                p1.vertices += p2.vertices[1::-1]
            shapeConcatenated.cutPolyline = p1

            # Reassign entry concatVerts on the new concatenated shape
            shapeConcatenated.concatVerts["exit1"] = shapeToConcat.concatVerts["exit1"]
            shapeConcatenated.concatVerts["exit2"] = shapeToConcat.concatVerts["exit2"]

        else:
            print("Warning: concatenation did not work ! ")
            # exit()
            return shapeToConcat

        return shapeConcatenated

    def getShapeRuleNames(self, ruleNamesList, name=""):
        for polyName in self.allPolyLayers:
            content = eval("self." + polyName)
            if type(content) == type(Polyline()):
                ruleNamesList += content.getPolyRuleNames(name=name)
            elif type(content) == type([]):
                for poly in content:
                    ruleNamesList += poly.getPolyRuleNames(name=name)
            else:
                print(
                    "Error: layer is neither a list nor a Polyline. What kind of layer is that?"
                )
        return ruleNamesList

    def forceClose(self, epsilon):
        self.cutPolyline.forceClose(epsilon=epsilon)

    def getShapeRuleVertices(self, rules):
        ruleNamesDict = {}
        for polyName in self.allPolyLayers:
            content = eval("self." + polyName)
            if type(content) == type(Polyline()):
                ruleNamesList = [
                    name for name in content.getPolyRuleNames() if name is not ""
                ]
                for ruleName in ruleNamesList:
                    if ruleName.replace("#", "DELTA") != "DELTA -1":
                        ruleNamesDict[ruleName] = rules[ruleName.replace("#", "DELTA")]
            elif type(content) == type([]):
                for poly in content:
                    ruleNamesList = [
                        name for name in poly.getPolyRuleNames() if name is not ""
                    ]
                    for ruleName in ruleNamesList:
                        if ruleName.replace("#", "DELTA") != "DELTA -1":
                            ruleNamesDict[ruleName] = rules[
                                ruleName.replace("#", "DELTA")
                            ]
        ruleNameNotches = [n.name for n in self.notches]
        for ruleName in ruleNameNotches:
            ruleNamesDict[ruleName] = rules[ruleName.replace("#", "DELTA")]
        return ruleNamesDict

    def transform_point_markings_to_segment(self):
        """
            Replace point markings by segment markings
            parameters:
                self (Shape): shape whose point markings have to be replaced by segment markings
            return:
                self (Shape) with segment markings instead of point markings
        """
        new_markings = []
        for poly_marking in self.markings:
            if len(poly_marking.vertices) == 1:
                point_marking = poly_marking.vertices[0]
                new_markings.append(point_marking.transform_into_segment())
            else:
                raise Exception("More than one marking in this polyline")
        self.markings = new_markings
        return self

    def get_frame_area(self):
        bounds = self.cutPolyline.getBounds()
        frame_area = math.fabs(bounds["top"] - bounds["bottom"]) * math.fabs(
            bounds["right"] - bounds["left"]
        )
        return frame_area

    def reset_layers_content(self, layers_names=[]):
        """
            Empty specified layers polylines
            parameters:
                layers_names: names of the layers which content should be reset
        """
        for layer_name in layers_names:
            content = eval("self." + layer_name)
            if isinstance(content, Polyline):
                setattr(self, layer_name, Polyline())
            elif isinstance(content, list):
                nb_polylines = len(content)
                empty_polys_list = []
                for i in range(nb_polylines):
                    empty_polys_list.append(Polyline())
                setattr(self, layer_name, empty_polys_list)

    def get_frame_dimensions(self):
        """
        Return the horizontal and vertical lengths of a the shape
        :param self:
        :return: two positive float: horizontal length and vertical length
        """
        bounds = self.cutPolyline.getBounds()
        horizontal_length = math.fabs(bounds["left"] - bounds["right"])
        vertical_length = math.fabs(bounds["top"] - bounds["bottom"])
        return horizontal_length, vertical_length

    def is_vertical(self):
        """
            Must be applied to a shape with angle in [0, 90, 180, 270]
            :param self:
            :return:
        """
        horizontal_length, vertical_length = self.get_frame_dimensions()
        return horizontal_length <= vertical_length

    def create_shape_markings(self):
        """
            Create markings for shape as specified in marking type filled (marking.type)
            parameters:
                shape (Shape):
            TODO Marking type should be a polyline field --> different types of marking for a shape
        """
        from tekyntools.shapeModifier.shapesPreprocessing import (
            get_markings_type_and_value,
        )
        from tekyntools.shapeModifier.markings_point_to_cross import create_L_markings
        from tekyntools.shapeModifier.markings_point_to_circle import (
            createCircleMarkings,
        )

        marking_type, value = get_markings_type_and_value(self)
        if marking_type is not None and value is not None:
            if marking_type == "CIRCLE":
                createCircleMarkings(self, radius=value)
            elif marking_type == "L":
                if self.check_polylines_are_points(["markings"]):
                    create_L_markings(self)

    def reset_all_vertices_names(self, layers_names):
        """
             Reset names of all vertices in polyline
            :param layers_names: Filter by polyline names
        """
        for layer in layers_names:
            content = eval("self." + layer)
            if isinstance(content, list):
                for polyline in content:
                    polyline.reset_vertices_names()
            else:
                content.reset_vertices_names()

    def check_polylines_are_points(self, layers_names):
        """
        TODO Test
        :param layers_names:
        :return:
        """
        for layer in layers_names:
            content = eval("self." + layer)
            if isinstance(content, list):
                nb_polylines = len(content)
                if nb_polylines == 0:
                    raise ValueError("Empty list")
                polys_are_points = True
                idx = 0
                while polys_are_points and idx < nb_polylines:
                    polys_are_points = content[idx].is_point()
                    idx += 1
                return polys_are_points
            else:
                return content.is_point()

    def translateShapeRuleNames(self, translation):
        for polyName in self.allPolyLayers:
            content = eval("self." + polyName)
            if type(content) == type(Polyline()):
                content.translatePolyRuleNames(translation=translation)
            elif type(content) == type([]):
                for poly in content:
                    poly.translatePolyRuleNames(translation=translation)
            else:
                print(
                    "Error: layer is neither a list nor a Polyline. What kind of layer is that?"
                )

    def getAllPolylines(self, filter=None):
        """
        Function to get all polylines of a given shape
        filter: list(str)
        return: {layerName: content} where layerName (str) and content (Polyline or list(Poyline))
        """
        allPolylinesDict = {}
        polylines_of_interest = self.allPolyLayers if filter is None else filter
        for polyName in polylines_of_interest:
            content = eval("self." + polyName)
            if type(content) == type(Polyline()):
                allPolylinesDict[polyName] = content
            elif type(content) == type([]):
                for poly in content:
                    allPolylinesDict[polyName] = poly
            else:
                print(
                    "Error: layer is neither a list nor a Polyline. What kind of layer is that?"
                )
        return allPolylinesDict

    def remove_duplicate_following_points(self):
        self.cutPolyline.remove_duplicate_following_points()
        self.shapePolyline.remove_duplicate_following_points()
