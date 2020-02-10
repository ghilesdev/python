import ezdxf
import pyclipper

from .shape import Shape
from .polyline import Polyline
from .vertex import Vertex
from .Notch import Notch


def mergePolylinesFragments(polylist):
    merged = 1
    l = len(polylist)

    vertices = []
    vertices.extend(polylist[0])
    polylist.pop(0)

    while merged < l:
        for p in polylist:
            if vertices[0].is_equal(p[0]):
                polylist.remove(p)
                p = p[::-1]
                tmp = vertices
                vertices = p
                vertices.extend(tmp)
                merged += 1
                break
            if vertices[0].is_equal(p[-1]):
                tmp = vertices
                vertices = p
                vertices.extend(tmp)
                polylist.remove(p)
                merged += 1
                break
            if vertices[-1].is_equal(p[0]):
                vertices.extend(p)
                polylist.remove(p)
                merged += 1
                break
            if vertices[-1].is_equal(p[-1]):
                polylist.remove(p)
                p = p[::-1]
                vertices.extend(p)
                merged += 1
                break
    return vertices


def isNotchValid(newVertex, notches):
    for notch in notches:
        if notch.is_equal(newVertex):
            return False
    return True


def addVertexToLayer(layer, v):
    layer.addVertex(v)


def assignRulToShape(polyline, vertex):
    for v in polyline.vertices:
        if v.is_equal(vertex, 0.1):
            v.name = vertex.name


def convert2Vertex(v):
    if type(v) is Vertex:
        v = (v.x, v.y)
    newCoord = [float("%.3f" % (x)) for x in v]
    if len(newCoord) == 2:
        newCoord.append("")  # append empty RUL if no coord z
    else:
        newCoord[2] = ""  # erase coord z and put RUL instead of it
    return Vertex(newCoord[0], newCoord[1], newCoord[2])


def parse(f):
    dxf = ezdxf.readfile(f)
    mds = dxf.blocks
    listShapes = []

    for e in mds.__iter__():
        s = Shape()
        dicLayerPolyline = {1: s.cutPolyline, 14: s.shapePolyline}
        polylineFragments = []
        noDuplicates = []
        s.fileName = e.name

        for ez in e.__iter__():
            """
                This will ignore layer which are not a number
                TODO: change it later when we need a better dxf parser
            """
            try:
                layer = int(ez.get_dxf_attrib("layer"))
            except:
                continue

            if ez.dxftype() == "POLYLINE":
                vertList = list(ez.points())
                p = Polyline()
                p.listToPolyline(vertList)
                if pyclipper.Area(p.polylineToTuple()) < 0:
                    vertList = vertList[::-1]
                if ez.is_closed:  # closing polyline if the attribute is_closed is true
                    vertList.append(vertList[0])
                if layer == 8:  # if layer is non permanant marking
                    s.dicMarkings[8].append(Polyline())
                    dicLayerPolyline[8] = s.dicMarkings[8][-1]
                if (
                    layer in dicLayerPolyline
                    and len(dicLayerPolyline[layer].vertices) > 2
                ):
                    polylineFragments.append(vertList)
                else:
                    if (
                        layer not in dicLayerPolyline
                    ):  # if layer is not in a specific layer of shape (unusedLayer)
                        pUnused = Polyline()
                        if layer not in s.unusedLayer:
                            s.unusedLayer[layer] = [pUnused]
                    for idx, v in enumerate(vertList):
                        if v == vertList[idx - 1] and idx != 0:  # skip duplicate vertex
                            continue
                        if layer in dicLayerPolyline:
                            addVertexToLayer(dicLayerPolyline[layer], convert2Vertex(v))
                        else:  # add to unused layer
                            addVertexToLayer(pUnused, convert2Vertex(v))
            elif ez.dxftype() == "POINT":
                if layer == 13:  # adding marking points which are in layer 13
                    s.dicMarkings[13].append(Polyline())
                    dicLayerPolyline[13] = s.dicMarkings[13][-1]
                    addVertexToLayer(
                        dicLayerPolyline[13], convert2Vertex(ez.dxf.location)
                    )
                    addVertexToLayer(
                        dicLayerPolyline[13], convert2Vertex(ez.dxf.location)
                    )  # need to add it twice to have the points in the polyline

            elif (
                ez.dxftype() == "TEXT"
                and layer != 19
                and ez.get_dxf_attrib("text")[0] == "#"
            ):
                coord = ez.get_dxf_attrib("insert")
                tag = ez.get_dxf_attrib("text")
                newTextVertex = Vertex(coord[0], coord[1], tag)
                duplicate = False  # avoid duplicate vertex
                for v in noDuplicates:
                    if (
                        newTextVertex.is_equal(v)
                        and newTextVertex.name == v.name
                        and layer not in [4, 80, 81, 82, 83]
                    ):  # if duplicate point in notch don't set it to duplicate
                        duplicate = True
                        continue

                for mark in s.dicMarkings[8] + s.dicMarkings[13]:
                    for v in mark.vertices:
                        if newTextVertex.is_equal(v):
                            v.name = newTextVertex.name

                if (
                    duplicate
                ):  # If vertex is a duplicate, do not append to notches or textMarkings
                    continue

                if int(layer) in [4, 80, 81, 82, 83] and isNotchValid(
                    newTextVertex, s.notches
                ):
                    s.notches.append(
                        Notch(
                            _x=newTextVertex.x,
                            _y=newTextVertex.y,
                            _name=newTextVertex.name,
                        )
                    )
                else:
                    s.textMarkings.append(newTextVertex)
                noDuplicates.append(newTextVertex)

            elif ez.dxftype() == "LINE" and layer == 7:
                v1 = Vertex(ez.dxf.start[0], ez.dxf.start[1])
                v2 = Vertex(ez.dxf.end[0], ez.dxf.end[1])
                s.grainPolyline.vertices = [v1, v2]

        if polylineFragments:
            frags = []
            for p in polylineFragments:
                poly = []
                for v in p:
                    poly.append(convert2Vertex(v))
                frags.append(poly)
            frags.insert(0, s.cutPolyline.vertices)
            s.cutPolyline.vertices = mergePolylinesFragments(frags)

        # Assign rules to polylines in each layer:
        for layer in s.allPolyLayers:
            content = eval("s." + layer)
            if type(content) == type([]):
                for p in content:
                    for tag in s.textMarkings:
                        assignRulToShape(p, tag)
            else:
                for tag in s.textMarkings:
                    assignRulToShape(content, tag)

        for layer in list(s.dicMarkings.keys()):
            s.markings.extend(s.dicMarkings[layer])

        if (
            len(s.cutPolyline.vertices) or s.markings
        ):  # adding to the listShapes only if the shape has vertices
            listShapes.append(s)

    return listShapes


if __name__ == '__main__':
    dxf = ezdxf.readfile('1.dxf')
    shapes = parse(dxf)