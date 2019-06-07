
import matplotlib.pyplot as plt
from FunctionaHelpers import *
from Structures import *
from random import randint


def sort_by_x(point):
    return point.x


def build_first_triangle(points):
    return Triangle(points[0] , points[1], points[2])


def sort_points(points):
    """ This function sorts the list of points by radial order, it does so w.r.t to the minimal point
    inside the array. """


    min_point = extrema(points, key=lambda point: point, comparator=Point.less)
    points = filter_(points, lambda point: point != min_point)  # take the minimum point out of list
                                                                # of points that should be sorted.

    print("min_point" + str(min_point))

    less_comparator = Point.less_radial(min_point)  # define comparator w.r.t to the minimal point.
    merge_sort(points, key=lambda point: point, comparator=less_comparator)
    return [min_point] + points


def graham_scan(points):
    stack = [points[0], points[1]]
    for point in points[2:]:
        while len(stack) > 1 and orient(stack[-2], stack[-1], point) < 0:
            stack.pop()
        stack.append(point)
    return stack


def add_point(stack , point , orient_):
    edges = []
    if orient_ == TURN_RIGHT:
        edges.append(Edge(stack[-1],point))
    while True:
        if (orient(stack[-2] ,stack[-1] , point ) != orient_):
            stack.pop()
            edges.append(Edge(stack[-1],point))

        if len(stack) < 2:
            edges.append(Edge(stack[-1],point))
            stack.append(point)
            return edges

        if (orient(stack[-2] ,stack[-1] , point ) == orient_):
            break
    edges.append(Edge(stack[-1],point))
    stack.append(point)
    return edges


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
            top = stack_[-1]
            while len(stack_) > 1 and orient(curr_point, stack_[-1], stack_[-2]) == TURN_LEFT:
                edges.append(Edge(curr_point, stack_[-2]))
                stack_.pop()
            stack_.append(curr_point)
        i += 1

    return triangles, edges


def built_curv_from_points(points):
    '''
    this function take input a list of points and constracts acurn made of Edges
    :param points: List of pionts
    :return: List of Edges
    '''
    curv = []
    for i in range(0, len(points) -1):
        curv.append(Edge(points[i] , points[i+1]))
    return curv


def compute_route(triangles, points):
    '''
    this function takes a path from pointes and a triangel list
    and return a list of edges the path passes through
    :param triangles:
    :param points:
    :return: Edges
    '''
    path = []
    curv = built_curv_from_points(points)
    for triangle in triangles:
        if triangle.is_point_inside(curv[0].p1):
            working_triangel = triangle
            break


    for path_edge in curv:
        while not working_triangel.is_point_inside(path_edge.p2):
            print("working triangel = " + str(working_triangel))
            edges = working_triangel.get_intersecting_edges(path_edge)
            if len(edges) < 2 :
                if working_triangel.is_point_inside(path_edge.p1):
                    out_edge = edges[0]
            else:
                if edges[0] == path[-1]:
                    out_edge = edges[1]
                else:
                    out_edge = edges[0]

            for triangle in triangles:  #shloud be done more efisiantly
                if out_edge in triangle.edges and not triangle == working_triangel:
                    working_triangel = triangle
                    break

            path.append(out_edge)


    return path




def reduce_edges(edges):
    pass


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

def test_graham_scan():


    # construct a test data-set
    points = []
    for i in range(10):
        points.append(Point(randint(0, 30), randint(0, 30)))
    points = sort_points(points)

    print("points")
    print(points)

    convex_hull = graham_scan(points)

    print(convex_hull)

    px = [point.x for point in points]
    py = [point.y for point in points]
    cx = [point.x for point in convex_hull]
    cy = [point.y for point in convex_hull]

    plt.scatter(px, py, c='b')
    plt.scatter(cx, cy, c='r')
    plt.gca().add_patch(plt.Polygon([point.vec for point in convex_hull], fill=False, ls='-'))
    plt.show()


def test_triangulation():


    # construct a test data-set
    points = []
    for i in range(10):
        points.append(Point(randint(0, 20), randint(0, 20)))

    points = [
        Point(2, 10),
        Point(4, 5),
        Point(10, 3),
        Point(15, 5),
        Point(10, 8),
        Point(11, 9),
        Point(13, 10),
        Point(16, 14)
    ]

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

    fig , ax0 = plt.subplots(1)

    x = [point.x for point in points]
    y = [point.y for point in points]
    ax0.scatter(x, y, s=20, color='b')

    for edge in edges:
        ax0.plot([edge.p1.x , edge.p2.x] , [edge.p1.y, edge.p2.y])

    #print("Triangles:")
    #for t in triangles:
    #    print(t)
    #    plt.gca().add_patch(plt.Polygon(t.vec, fill=False, ls='-'))

    plt.show()

def test_compute_route():

    obstical_points = [Point(1,0),Point(3,2),Point(5,7),Point(6,12),Point(8,4),Point(9,13),Point(11,19),Point(12,9),Point(15,3)]

    px = [point.x for point in obstical_points]
    py = [point.y for point in obstical_points]

    edges = [Edge(obstical_points[0],obstical_points[1]) ,
             Edge(obstical_points[0],obstical_points[2]) ,
             Edge(obstical_points[0],obstical_points[3]) ,
             Edge(obstical_points[1],obstical_points[2]) ,
             Edge(obstical_points[2],obstical_points[3]) ,
             Edge(obstical_points[1],obstical_points[4]) ,
             Edge(obstical_points[2],obstical_points[4]) ,
             Edge(obstical_points[4],obstical_points[5]) ,
             Edge(obstical_points[4],obstical_points[6]) ,
             Edge(obstical_points[4],obstical_points[7]) ,
             Edge(obstical_points[4],obstical_points[8]) ,
             Edge(obstical_points[2],obstical_points[5]) ,
             Edge(obstical_points[3],obstical_points[5]) ,
             Edge(obstical_points[5],obstical_points[6]) ,
             Edge(obstical_points[6],obstical_points[7]) ,
             Edge(obstical_points[7],obstical_points[8]) ,
             Edge(obstical_points[0],obstical_points[4]) ,
             Edge(obstical_points[0],obstical_points[8]) ,
             Edge(obstical_points[3],obstical_points[6]) ,
             Edge(obstical_points[6],obstical_points[8]) ,]


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
                if edge == Edge(p1,p2):
                   triangel = Triangle(point,p1,p2)
                   if triangel not in triangels and triangel.no_point_inside(obstical_points):
                        triangels.append(triangel)


    curv = [Point(1.5,0.3) , Point(10,8.6) , Point(11.3,2.5)]

    rout = compute_route(triangels, curv)
    print (rout)

    fig , ax0 = plt.subplots(1)
    ax0.scatter(px, py, c='b')
    for edge in edges:
        ax0.plot([edge.p1.x , edge.p2.x] , [edge.p1.y, edge.p2.y])

    cpx = [point.x for point in curv]
    cpy = [point.y for point in curv]

    ax0.plot(cpx, cpy)
    plt.show()

# test_sort_points()

test_triangulation()

#test_graham_scan()
#test_compute_route()
