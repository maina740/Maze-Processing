import numpy as np
import utils
import cv2 as cv
from imgp import display_image




weight = np.array([2, 4, 3])
max_distance_of_a_marker_from_a_edge = 40
max_black_bgr = 60
window_margin = 10



def check_image_dimensions(maze_height, maze_width, x, y):
    if y > maze_height or x > maze_width:
        print("Image you provided posses an edge in the maze that goes out of the image, exiting!")
        exit(1)

# Check whether a particular coordinate is making any edge or not
def is_corner_in_this_pixel_window(window, coordinates, y, x, index):
    lines = window.shape[index]
    vertex = 0
    for coordinate in coordinates:
        # print(coordinate)
        x_coordinate, y_coordinate = coordinate[1], coordinate[0]

        if index == 0:
            if x_coordinate == x and y_coordinate >= y and y_coordinate <= y + lines:
                vertex = coordinate[2] + 1
                break;
        else:
            if y_coordinate == y and x_coordinate >= x and x_coordinate <= x + lines:
                vertex = coordinate[2] + 1
                break

    return vertex


# Return the number of black pixels found
def process_the_pixel_window(window, index):
    lines = window.shape[index]

    # print(window.shape)
    black_pixels = 0
    for line in range(lines):
        if index == 0:
            if utils.get_average(window[line, 0]) < max_black_bgr:
                black_pixels += 1
        else:
            if utils.get_average(window[0, line]) < max_black_bgr:
                black_pixels += 1

    if black_pixels > 8:
        return True
    else:
        return False


# Sub function for generating detecting an edge if it's there in the maze
def generate_edges(coordinates, maze, index):
    edges = np.array([[0, 0, 0]])
    for coordinate in coordinates:
        x, y, vertex_u = coordinate[1], coordinate[0], coordinate[2] + 1

        top_y_coordinate, bottom_y_coordinate = y - 20, y + 20
        left_x_coordinate, right_x_coordinate = x - 20, x + 20

        # generate edge along width if exits
        window = maze[top_y_coordinate:bottom_y_coordinate, x:x + 1]
        while process_the_pixel_window(window, index) == True:
            vertex_v = is_corner_in_this_pixel_window(window, coordinates, top_y_coordinate, x + 1, index)
            if vertex_v > 0:
                # print(vertex_u, vertex_v)
                edges = np.append(edges, [[vertex_u, vertex_v, 0]], axis = 0)
                break

            x += 1
            window = maze[top_y_coordinate:bottom_y_coordinate, x:x + 1]
            check_image_dimensions(maze.shape[0], maze.shape[1], x, y)


        # generate edge along height if exists
        window = maze[y:y + 1, left_x_coordinate:right_x_coordinate]
        while process_the_pixel_window(window, 1 - index) == True:
            vertex_v = is_corner_in_this_pixel_window(window, coordinates, y + 1, left_x_coordinate, 1 - index)
            if vertex_v > 0:
                # print(vertex_u, vertex_v)
                edges = np.append(edges, [[vertex_u, vertex_v, 0]], axis = 0)
                break

            y += 1
            window = maze[y:y + 1, left_x_coordinate:right_x_coordinate]
            check_image_dimensions(maze.shape[0], maze.shape[1], x, y)

    # print(edges)
    return np.delete(edges, 0, axis = 0)


# Generate if any edge if present in the maze
def generate_edges_using_a_pixels_window(__corners, maze):
    total_corners = len(__corners)

    corners = np.array([[0, 0, 0]])
    for i in range(total_corners):
        corners = np.append(corners, [[__corners[i][0], __corners[i][1], i]], axis = 0)

    corners = np.delete(corners, 0, axis = 0)
    # corners = format_xy_coordinates_of_corners(__corners)
    edges = generate_edges(corners, maze, 0)

    return (corners, edges)



# Add weight of the edge to the matrix of edges
def add_weight(edges, bgr, j):
    b, g, r = bgr
    if b > g and b > r:
        edges[j][2] += weight[0]
    elif g > b and g > r:
        edges[j][2] += weight[1]
    else:
        edges[j][2] += weight[2]

# Detect if there is any marker around a particular edge
def is_the_marker_around_the_edge(base, lower_bound, upper_bound, coordinate, maze, index, edges, j):
    a, b = coordinate[index], coordinate[1 - index]
    if a >= lower_bound and a <= upper_bound and b >= base - max_distance_of_a_marker_from_a_edge and b <= base + max_distance_of_a_marker_from_a_edge:
        if index == 1:
            add_weight(edges, maze[b, a], j)
            # print(edge, (b, a), maze[b, a])
        else:
            add_weight(edges, maze[a, b], j)
            # print(edge, (a, b), maze[a, b])


# Generate weights of edges
def generate_edges_weights(edges, markers, corners, maze):
    __edges = np.array([[0, 0, 0]])
    for edge in edges:
        __edges = np.append(__edges, [edge], axis = 0)

    __edges = np.delete(__edges, 0, axis = 0)

    __markers = np.array([[0, 0]])
    for marker in markers:
        __markers = np.append(__markers, [[marker[1], marker[0]]], axis = 0)

    __markers = np.delete(__markers, 0, axis = 0)

    edges_corners = np.array([[[0, 0], [0, 0]]])
    for edge in __edges:
        u, v = edge[0] - 1, edge[1] - 1
        edges_corners = np.append(edges_corners, [[[corners[u][0], corners[u][1]], [corners[v][0], corners[v][1]]]], axis = 0)

    edges_corners = np.delete(edges_corners, 0, axis = 0)
    length = len(edges_corners)
    for i in range(length):
        edge_corners = edges_corners[i]
        x1, x2, y1, y2 = edge_corners[0][1], edge_corners[1][1], edge_corners[0][0], edge_corners[1][0]
        # print(y1, x1, ' ', y2, x2)
        for marker in markers:
            if abs(y1 - y2) < 10:
                is_the_marker_around_the_edge(y1, x1, x2, marker, maze, 1, __edges, i)
            else:
                is_the_marker_around_the_edge(x1, y1, y2, marker, maze, 0, __edges, i)

    # print(__edges)
    return __edges


# Print edges
def display_edges(edges):
    print("Weight of blue marker : " + str(weight[0]))
    print("Weight of green marker : " + str(weight[1]))
    print("Weight of red marker : " + str(weight[2]) + '\n')

    total_edges = len(edges)
    print("Edges associated with the maze is as follow,\nTotal undirected edges (directed edges * 2) : " + str(total_edges * 2))
    for edge in edges:
        print(str(edge[0]) + " --> " + str(edge[1]) + "    weight : " + str(edge[2]))


# Print the graph data structure
def display_graph(graph):
    print("\nThe graph (Data structure) associated with the maze is as follows,")
    length = len(graph)

    print("Source --> [destination_1, edge_weight_1], [destination_2, edge_weight_2], ... ,[destination_n, edge_weight_n]")
    for i in range(length):
        if i == 0:
            continue
        print(str(i) + " --> " + str(graph[i]))


# Print the robot's location
def display_markers(markers, maze):
    __maze = maze.copy()
    total_markers = len(markers)
    print("\nMarkers ((y, x) coorinate of the centre) assocaited with the maze are as follow,\nTotal markers : " + str(total_markers))

    _b, _g, _r = 0, 0, 0
    for i in range(total_markers):
        marker = markers[i]
        # print(marker)
        x, y = marker[1], marker[0]
        mark = str(i + 1)
        __maze = cv.putText(__maze, mark, (x - 5, y + 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        print(str(i + 1) + " : (" + str(y) + ',' + str(x) + ')')
        b, g, r = maze[y, x]
        if b > g and b > r:
            _b += 1
        elif g > b and g > r:
            _g += 1
        else:
            _r += 1

    print("Total red markers : " + str(_r))
    print("Total green markers : " + str(_g))
    print("Total blue markers : " + str(_b))

    return __maze


# Create an adjacency list (undirected graph) according to the generated edges
def create_graph(vertices, edges):
    # graph = np.array([])
    undirected_graph = []
    for i in range(vertices + 1):
        undirected_graph.append([])
        # graph = np.append(graph, [[1]], axis = 0)

    for edge in edges:
        u, v, weight = edge[0], edge[1], edge[2]

        undirected_graph[u].append([v, weight])
        undirected_graph[v].append([u, weight])
        # graph[u] = np.append(graph[u], [[v, weight]], axis = 0)
        # graph[v] = np.append(graph[v], [[u, weight]], axis = 0)

    return undirected_graph



def find_the_robot_location():
    pass
