#!/usr/bin/env python3

import sys

X, Y, Z = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
print("Source  Nodes X: " + str(X))
print("Transit Nodes Y: " + str(Y))
print("Dest    Nodes Z: " + str(Z))

dvolumes = []
# Source nodes Si
for i in range(0, X+1):
    dvolumes.append([])
    # Destination nodes Dj
    for j in range(0, Z+1):
        # Demand volumes Hij = i + j
        dvolumes[i].append(i + j)

def printdv(volumes):
    for row in volumes:
        print(row)


printdv(dvolumes)


