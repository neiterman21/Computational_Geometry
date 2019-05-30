def orient(p, q, r):
    """Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
    qr = q.x * r.y - q.y * r.x
    pr = p.x * r.y - p.y * r.x
    pq = p.x * q.y - p.y * q.x
    det = qr - pr + pq
    if det > 0:
        return 1
    if det < 0:
        return -1
    return 0


def sort_points(points):
    """ This function sorts the list of points by radial order, it does so w.r.t to the minimal point
    inside the array. """

    from FunctionaHelpers import extrema, merge_sort, filter_
    from Structures import Point

    min_point = extrema(points, key=lambda point: point, comparator=Point.less)
    points = filter_(points, lambda point: point != min_point)  # take the minimum point out of list
                                                                # of points that should be sorted.

    print("min_point" + str(min_point))

    less_comparator = Point.less_radial(min_point)  # define comparator w.r.t to the minimal point.
    merge_sort(points, key=lambda point: point, comparator=less_comparator)
    return [min_point] + points


def triangulate(points):
    """
    This function takes as input a list of Points.
    :param points: List of points.
    :return: List of triangles.
    """

    from Structures import Triangle
    triangles = []
    points = sort_points(points)
    stack = [points[0], points[1]]
    for point in points[2:]:
        p_top = stack.pop()
        p_second_top = stack.pop()
        triangles.append(Triangle(p_second_top, p_top, point))
        stack.append(p_top)
        stack.append(point)

    return triangles, points



def compute_route(triangles, points):
    pass


def reduce_edges(edges):
    pass


def test_sort_points():
    from random import randint
    from Structures import Point

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
    from matplotlib import pyplot as plt
    x = [point.x for point in points]
    y = [point.y for point in points]
    plt.scatter(x, y)
    plt.show()


def test_triangulation():

    from random import randint
    from Structures import Point

    # construct a test data-set
    points = []
    for i in range(10):
        points.append(Point(randint(0, 30), randint(0, 30)))

    triangles, points = triangulate(points)

    print(points)

    import matplotlib.pyplot as plt
    plt.figure()
    x = [point.x for point in points]
    y = [point.y for point in points]
    plt.scatter(x, y, s=20, color='b')

    print("Triangles:")
    for t in triangles:
        print(t)
        plt.gca().add_patch(plt.Polygon(t.vec, fill=False, ls='-'))

    plt.show()

# test_sort_points()

test_triangulation()