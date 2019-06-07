import matplotlib.pyplot as plt
from random import randint

from hw3.geolib.Structures import *
from hw3.geolib.Algorithms import compute_route, sort_points, triangulate_


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
    # construct a test data-set
    points = []
    for i in range(10):
        points.append(Point(randint(0, 20), randint(0, 20)))

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

    triangles, edges = triangulate_(points)

    fig, ax0 = plt.subplots(1)

    x = [point.x for point in points]
    y = [point.y for point in points]
    ax0.scatter(x, y, s=20, color='b')

    for edge in edges:
        ax0.plot([edge.p1.x, edge.p2.x], [edge.p1.y, edge.p2.y])

    # print("Triangles:")
    # for t in triangles:
    #    print(t)
    #    plt.gca().add_patch(plt.Polygon(t.vec, fill=False, ls='-'))

    plt.show()


def test_compute_route():
    obstical_points = [Point(1, 0), Point(3, 2), Point(5, 7), Point(6, 12), Point(8, 4), Point(9, 13), Point(11, 19),
                       Point(12, 9), Point(15, 3)]

    px = [point.x for point in obstical_points]
    py = [point.y for point in obstical_points]

    edges = [Edge(obstical_points[0], obstical_points[1]),
             Edge(obstical_points[0], obstical_points[2]),
             Edge(obstical_points[0], obstical_points[3]),
             Edge(obstical_points[1], obstical_points[2]),
             Edge(obstical_points[2], obstical_points[3]),
             Edge(obstical_points[1], obstical_points[4]),
             Edge(obstical_points[2], obstical_points[4]),
             Edge(obstical_points[4], obstical_points[5]),
             Edge(obstical_points[4], obstical_points[6]),
             Edge(obstical_points[4], obstical_points[7]),
             Edge(obstical_points[4], obstical_points[8]),
             Edge(obstical_points[2], obstical_points[5]),
             Edge(obstical_points[3], obstical_points[5]),
             Edge(obstical_points[5], obstical_points[6]),
             Edge(obstical_points[6], obstical_points[7]),
             Edge(obstical_points[7], obstical_points[8]),
             Edge(obstical_points[0], obstical_points[4]),
             Edge(obstical_points[0], obstical_points[8]),
             Edge(obstical_points[3], obstical_points[6]),
             Edge(obstical_points[6], obstical_points[8]), ]

    triangels = []

    for point in obstical_points:
        for edge in edges:
            if edge.p1 == point or edge.p2 == point:
                point.out_edges.append(edge)

    for point in obstical_points:
        for edge1 in point.out_edges:
            for edge2 in point.out_edges:
                p1 = edge1.p2 if point == edge1.p1 else edge1.p1
                p2 = edge2.p2 if point == edge2.p1 else edge2.p1
            for edge in edges:
                if edge == Edge(p1, p2):
                    triangle = Triangle(point, p1, p2)
                    if triangle not in triangels and triangle.no_point_inside(obstical_points):
                        triangels.append(triangle)

    curv = [Point(1.5, 0.3), Point(10, 8.6), Point(11.3, 2.5)]

    rout = compute_route(triangels, curv)
    print(rout)

    fig, ax0 = plt.subplots(1)
    ax0.scatter(px, py, c='b')
    for edge in edges:
        ax0.plot([edge.p1.x, edge.p2.x], [edge.p1.y, edge.p2.y])

    cpx = [point.x for point in curv]
    cpy = [point.y for point in curv]

    ax0.plot(cpx, cpy)
    plt.show()


# test_sort_points()
test_triangulation()
# test_compute_route()
