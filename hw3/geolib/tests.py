import matplotlib.pyplot as plt
from random import randint

from hw3.geolib.DataPreprocessing import numbers2points, bound_curve
from hw3.geolib.FunctionaHelpers import point_on_line
from hw3.geolib.Structures import *
from hw3.geolib.Algorithms import compute_route, sort_points, triangulate, make_curve, reduce_route


def test_sort_points():
    # construct a test data-set
    points = []
    for i in range(10):
        points.append(Point(randint(0, 30), randint(0, 30)))

    print("initial array of points = ")
    print(points)

    points = sort_points(points)
    print("sorted points = ")
    print(points)

    # plot the results
    x = [point.x for point in points]
    y = [point.y for point in points]
    plt.scatter(x, y)
    plt.show()


def test_triangulation():

    points = []

    #random test set
    for i in range(15):
        points.append(Point(randint(0, 20), randint(0, 20)))

    # test set 1 passed
    # points = [
    #     Point(2, 10),
    #     Point(4, 5),
    #     Point(10, 3),
    #     Point(15, 5),
    #     Point(10, 8),
    #     Point(11, 9),
    #     Point(13, 10),
    #     Point(16, 14)
    # ]

    # test set 2 - passed
    # points = [
    #     Point(1, 9),
    #     Point(9, 3),
    #     Point(18, 3),
    #     Point(7, 8),
    #     Point(13, 11),
    #     Point(10, 14),
    #     Point(19, 20),
    #     Point(15, 20),
    #     Point(4, 17),
    #     Point(3, 20)
    # ]

    # test set 3 -passed
    # points = [
    #     Point(2, 4),
    #     Point(3, 2),
    #     Point(5, 1),
    #     Point(12, 1),
    #     Point(14, 2),
    #     Point(10, 3),
    #     Point(11, 5),
    #     Point(13, 6),
    #     Point(15, 7),
    #     Point(12, 8),
    #     Point(8, 8),
    #     Point(5, 7),
    #     Point(4, 7),
    #     Point(3, 8)
    # ]

    # test set 4 - passed
    # points = [
    #     Point(2, 4),
    #     Point(3, 2),
    #     Point(5, 1),
    #     Point(12, 1),
    #     Point(14, 2),
    #     Point(10, 3),
    #     Point(11, 5),
    #     Point(13, 6),
    #     Point(15, 7),
    #     Point(12, 8),
    #     Point(8, 8),
    #     Point(5, 7),
    #     Point(4, 7),
    #     Point(3, 8),
    #     Point(2.7, 1.3),
    #     Point(2.7, 7.6),
    #     Point(14, 1.3),
    #     Point(14, 7.6)
    # ]

    # test set 5 - passed
    # points = [
    #     Point(2, 4),
    #     Point(20, 0.5),
    #     Point(18, 1.5),
    #     Point(9, 4),
    #     Point(9, 5),
    #     Point(10, 6),
    #     Point(12, 7)
    # ]

    triangles, edges = triangulate(points)

    fig, ax0 = plt.subplots(1)

    x = [point.x for point in points]
    y = [point.y for point in points]
    ax0.scatter(x, y, s=20, color='b')

    for i in range(len(points)):
        ax0.annotate(points[i].label, (x[i], y[i]))

    print("Edges:")
    for edge in edges:
        print(edge)
        # ax0.plot([edge.p1.x, edge.p2.x], [edge.p1.y, edge.p2.y], color='black')

    print("Triangles:")
    for t in triangles:
       print("triangle=" + str(t) + ", adj=" + str(t.adj_triangles))
       plt.gca().add_patch(plt.Polygon(t.points_vec, fill=False, ls='-'))

    plt.show()


def test_compute_route():

    obstacle_input = [randint(0, 30) for i in range(40)]
    curve_input = [randint(0, 30) for i in range(10)]
    route = []

    print("obstacle_input = " + str(obstacle_input))
    print("curve_input = " + str(curve_input))

    # obstacle_input = [
    #     2, 4,
    #     3, 2,
    #     5, 1,
    #     12, 1,
    #     14, 2,
    #     10, 3,
    #     11, 5,
    #     13, 6,
    #     15, 7,
    #     12, 8,
    #     8, 8,
    #     5, 7,
    #     4, 7,
    #     3, 8,
    # ]
    #
    # curve_input = [
    #     2.4, 3.4,
    #     2.8, 3.4,
    #     2.6, 3.0,
    #     3.4, 3.0,
    #     3, 2.5,
    #     5.3, 2.7,
    #     8.6, 1.5,
    #     10.5, 1.8,
    #     9.5, 2.9,
    #     9.3, 3.9,
    #     7.8, 4.8,
    #     10.8, 5.7,
    #     10.2, 6.4
    # ]
    #
    # curve_input = [
    #     2.4, 3.4,
    #     2.8, 3.4,
    #     2.6, 3.0,
    #     3.4, 3.0,
    #     3, 2.5,
    #     5.3, 2.7,
    #     10.5, 1.8,
    #     11.2, 1.4,
    #     12.2, 1.3,
    #     13.2, 1.7,
    #     12.2, 3,
    #     10.8, 3.7,
    #     9.3, 3.9,
    #     5.0, 4.0,
    #     5.16, 5,
    #     11.4, 5.9,
    #     12.6, 3.2,
    #     14, 4.7,
    #     13.5, 7.11,
    #     11.4, 7.6,
    #     9.8, 7.5,
    #     5.4, 6.4,
    #     4.7, 7.6,
    #     2.7, 6.4
    # ]

    # test set 2
    obstacle_input = [
        4, 4,
        6, 2,
        10, 2,
        12, 3,
        8, 5,
        8, 7,
        10, 10
    ]
    curve_input = [
        0, 0.5,
        2, 8,
        7, 3,
        13, 2,
        16, 6,
        8, 10
    ]

    obstacle_points = numbers2points(obstacle_input)

    curve_points = numbers2points(curve_input)
    obstacle_points += bound_curve(curve_points)

    print("obstacle_points = " + str(obstacle_points))
    print("curve_points = " + str(obstacle_points))

    triangles, edges = triangulate(obstacle_points)

    route = compute_route(triangles, make_curve(curve_points))
    print("route = " + str(route))

    route = reduce_route(route)
    print("reduced routes = " + str(route))

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
    for edge in make_curve(curve_points):
        ax0.plot([edge.p1.x, edge.p2.x], [edge.p1.y, edge.p2.y], c='g')

    # plot the reduced route on the screen
    for edge in route:
        ax0.plot([edge.p1.x, edge.p2.x], [edge.p1.y, edge.p2.y], c='b', linewidth=2)

    plt.show()


def test_point_on_line():
    e_start = Point(0, 0)
    e_end = Point(5, 5)
    p1 = Point(4, 4)
    p2 = Point(6, 6)
    print(point_on_line(e_start, e_end, p1))
    print(point_on_line(e_start, e_end, p2))

# test_sort_points()
# test_triangulation()
test_compute_route()
# test_point_on_line()

