import numpy as np
from numpy.matlib import repmat
from matplotlib import pyplot as plt

cal_points =    [(75, 100), (160, 1200), (1125, 95), (1173, 1280),
                (160, 1250), (135, 2500), (1173, 1280), (1203, 2560),
                (1125, 95), (1173, 1280), (2375, 76), (2399, 1199),
                (1173, 1280), (1203, 2560), (2375, 1239), (2501, 2611)]

cal_points =    [(75, 100), (160, 1200), (160, 1250), (1125, 95), (1173, 1280),
                (160, 1250), (135, 2500), (1173, 1280), (1203, 2560),
                (1125, 95), (1173, 1280), (2375, 76), (2399, 1199),
                (1173, 1280), (1203, 2560), (2375, 1239), (2501, 2611)]

X = [100, 2500, 95, 2560]
imh, imw = 12, 12

def fxy(cal_points, imh, imw):

    # TODO: Currently only works with 9 calibration points, or four quadrants.
    # Generalise to as many quadrants as one would like

    quadrants = [cal_points[0], cal_points[1], cal_points[3], cal_points[4],
                 cal_points[1], cal_points[2], cal_points[4], cal_points[5],
                 cal_points[3], cal_points[4], cal_points[6], cal_points[7],
                 cal_points[4], cal_points[5], cal_points[7], cal_points[8]]

    conversion_mat_x = np.zeros((imh, imw))
    conversion_mat_y = np.zeros((imh, imw))

    # Upper left
    upper_left_x = np.linspace((quadrants[0][0],quadrants[1][0]),(quadrants[2][0],quadrants[3][0]), imw//2)
    upper_left_y = np.linspace((quadrants[0][1],quadrants[1][1]),(quadrants[2][1],quadrants[3][1]), imh//2)
    ulx = []
    for mat in upper_left_x:
        ulx.append(np.linspace(mat[0], mat[1], imw//2))
    conversion_mat_x[:imh//2, :imw//2] = np.array(ulx).astype(int)
    uly = []
    for mat in upper_left_y:
        uly.append(np.linspace(mat[0], mat[1], imh//2))
    conversion_mat_y[:imh//2, :imw//2] = np.array(uly).astype(int)

    # Upper right
    upper_right_x = np.linspace((quadrants[4][0],quadrants[5][0]),(quadrants[6][0],quadrants[7][0]), imw//2)
    upper_right_y = np.linspace((quadrants[4][1],quadrants[5][1]),(quadrants[6][1],quadrants[7][1]), imh//2)
    ulx = []
    for mat in upper_right_x:
        ulx.append(np.linspace(mat[0], mat[1], imw//2+1))
    conversion_mat_x[:imh//2, imw//2-1:imw] = np.array(ulx).astype(int)
    uly = []
    for mat in upper_right_y:
        uly.append(np.linspace(mat[0], mat[1], imh//2+1))
    conversion_mat_y[:imh//2, imw//2-1:imw] = np.array(uly).astype(int)

    # Lower left
    lower_left_x = np.linspace((quadrants[8][0],quadrants[9][0]),(quadrants[10][0],quadrants[11][0]), imw//2+1)
    lower_left_y = np.linspace((quadrants[8][1],quadrants[9][1]),(quadrants[10][1],quadrants[11][1]), imh//2+1)
    llx = []
    for mat in lower_left_x:
        llx.append(np.linspace(mat[0], mat[1], imw//2))
    conversion_mat_x[(imh-1)//2:imh, :imw//2] = np.array(llx).astype(int)
    lly = []
    for mat in lower_left_y:
        lly.append(np.linspace(mat[0], mat[1], imh//2))
    conversion_mat_y[(imh-1)//2:imh, :imw//2] = np.array(lly).astype(int)

    # Lower right
    lower_right_x = np.linspace((quadrants[12][0],quadrants[13][0]),(quadrants[14][0],quadrants[15][0]), imw//2+1)
    lower_right_y = np.linspace((quadrants[12][1],quadrants[13][1]),(quadrants[14][1],quadrants[15][1]), imh//2+1)
    lrx = []
    for mat in lower_right_x:
        lrx.append(np.linspace(mat[0], mat[1], imw//2+1))
    conversion_mat_x[(imh-1)//2:imh, imw//2-1:imw] = np.array(lrx).astype(int)
    lry = []
    for mat in lower_right_y:
        lry.append(np.linspace(mat[0], mat[1], imh//2+1))
    conversion_mat_y[(imh-1)//2:imh, imw//2-1:imw] = np.array(lry).astype(int)

    return np.stack([conversion_mat_x, conversion_mat_y])


mat = fxy(1, 1, cal_points)
print(mat[:,7:,7:])
#print(mat[:])
