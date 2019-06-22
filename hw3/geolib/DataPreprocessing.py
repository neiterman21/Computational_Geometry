import sys
from matplotlib import pyplot as plt
from hw3.geolib.FunctionaHelpers import *
from hw3.geolib.Structures import *


def line2numbers(line):
    """ Function takes string line and converts it into list of integers. """
    # I damn love functional programming
    return map_(filter_([x for x in line.strip("\n").split(" ")], lambda a: a != ''), lambda a: float(a))


def numbers2points(numbers):
    """ It converts list of integer numbers to list of 2d points. """
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
    try:
        lines = open(sys.argv[1], "r").readlines()
    except IOError:
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

    obstacle_points += compute_big_rectangle(obstacle_points + curve_points)

    # Verify the content of the file.
    error_msg(number_of_obstacle_points + 4 != len(obstacle_points),
              "The supplied input file has an illegal format")
    error_msg(number_of_curve_points != len(curve_points),
              "The supplied input file has an illegal format")

    # Check if user wants to plot the data on the screen.
    plot = False
    try:
        plot = sys.argv[2] == 'plot'
    except IndexError:
        pass

    return obstacle_points, curve_points, plot


def plot_state(obstacle_points, curve_points, triangles, route):
    """ Shows the convex hull and the query point on the screen. """
    # plot results on the screen
    fig, ax0 = plt.subplots(1)

    # plot the obstacle points
    px = [point.x for point in obstacle_points]
    py = [point.y for point in obstacle_points]
    ax0.scatter(px[:-4], py[:-4], s=20, color='b')
    ax0.scatter(px[-4:], py[-4:], s=20, color='red')
    for i in range(len(obstacle_points)):
        ax0.annotate(obstacle_points[i].label, (px[i], py[i]))

    # plot the triangles
    for t in triangles:
        # print("triangle=" + str(t) + ", adj=" + str(t.adj_triangles))
        plt.gca().add_patch(plt.Polygon(t.points_vec, fill=False, ls='-'))

    # plot the curve on the screen
    cpx = [point.x for point in curve_points]
    cpy = [point.y for point in curve_points]
    ax0.plot(cpx, cpy, c='g')
    from hw3.geolib.Algorithms import make_curve

    for edge in make_curve(curve_points):
        ax0.plot([edge.p1.x, edge.p2.x], [edge.p1.y, edge.p2.y], c='g')

    # plot the reduced route on the screen
    for edge in route:
        ax0.plot([edge.p1.x, edge.p2.x], [edge.p1.y, edge.p2.y], c='b', linewidth=2)

    plt.show()