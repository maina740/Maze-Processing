import numpy as np
import cv2 as cv
import math

# import local modules
from corners import remove_unnecessary_corners, adjust_corners
from graph import generate_edges_using_a_pixels_window, display_edges, create_graph, display_graph, generate_edges_weights, display_markers
from imgp import detect_corners, detect_markers_and_robot, display_image, draw_vertices_or_dots, is_opened
from robot import display_robot, detect_robot_location
from utils import get_average


dot, number = 0, 1
dimensions = [800, 800]
image_paths = ["images/maze.jpg", "images/maze(1).jpg", "images/maze(3).webp", "images/maze(4).png", "images/maze(5).jpeg"]
image_path = "images/maze_2.jpg"
#image_path = "images/maze_1.png"



# Read the image
maze = cv.imread(image_path, 1)
is_opened(maze)
display_image(maze, "Maze")

# if maze.shape[0] != dimensions[0] or maze.shape[1] != dimensions[1]:
#     # print("YES")
#     maze = cv.resize(maze, (dimensions[1], dimensions[0]))

# Make a copy so that original image can be used later
_maze = maze.copy()
__maze = maze.copy()



# Get the corner(s) coordinates with cornerHarris()
corners, _maze = detect_corners(_maze)
_maze = draw_vertices_or_dots(corners, __maze, dot)
display_image(_maze, "Corners detected")
# print(corners)


# Remove corners that are not required
corners = remove_unnecessary_corners(corners)
_maze = draw_vertices_or_dots(corners, maze.copy(), dot)
display_image(_maze, "Unnecessary corners removed")
#print(corners)

# If a corner is partially on black and partially on white, bring it to the complete black area, this will help later in generating graph
corners = adjust_corners(corners, _maze)
_maze = draw_vertices_or_dots(corners, __maze, dot)
display_image(_maze, "Corners adjusted")


## Store the edges between the vertices
sorted_corners, _edges = generate_edges_using_a_pixels_window(corners, __maze)

## Detect markers and robot's location
markers, robot = detect_markers_and_robot(__maze)
# print(markers)
## print(robot)

## Generate edges weight
_edges = generate_edges_weights(_edges, markers, sorted_corners, __maze)
display_edges(_edges)


#robot_location = detect_robot_location(_edges, robot, corners, __maze)
#print("Robot's location : ", robot_location)


# Create the adjacency list (undirected graph) according to the generated edges
undirected_graph_of_the_maze = create_graph(len(sorted_corners), _edges)
display_graph(undirected_graph_of_the_maze)


# Draw a marker number and print associated coordinates
_maze = display_markers(markers, __maze)

# Draw robot's location
#_maze = display_robot(robot, _maze)

# Draw vertex number associated with the particular vertex
_maze = draw_vertices_or_dots(sorted_corners, _maze, number)


display_image(_maze, "Final maze")
"""
    To do -
    Robot'as location at the start, end or between an edge
    Robot's score
"""
