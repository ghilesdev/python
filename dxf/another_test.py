import dxfgrabber
import matplotlib.pyplot as plt

dxf = dxfgrabber.readfile("1.dxf")

# an example on how to access the coordinates of a point found by the variable  explorer
# print(dxf.blocks._blocks['0']._entities[0].points[0])

# extracting coords for one shape
# coords = [c for c in dxf.blocks._blocks['22']._entities[0].points]


# extracting the shapes as list
shapes = [shape for shape in dxf.blocks._blocks]

# creating shapes dict from the list above
entities = {k: dxf.blocks._blocks[k] for k in shapes}
# print(entities['0']._entities[0].points)

# dict of all shapes with their coordinates
all_entities = {k: dxf.blocks._blocks[k]._entities[0].points for k in entities}

X = []
Y = []
print(all_entities)
for k, v in all_entities.items():
    print(len(v))
    for i in range(len(v)):
        X.append(v[i][0])
        Y.append(v[i][1])

# x = []
# y = []
# for i, c in enumerate(coords):
#     x.append(c[0])
#     y.append(c[1])

plt.plot(X, Y)
plt.show()
