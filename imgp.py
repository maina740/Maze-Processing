import cv2 as cv
import numpy as np
from utils import get_average

# Check if the image is opened
def is_opened(image):
    if image is None:
        print("Couldn't open the file!")
        exit(1)



# Display the image
def display_image(image, image_title = "Image"):
    while True:
        cv.imshow(image_title, image)
        key = cv.waitKey(1)
        if key == 27:
            break

    cv.destroyAllWindows()


# Draw corresponding vertex number or dots on each corner in the image, depends on the 'what' variable
def draw_vertices_or_dots(corners, maze, what):
    __maze = maze.copy()
    if what == 0:
        for corner in corners:
            cv.circle(__maze, (corner[1], corner[0]), 4, (0, 0, 255), -1)
    elif what == 1:
        for corner in corners:
            index = str(int('1') + corner[2])
            __maze = cv.putText(__maze, index, (corner[1] - 10, corner[0] + 5), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return __maze



# Detect corners (coordinates where the intensity of light changes rapidly along the both x and y axes) in the image
def detect_corners(maze):
    # maze = cv.resize(maze, (dimensions[1], dimensions[0]))

    # Convert the image from BGR to GRAY
    gray_maze = cv.cvtColor(maze, cv.COLOR_BGR2GRAY)
    # Normal thresholding
#    _, _mask = cv.threshold(gray_maze, 20, 255, cv.THRESH_BINARY)
#    # Adaptive thresholding
#    #_mask_ = cv.adaptiveThreshold(gray_maze, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
#    display_image(_mask, "Just the track")

    # Detect corners
    gray_maze = cv.medianBlur(gray_maze, 5)
    corners = cv.cornerHarris(gray_maze, 2, 3, 0.04)
    # display_image(corners, "Corners")

    # Create a complete black image of size similiar to actual image and draw corners on it
    mask = np.zeros_like(gray_maze)
    mask[corners > 0.01 * corners.max()] = 255
    # display_image(mask, "mask")

    # Get the actual coordinates of all the corners
    coordinates = np.argwhere(mask)

    # Dilate the image and draw corners on the actual image
    cv.dilate(maze, None)
    maze[corners > 0.025 * corners.max()] = [0, 0, 255]

    return (coordinates, maze)



def remove_track(image):
    _image = image.copy()
    rows, cols = _image.shape[0], _image.shape[1]
    for row in range(rows):
        for col in range(cols):
            if get_average(_image[row, col]) < 20:
                _image[row, col] = (255, 255, 255)

    return _image


def get_xy_coordinates(coordinates, length):
    x, y = 0, 0
    for xy in coordinates:
        # print(xy)
        x += xy[0][0]
        y += xy[0][1]

    x //= length
    y //= length

    return (x, y)


def detect_markers_and_robot(maze):
    _maze = remove_track(maze)
    gray_maze = cv.cvtColor(_maze, cv.COLOR_BGR2GRAY)
    __, _mask = cv.threshold(gray_maze, 240, 255, cv.THRESH_BINARY)

    markers, robot = np.array([[0, 0]], dtype = np.uint16), np.array([], dtype = np.uint16)

    contours, __ = cv.findContours(_mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        # print(approx)
        length = len(approx)
        x, y = get_xy_coordinates(approx, length)
        if length == 4:
            b, g, r = maze[y, x]
            if g > b and g > r:
                robot = np.append(robot, [y, x], axis = 0)
        elif length > 4:
            markers = np.append(markers, [[y, x]], axis = 0)
            # cv.circle(_image, (average_y, average_x), 1, (0, 0, 0), 2)


    return (np.delete(markers, 0, axis = 0), robot)
