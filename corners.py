import numpy as np
import cv2 as cv

# local moduls
from utils import get_average, euclidean_distance, bound



max_distance_between_tow_close_corners = 30
corner_adjustment = 8

# Returns a numpy array that has only necessary corners of a maze, i.e it filters out the extra corners (i.e coordinates) detected by the cornerHarris() function and leaves a single corner for a single corner of a maze
def remove_unnecessary_corners(coordinates):
    __coordinates_copy = coordinates
    length = len(__coordinates_copy)
    for i in range(length):
        _x__coordinate = coordinates[i]
        deleted = 0
        for j in range(i + 1, length):
            _y__coordinate = coordinates[j]
            distance = euclidean_distance(_x__coordinate, _y__coordinate)
            # print("Distance : ", distance)
            if distance < max_distance_between_tow_close_corners:
                    __coordinates_copy[j] = [0, 0]

    deleted = 0
    for i in range(length):
        if __coordinates_copy[i - deleted][0] + __coordinates_copy[i - deleted][1] == 0:
            # print(i, deleted, len(__coordinates_copy), i - deleted)
            __coordinates_copy = np.delete(__coordinates_copy, i - deleted, 0)
            deleted += 1

    return __coordinates_copy
# coordinates = remove_unnecessary_corners(coordinates)


# Bring corners from partially black area to completely black area
def adjust_corners(coordinates, maze):
	for i in range(0, maze.shape[1]):
		for j in range(0, maze.shape[0]):
			average = get_average(maze[j, i])
			if average > 50 and average < 200:
				maze[j, i] = (0, 0, 0)
				
	for coordinate in coordinates:
		x_coordinate, y_coordinate = coordinate[1], coordinate[0]

		# print(x_coordinate, y_coordinate)
		left_pixels, right_pixels = 0, 0
		for x in range(x_coordinate, x_coordinate + 10):
			x = bound(0, x, 800)
			right_pixels += get_average(maze[y_coordinate, x])

		for x in range(x_coordinate - 10, x_coordinate):
			x = bound(0, x, 800)
			left_pixels += get_average(maze[y_coordinate, x])


		bottom_pixels, top_pixels = 0, 0
		for y in range(y_coordinate, y_coordinate + 10):
			y = bound(0, y, 800)
			bottom_pixels += get_average(maze[y, x_coordinate])

		for y in range(y_coordinate - 10, y_coordinate):
			y = bound(0, y, 800)
			top_pixels += get_average(maze[y, x_coordinate])


		if(left_pixels < right_pixels):
			coordinate[1] -= corner_adjustment
		else:
			coordinate[1] += corner_adjustment

		if top_pixels < bottom_pixels:
			coordinate[0] -= corner_adjustment
		else:
			coordinate[0] += corner_adjustment

	return coordinates




# set a particular coordinate's value to the average of coordinate values (that has distance less than 21 pixels between them), for both x and y axis
def align_corners(coordinates):
    total_corners = len(coordinates)

    # align corners horizontally that has distance less than 20 pixels between them
    i = 0
    while i < total_corners:
        y, average = coordinates[i][0], 0
        indexes = np.array([], dtype = np.uint8)

        while i < total_corners and coordinates[i][0] - y <= 20:
            average += coordinates[i][0]
            indexes = np.append(indexes, [i], 0)
            i += 1

        average = average // len(indexes)

        for index in indexes:
            coordinates[index][0] = average

    # align corners vertically that has distance less than 20 pixels between them
    i = 0
    while i < total_corners:
        j, y = i, coordinates[i][1]

        indexes = np.array([], dtype = np.uint8)
        average = 0
        while j < total_corners:
            if abs(coordinates[j][1] - y) <= 20:
                average += coordinates[j][1]
                indexes = np.append(indexes, [j], 0)

            j += 1

        average = average // len(indexes)

        for index in indexes:
            coordinates[index][1] = average

        i += 1

    return coordinates
# align_corners(coordinates)
