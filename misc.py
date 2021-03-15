import numpy as np
from numpy.matlib import repmat
from matplotlib import pyplot as plt

#  1  2  3  4
#  5  6  7  8
#  9 10 11 12
# 13 14 15 16

cal_points =    [(100, 75), (1250, 160), (95, 1125), (1280, 1173),
                (1250, 160), (2500, 135), (1280, 1173), (2560, 1203),
                (95, 1125), (1280, 1173), (76, 2375), (1199, 2399),
                (1280, 1173), (2560, 1203), (1239, 2375), (2611, 2501)]

"""
for i, p in enumerate(cal_points):
    plt.plot(p[0], p[1], '*',label=f'{[i+1]}')
    plt.legend(loc="upper left")
plt.show()
"""

X = [100, 2500, 95, 2560]
imh, imw = 6, 6

def fxy(x, y, boundaries, return_mat=False):
    # TODO: This currently only works for one square made by calibration coordinates. Extend function
    # so that it concatinates several squares (4?)

    conversion_mat_x = np.zeros((imh, imw))
    conversion_mat_y = np.zeros((imh, imw))

    # Upper left
    upper_left_x = np.linspace((boundaries[0][0],boundaries[1][0]),(boundaries[2][0],boundaries[3][0]), imw//2)
    upper_left_y = np.linspace((boundaries[0][1],boundaries[1][1]),(boundaries[2][1],boundaries[3][1]), imh//2)
    ulx = []
    for mat in upper_left_x:
        ulx.append(np.linspace(mat[0], mat[1], imw//2))
    conversion_mat_x[:imh//2, :imw//2] = np.array(ulx).astype(int)
    uly = []
    for mat in upper_left_y:
        uly.append(np.linspace(mat[0], mat[1], imh//2))
    conversion_mat_y[:imh//2, :imw//2] = np.array(uly).astype(int)

    # Upper right
    upper_right_x = np.linspace((boundaries[4][0],boundaries[5][0]),(boundaries[6][0],boundaries[7][0]), imw//2)
    upper_right_y = np.linspace((boundaries[4][1],boundaries[5][1]),(boundaries[6][1],boundaries[7][1]), imh//2)
    ulx = []
    for mat in upper_right_x:
        ulx.append(np.linspace(mat[0], mat[1], imw//2+1))
    conversion_mat_x[:imh//2, imw//2-1:imw] = np.array(ulx).astype(int)
    uly = []
    for mat in upper_right_y:
        uly.append(np.linspace(mat[0], mat[1], imh//2+1))
    conversion_mat_y[:imh//2, imw//2-1:imw] = np.array(uly).astype(int)

    # Lower left
    lower_left_x = np.linspace((boundaries[8][0],boundaries[9][0]),(boundaries[10][0],boundaries[11][0]), imw//2)
    lower_left_y = np.linspace((boundaries[8][1],boundaries[9][1]),(boundaries[10][1],boundaries[11][1]), imh//2)
    llx = []
    for mat in lower_left_x:
        llx.append(np.linspace(mat[0], mat[1], imw//2))
    conversion_mat_x[imh//2:imh, :imw//2] = np.array(llx).astype(int)
    lly = []
    for mat in lower_left_y:
        lly.append(np.linspace(mat[0], mat[1], imh//2))
    conversion_mat_y[imh//2:imh, :imw//2] = np.array(lly).astype(int)

    # Lower right
    lower_right_x = np.linspace((boundaries[12][0],boundaries[13][0]),(boundaries[14][0],boundaries[15][0]), imw//2)
    lower_right_y = np.linspace((boundaries[12][1],boundaries[13][1]),(boundaries[14][1],boundaries[15][1]), imh//2)
    lrx = []
    for mat in lower_right_x:
        lrx.append(np.linspace(mat[0], mat[1], imw//2+1))
    conversion_mat_x[imh//2:imh, imw//2-1:imw] = np.array(lrx).astype(int)
    lry = []
    for mat in lower_right_y:
        lry.append(np.linspace(mat[0], mat[1], imh//2+1))
    conversion_mat_y[imh//2:imh, imw//2-1:imw] = np.array(lry).astype(int)


    return np.stack([conversion_mat_x, conversion_mat_y])


mat = fxy(1, 1, cal_points)
#print(mat[:,5,5])
print(mat[:])
