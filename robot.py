import numpy as np
import cv2 as cv

# local modules
from utils import get_average
from imgp import display_image


def which_corner_is_it(x_coordinate, y_coordinate, maze):
    # black_pixels[0] --> number of black_pixels right to the x-coordinate of the corner
    # black_pixels[1] --> number of black_pixels left to the x-coordinate of the corner

    black_pixels = np.array([0, 0])
    _x = x_coordinate
    while get_average(maze[y_coordinate, _x]) < 50:
        black_pixels[0] += 1
        _x += 1

    _x = x_coordinate
    while get_average(maze[y_coordinate, _x]) < 50:
        black_pixels[1] += 1
        _x -= 1

    return black_pixels[0] > black_pixels[1]



def detect_robot_location(edges, robot, corners, maze):
    __edges = np.array([[0, 0, 0]])
    for edge in edges:
        __edges = np.append(__edges, [edge], axis = 0)

    __edges = np.delete(__edges, 0, axis = 0)

    edges_corners = np.array([[[0, 0], [0, 0]]])
    for edge in __edges:
        u, v = edge[0] - 1, edge[1] - 1
        edges_corners = np.append(edges_corners, [[[corners[u][0], corners[u][1]], [corners[v][0], corners[v][1]]]], axis = 0)

    edges_corners = np.delete(edges_corners, 0, axis = 0)
    length = len(edges_corners)

    robot_x, robot_y = robot[1], robot[0]
    for i in range(length):
        edge_corners = edges_corners[i]
        x1, x2, y1, y2 = edge_corners[0][1], edge_corners[1][1], edge_corners[0][0], edge_corners[1][0]
        # print(y1, x1, ' ', y2, x2)
        if (robot_x >= x1 and robot_x <= x2) or (robot_y >= y1 and robot_y <= y2):
            return __edges[i]

    return [0, 0]



def display_robot(robot, maze):
    print("\nLocation of the robot is given as (y, x) coordinate, where y and x represents the average of y coordinates and x coordinates of 4 corners of the robot's shape (i.e square/rectangle) respectively.\nThe location is : (" + str(robot[0]) + ',' + str(robot[1]) + ")\n")

    coordinates = "Robot (" + str(robot[0]) + ',' + str(robot[1]) + ')'
    __maze = cv.putText(maze, coordinates, (robot[1] - 60, robot[0]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return __maze
