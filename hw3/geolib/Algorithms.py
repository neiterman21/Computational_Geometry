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


def graham_scan(points):
    stack = [points[0], points[1]]
    bad_points = []
    for point in points[2:]:
        while len(stack) > 1 and orient(stack[-2], stack[-1], point) < 0:
            bad_points.append(stack.pop())
        stack.append(point)
    return stack, bad_points


def triangulate(points):
    """
    This function takes as input a list of Points.
    :param points: List of points.
    :return: List of triangles.
    """

    from Structures import Triangle
    triangles = []
    hulls = []
    points = sort_points(points)

    while len(points) > 2:
        points = sort_points(points)
        hull, points = graham_scan(points)
        hulls.append(hull)

    # bad code don't use!
    edges = []
    j = 0
    from Structures import Edge
    for i in range(0, len(hulls[1])):
        prev = hulls[1][(i - 1) % len(hulls[1])]
        current = hulls[1][i]
        next = hulls[1][(i + 1) % len(hulls[1])]
        done = False
        while not done and j < len(hulls[0]):
            try:
                temp_point = hulls[0][j]
            except:
                print(i)
                print(j)
                print(len(hulls[0]))
                exit(1)
            temp_edge = Edge(current, temp_point)
            if orient(current, next, temp_point) == -1 and orient(current, prev, temp_point) == 1:
                edges.append(temp_edge)
                j += 1
            else:
                done = True

    return hulls, edges


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
        points.append(Point(randint(0, 100), randint(0, 100)))

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


def test_graham_scan():
    from random import randint
    from Structures import Point

    # construct a test data-set
    points = []
    for i in range(10):
        points.append(Point(randint(0, 30), randint(0, 30)))
    points = sort_points(points)

    print("points")
    print(points)

    convex_hull, bad_points = graham_scan(points)

    print(convex_hull)

    px = [point.x for point in points]
    py = [point.y for point in points]
    cx = [point.x for point in convex_hull]
    cy = [point.y for point in convex_hull]
    bx = [point.x for point in bad_points]
    by = [point.y for point in bad_points]

    import matplotlib.pyplot as plt
    plt.scatter(px, py, c='b')
    plt.scatter(bx, by, c='r')
    plt.gca().add_patch(plt.Polygon([point.vec for point in convex_hull], fill=False, ls='-'))
    plt.show()


def test_hull_decomposition():
    from random import randint
    from Structures import Point

    # construct a test data-set
    points = []
    for i in range(40):
        points.append(Point(randint(0, 30), randint(0, 30)))

    hulls, edges = triangulate(points)

    print("Hulls")
    from matplotlib import pyplot as plt
    import matplotlib.lines as mlines
    plt.figure()
    x = [point.x for point in points]
    y = [point.y for point in points]
    plt.scatter(x, y, s=20, color='b')

    for hull in hulls:
        print(hull)
        plt.gca().add_patch(plt.Polygon([point.vec for point in hull], fill=False, ls='-'))

    print("Edges")
    for edge in edges:
        print(edge)
        # plt.gca().add_patch(mlines.Line2D(edge.p1.vec, edge.p2.vec))
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

# test_triangulation()

# test_graham_scan()

test_hull_decomposition()