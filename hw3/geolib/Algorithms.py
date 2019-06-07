def sort_by_x(point):
    return point.x


def build_first_triangle(points):
    return Triangle(points[0], points[1], points[2])


def sort_points(points):
    """ This function sorts the list of points by radial order, it does so w.r.t to the minimal point
    inside the array. """

    min_point = extrema(points, key=lambda point: point, comparator=Point.less)
    points = filter_(points, lambda point: point != min_point)  # take the minimum point out of list
    # of points that should be sorted.

    less_comparator = Point.less_radial(min_point)  # define comparator w.r.t to the minimal point.
    merge_sort(points, key=lambda point: point, comparator=less_comparator)
    return [min_point] + points


def triangulate_(points):
    edges = []
    triangles = []
    points = sort_points(points)

    print("points = ")
    print(points)

    axis_point = points[0]

    stack_ = [points[0], points[1]]
    edges.append(Edge(points[0], points[1]))
    prev_triangle = None
    i = 2
    while i <= len(points):
        curr_point = points[i % len(points)]
        edges.append(Edge(stack_[-1], curr_point))
        edges.append(Edge(axis_point, curr_point))
        curr_triangle = Triangle(axis_point, stack_[-1], curr_point)
        if orient(stack_[-2], stack_[-1], curr_point) == TURN_LEFT:
            stack_.append(curr_point)
            triangles.append([prev_triangle, curr_triangle])
            prev_triangle = curr_triangle
        elif orient(stack_[-2], stack_[-1], curr_point) == TURN_RIGHT:
            while len(stack_) > 1 and orient(curr_point, stack_[-1], stack_[-2]) == TURN_LEFT:
                edges.append(Edge(curr_point, stack_[-2]))
                stack_.pop()
            stack_.append(curr_point)
        i += 1

    return triangles, edges


def built_curve_from_points(points):
    """
    This function takes input of a list of points and constructs a curve made of Edges
    :param points: List of points
    :return: List of Edges
    """
    curve = []
    for i in range(0, len(points) - 1):
        curve.append(Edge(points[i], points[i + 1]))
    return curve


def compute_route(triangles, points):
    """
    This function takes a path from points and a triangle list
    and returns a list of edges the path passes through
    :param triangles:
    :param points:
    :return: Edges
    """
    path = []
    curve = built_curve_from_points(points)
    working_triangle = None

    for triangle in triangles:
        if triangle.is_point_inside(curve[0].p1):
            working_triangle = triangle
            break

    for path_edge in curve:
        while not working_triangle.is_point_inside(path_edge.p2):
            print("working triangle = " + str(working_triangle))
            edges = working_triangle.get_intersecting_edges(path_edge)
            if len(edges) < 2:
                if working_triangle.is_point_inside(path_edge.p1):
                    out_edge = edges[0]
            else:
                if edges[0] == path[-1]:
                    out_edge = edges[1]
                else:
                    out_edge = edges[0]

            for triangle in triangles:  # shloud be done more efisiantly
                if out_edge in triangle.edges and not triangle == working_triangle:
                    working_triangle = triangle
                    break

            path.append(out_edge)

    return path


def reduce_edges(edges):
    pass
