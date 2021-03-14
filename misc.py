import numpy as np
from numpy.matlib import repmat

boundaries = [(100,75), (2500, 160), (95, 2250), (2560, 2376)]
X = [100, 2500, 95, 2560]
imh, imw = 10, 10

def fxy(x, y):
    # TODO: This currently only works for one square made by calibration coordinates. Extend function
    # so that it concatinates several squares (4?)
    xmat = np.linspace((boundaries[0][0],boundaries[1][0]),(boundaries[2][0],boundaries[3][0]), imw)
    ymat = np.linspace((boundaries[0][1],boundaries[1][1]),(boundaries[2][1],boundaries[3][1]), imh)

    xx = []
    for mat in xmat:
        xx.append(np.linspace(mat[0], mat[1], imw))
    xx = np.array(xx).astype(int)

    yy = []
    for mat in ymat:
        yy.append(np.linspace(mat[0], mat[1], imh))
    yy = np.array(yy).astype(int)

    return xx[x, y], yy[x, y]

print(fxy(5,5))
