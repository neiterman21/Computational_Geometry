import sys
from matplotlib import pyplot as plt


def line2numbers(line):
    """ Function takes string line and converts it into list of integers. """
    from FunctionaHelpers import filter_, map_
    l = [x for x in line.strip("\n").split(" ")]
    l = filter_(l, lambda a: a != '')
    l = map_(l, lambda a: int(a))
    return l


def numbers2points(numbers):
    """ It converts list of integer numbers to list of 2d points. """
    from geolib.Structures import Point
    error_msg(len(numbers) % 2 == 1, "An odd number of numbers was supplied cannot construct the hull.")
    return [Point(numbers[i], numbers[i + 1]) for i in range(0, len(numbers), 2)]


def error_msg(condition, msg):
    """ Function checks the condition, and if it false then it prints relevant
    error on the screen and exits the program. """
    if condition:
        print("Error: " + msg)
        exit(1)


def get_input():
    """ Responsible to verify the input of the program and retrieving an input
    information."""

    # Check the number of supplied arguments
    error_msg(len(sys.argv) <= 1, "No input file was supplied. ")

    # Verify the the filename is legal and open operation is done.
    lines = []
    try:
        lines = open(sys.argv[1], "r").readlines()
    except:
        lines = []
        error_msg(True, "Could not open file {}".format(sys.argv[1]))

    print(lines)
    # Verify that file contains at least 3 lines.
    error_msg(len(lines) < 4, "The supplied input file has an illegal format")

    # Construct data
    number_of_obstacle_points = line2numbers(lines[0])[0]
    number_of_curve_points = line2numbers(lines[2])[0]

    obstacle_points_line_ = ""
    curve_points_line_ = ""
    obstacle_points_line_ += lines[1].strip("\n")
    curve_points_line_ += lines[3].strip("\n")

    obstacle_points = numbers2points(line2numbers(obstacle_points_line_))

    curve_points = numbers2points(line2numbers(curve_points_line_))

    min_x = min(curve_points, key=lambda point: point.x).x
    min_y = min(curve_points, key=lambda point: point.y).y

    max_x = max(curve_points, key=lambda point: point.x).x
    max_y = max(curve_points, key=lambda point: point.y).y

    from geolib.Structures import Point
    obstacle_points += [Point(min_x, min_y), Point(min_x, max_y),
                        Point(max_x, min_y), Point(max_x, max_y)]

    # Verify the content of the file.
    error_msg(number_of_obstacle_points + 4 != len(obstacle_points),
              "The supplied input file has an illegal format")
    error_msg(number_of_curve_points != len(curve_points),
              "The supplied input file has an illegal format")

    # Check if user wants to plot the data on the screen.
    plot = False
    try:
        plot = sys.argv[2] == 'plot'
    except:
        pass

    return obstacle_points, curve_points, plot


def plot_state(obstacle_points, curve_points):
    """ Shows the convex hull and the query point on the screen. """
    ox = []
    oy = []

    cx = []
    cy = []

    for point in obstacle_points:
        ox.append(point.x)
        oy.append(point.y)

    for point in curve_points:
        cx.append(point.x)
        cy.append(point.y)

    plt.plot(cx, cy, "bo-", ox, oy, "ro")
    plt.show()

