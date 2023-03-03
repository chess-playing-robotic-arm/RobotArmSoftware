import math
import numpy as np
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from statistics import mean
import cv2 as cv

from CoordinateSystemTools import CoordinateSystemTools


def h_v_lines(lines):
    x_dim = lines.shape[0]
    h_lines, v_lines = [], []
    lines = lines.reshape(x_dim, 2)

    for rho, theta in lines:
        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
            v_lines.append([rho, theta])
        else:
            h_lines.append([rho, theta])
    return h_lines, v_lines


# Find the intersections of the lines
def line_intersections(h_lines, v_lines):
    points = []
    for r_h, t_h in h_lines:
        for r_v, t_v in v_lines:
            a = np.array([[np.cos(t_h), np.sin(t_h)],
                         [np.cos(t_v), np.sin(t_v)]])
            b = np.array([r_h, r_v])
            inter_point = np.linalg.solve(a, b)
            points.append(inter_point)
    return np.array(points)


# Hierarchical cluster (by euclidean distance) intersection points
def cluster_points(points):
    dists = spatial.distance.pdist(points)
    single_linkage = cluster.hierarchy.single(dists)
    flat_clusters = cluster.hierarchy.fcluster(single_linkage, 10, 'distance')
    cluster_dict = defaultdict(list)
    for i in range(len(flat_clusters)):
        cluster_dict[flat_clusters[i]].append(points[i])
    cluster_values = cluster_dict.values()
    clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(
        np.array(arr)[:, 1])), cluster_values)
    return sorted(list(clusters), key=lambda k: [k[1], k[0]])

# TODO:remove if replacment is found


def augment_points(points):
    points_shape = list(np.shape(points))
    # print('shape : ' + str(points_shape))
    augmented_points = []
    for row in range(int(points_shape[0] / 11)):
        start = row * 9
        end = (row * 9) + 8
        rw_points = points[start:end + 1]
        rw_y = []
        rw_x = []
        for point in rw_points:
            x, y = point
            rw_y.append(y)
            rw_x.append(x)
        y_mean = mean(rw_y)
        for i in range(len(rw_x)):
            point = (rw_x[i], y_mean)
            augmented_points.append(point)
    augmented_points = sorted(augmented_points, key=lambda k: [k[1], k[0]])
    return augmented_points


def boardPoints(points):
    points_shape = list(np.shape(points))
    p_x = []
    p_y = []
    diff_y = []
    y_prev = points[0][1]
    for point in points:
        x, y = point
        p_x.append(x)
        p_y.append(y)
        diff = y_prev - y
        diff_y.append(diff)
        y_prev = y

    return diff_y

# TODO: remove or use after the drawExtractedSquare


def deleteExtraPoints(points, diff_y):
    peaks_postions = []
    current_peak = abs(diff_y[0])
    for i in range(len(diff_y)):
        if abs(diff_y[i]) > (current_peak + 10):
            peaks_postions.append(i)
            current_peak = abs(diff_y[0])

    print(peaks_postions)


def drawLines(img, lines):
    if lines is not None:
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)


def drawLinesP(img, lines):
    for points in lines:
        x1, y1, x2, y2 = points[0]
        cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)


def drawPoints(img, points, color = (0,255,255)):
    for point in points:
        print('trying to draw : ' + str(point))
        x = np.array(point)
        x = x.astype(int)
        point = tuple(x)
        cv.circle(img, point, 1, color, 2)


def drawOrderedPoints(img, points):
    for rows in points:
        for point in rows:
            x = np.array(point)
            x = x.astype(int)
            point = tuple(x)
            cv.circle(img, point, 1, (0, 0, 255), 2)


def detectRedCorners(img):
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])
    
    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255])
    
    lower_mask = cv.inRange(hsv, lower1, upper1)
    upper_mask = cv.inRange(hsv, lower2, upper2)
    
    full_mask = lower_mask + upper_mask;
    coord = cv.findNonZero(full_mask)
    
    coord = np.reshape(coord,(coord.shape[0],2))
    # print(coord.shape)
    points = cluster_points(coord)
    return points

# TODO: return corrected corrners
def drawExtractedSquare(img, points):
   
    x_dim = points.shape[0]
    points = points.reshape(x_dim, 2)
    
    points = points.astype(int)
    print(points)

    x, y, w, h = cv.boundingRect(points)
    p1 = (x, y+h)  # bottom-left
    print(p1)
    cv.circle(img, p1, 3, (255, 255, 0), 2)

    currentYmin = y+h
    currentXmax = x
    currentXmin = x+w
    p2 = 0  # top-right
    p3 = 0  # bottom-right
    p4 = 0  # top-left
    for point in points:
        point = tuple(point)
        print(point)
        if point[1] < currentYmin or point[0] > currentXmax:
            currentYmin = point[1]
            p2 = point
        if point[0] > currentXmax:
            currentXmax = point[0]
            p3 = point

        if point[1] <= y + 10:
            if point[0] < currentXmin:
                currentXmin = point[0]
                p4 = point
        # cv.circle(img, point, 1, (255, 255, 255), 2)

    if not p2 == 0:
        print(p2)
        cv.circle(img, p2, 1, (255, 255, 0), 2)
    if not p3 == 0:
        print(p3)
        cv.circle(img, p3, 1, (255, 255, 0), 2)
    if not p4 == 0:
        print(p4)
        cv.circle(img, p4, 1, (255, 255, 0), 2)
        # cv.circle(img, point, 1, (255, 0, 255), 2)
    correctedPoints = CoordinateSystemTools(points[0], points[1], points[2], points[3])
    
    return correctedPoints

# todo fix it


def removeClosePoints(points, center, threshold):
    tempPoints = points.copy()
    for i in range(len(points)):

        currentPoint = points[i]
        # if not cornerPoints.isInsidePolygon(currentPoint):
        #     tempPoints.remove(currentPoint)
        #     break

        for j in range(len(points)):
            commparedPoint = points[j]

            if commparedPoint == currentPoint:
                break
            # if math.dist(currentPoint, commparedPoint) < threshhold:
            #     if math.dist(currentPoint, center) > math.dist(commparedPoint, center):
            if abs(math.hypot(currentPoint[0]-commparedPoint[0], currentPoint[1]-commparedPoint[1])) < threshold:
                if abs(math.hypot(currentPoint[0]-center[0], currentPoint[1]-center[1])) > abs(math.hypot(commparedPoint[0]-center[0], commparedPoint[1]-center[1])):
                    if(currentPoint in tempPoints):
                        tempPoints.remove(currentPoint)

                else:
                    if(commparedPoint in tempPoints):
                        tempPoints.remove(commparedPoint)

    return tempPoints


def organizeSave(points):
    row = []
    allRows = []
    for i in range(1, len(points)+1):
        row.append(points[i-1])
        if i % 9 == 0 and i != 0:
            allRows.append(row)
            row = []
    with open('points.txt', 'w') as file:
        for i in range(len(allRows)):
            for point in allRows[i]:
                file.write(f'{point}- ')
            file.write('\n')
        file.close()
    return allRows


def readPoints():
    file = open('points.txt', 'r')
    lines = file.readlines()
    points = []
    for line in lines:
        row = line.split("- ")
        row = stringToPoints(row)
        points.append(row)
        row = []

    return points


def stringToPoints(strRow):
    row = []
    for point in strRow:
        if not point == '\n':
            point = point[1:-2]
            point = point.split(", ")
            point = (float(point[0]), float(point[1]))
            row.append(point)
    return row

# Crops and returns a square


def crop(img, square):
    points = square.points()
    # print(points)
    p1 = points[1]
    p4 = points[3]
   
    x = int(p1[0])
    w = int(p4[0])
    y = int(p1[1])
    h = int(p4[1])

    # newImg = img[y:y+h, x:x+w] 
    newImg = img[y-5:h+5, x-5:w+5]
    # newImg = img[y:h, x:w]
    # newImg = img[x:w, y:h]
    # print(newImg)

    newImg = cv.resize(newImg, (256, 256))
    return newImg


def writeOutSquares(squares, path, index):
    print('writing ...')
    for row in squares:
        for s in row:
            filename = f'{path}{str(index)}.png'
            print(filename)
            cv.imwrite(filename, s)
            index += 1
            
