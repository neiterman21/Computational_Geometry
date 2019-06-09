from hw3.geolib.Structures import *
from hw3.geolib.FunctionaHelpers import *


def sort_points(points):
    """ This function sorts the list of points by radial order, it does so w.r.t to the minimal point
    inside the array. """

    min_point = extrema(points, key=lambda point: point, comparator=Point.less)
    points = filter_(points, lambda point: point != min_point)  # take the minimum point out of list
    # of points that should be sorted.

    less_comparator = Point.less_radial(min_point)  # define comparator w.r.t to the minimal point.
    merge_sort(points, key=lambda point: point, comparator=less_comparator)
    points = [min_point] + points

    for i in range(1, len(points) + 1):
        points[i - 1].label = i

    return points


def triangulate(points):
    """
    This function accepts list of points and performs graham-scan algorithm for triangulation of these points.
    :param points:  List of Point objects, the list of points.
    :return:        Two lists - [Triangles, Edges]. The first holds the triangles defined by the points and the
                    adjacency relationships between them, while the second is the list of edges created during the
                    triangulation procedure.
    """

    edges = []
    points = sort_points(points)
    triangles = []

    axis_point = points[0]

    stack_ = [points[0], points[1]]                         # stack of points for the graham scan
    triangle_stack = []                                     # stack of triangles for closing them correctly

    edges.append(Edge.create_edge(points[1], points[0]))
    i = 2

    while i < len(points):

        curr_point = points[i % len(points)]                # the point we currently check
        e1 = Edge.create_edge(stack_[-1], curr_point)
        e2 = Edge.create_edge(curr_point, axis_point)

        # the construction of the trivial triangle with the axis point
        convex_triangle = Triangle(edges[-1].twin, e1, e2)
        if triangles:
            Triangle.set_adj_triangles(convex_triangle, triangles[-1])
        triangles.append(convex_triangle)

        edges.extend([e1, e2])

        if orient(stack_[-2], stack_[-1], curr_point) == TURN_LEFT:
            stack_.append(curr_point)

        elif orient(stack_[-2], stack_[-1], curr_point) == TURN_RIGHT:

            # this loop will run O(n) times at most
            adj_triangle_1 = convex_triangle
            while len(stack_) > 1 and orient(curr_point, stack_[-1], stack_[-2]) == TURN_LEFT:

                e = Edge.create_edge(curr_point, stack_[-2])    # new edge that should be added
                e_ = Edge(stack_[-1], stack_[-2])               # the `special edge', for searching for adjacent
                                                                # triangle in the triangles stacks

                # define the adj triangles for the potential newly created triangle
                # this function looks up for the adj triangle inside the history triangles
                # this function will run at most O(n) times - mathematically should be verified.
                adj_triangle_2 = triangle_stack.pop()
                while e_ != adj_triangle_2.e2:
                    adj_triangle_2 = triangle_stack.pop()

                new_triangle = Triangle(adj_triangle_2.e2.twin, e.twin, adj_triangle_1.e2.twin)

                triangles.insert(-1, new_triangle)          # update the triangle list
                triangle_stack.append(new_triangle)     # update the history stack

                # update the adjacency relationships
                Triangle.set_adj_triangles(new_triangle, adj_triangle_1)
                Triangle.set_adj_triangles(new_triangle, adj_triangle_2)

                adj_triangle_1 = new_triangle

                edges.insert(-1, e.twin)
                stack_.pop()
            stack_.append(curr_point)

        # advance the loop
        triangle_stack.append(convex_triangle)
        i += 1

    edges = edges[:-2]

    return triangles, edges


def make_curve(points):
    """
    This function takes input of a list of points and constructs a curve made of Edges
    :param points: List of points
    :return: List of Edges
    """
    curve = []
    for i in range(0, len(points) - 1):
        curve.append(Edge(points[i], points[i + 1]))
    return curve


def find_starting_triangle(triangles, curve):
    """
    This function computes the triangle where curve starts.
    :param triangles:
    :param curve:
    :return: next triangle, previous triangle, intersecting edges, next edge index
    """
    for triangle in triangles:
        if triangle.is_point_inside(curve[0].p1):
            return triangle


def next_triangle(current_triangle, previous_triangle, edge):
    intersecting_edges = current_triangle.get_intersecting_edges_indices(edge)

    result = [current_triangle, current_triangle, []]

    if len(intersecting_edges) == 0:
        pass
    elif len(intersecting_edges) == 1:
        if previous_triangle is not None and current_triangle.adj_triangles[intersecting_edges[0]] == previous_triangle:
            pass
        else:
            result[0] = current_triangle.adj_triangles[intersecting_edges[0]]
            result[1] = current_triangle
            result[2] = [current_triangle.edges[intersecting_edges[0]]]
    else:
        i = 0
        if current_triangle.adj_triangles[intersecting_edges[0]] == previous_triangle:
            i = 1
        result[0] = current_triangle.adj_triangles[intersecting_edges[i]]
        result[1] = current_triangle
        result[2] = [current_triangle.edges[intersecting_edges[i]]]

    return result


def compute_route(triangles, curve):
    """
    This function takes map that consist our of triangles and the curve in form of list of edges. This function returns
    list of edges of the triangles such that is a shortest path on the map.
    :param triangles:   Map that consists out of triangles.
    :param curve:       Edges that represent the curve
    :return:            List of edges that represent the intersection of triangles and curve.
    """
    route = []
    prev_triangle = None
    current_triangle = find_starting_triangle(triangles, curve)

    edge_index = 0
    while edge_index < len(curve):
        current_triangle, prev_triangle, intersecting_edges = next_triangle(current_triangle, prev_triangle, curve[edge_index])
        if prev_triangle.is_point_inside(curve[edge_index].p2):
            edge_index += 1
        route.extend(intersecting_edges)

    return route


def reduce_route(route):
    i = 0
    j = 1
    cut_ranges = []
    while i < len(route):
        j = i + 1
        while j < len(route) and route[i] == route[j]:
            j += 1
        cut_ranges.append([i, j])
        i = j

    return [route[index[0]] for index in cut_ranges]

