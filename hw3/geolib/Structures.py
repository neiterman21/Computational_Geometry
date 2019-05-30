from numpy import dot, array, arccos
from numpy.linalg import norm

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vec = array([x, y])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __str__(self):
        return repr(self)

    @staticmethod
    def less(p1, p2):
        return p1.x < p2.x or (p1.x == p2.x and p1.y < p2.y)

    @staticmethod
    def less_radial(axis_point):
        def less(p1, p2):
            u = p1.vec - axis_point.vec
            v = p2.vec - axis_point.vec
            axis = array([0, -1])

            alpha1 = arccos(dot(u, axis)/norm(u)/norm(axis))
            alpha2 = arccos(dot(v, axis)/norm(v)/norm(axis))

            if alpha1 < alpha2:
                return True
            elif alpha1 == alpha2:
                return norm(u) < norm(v)
            return False
        return less


class Edge:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.left_adj_triangle = None       # The direction is p1p2
        self.right_adj_triangle = None

    def __eq__(self, other):
        return (self.p1 == other.p1 and self.p2 == other.p2) \
               or (self.p2 == other.p1 and self.p1 == other.p2)

    def __ne__(self, other):
        return not self == other

    def is_intersect(self, other):
        """
        :param other: Edge
        :return: True if and only if this and other edge has common point.
        """
        from geolib.Algorithms import orient
        test_orient_1 = \
            orient(self.p1, self.p2, other.p1) * -1 == orient(self.p1, self.p2, other.p2)
        test_orient_2 = \
            orient(other.p1, other.p2, self.p1) * -1 == orient(other.p1, other.p2, self.p2)
        return test_orient_1 and test_orient_2


class Triangle:

    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.edges = [Edge(p1, p2), Edge(p2, p3), Edge(p3, p1)]
        self.adj_triangles = []
        self.vec = [p1.vec, p2.vec, p3.vec]

    def is_point_inside(self, q):
        """
        This function queries whether the point inside the triangle.
        :param q: Point
        :return: True if and only if the point inside the triangle.
        """
        from geolib.Algorithms import orient
        return orient(self.p1, self.p2, q) == orient(self.p2, self.p3, q) == orient(self.p3, self.p1, q)

    def __eq__(self, other):
        vx = [self.p1, self.p2, self.p3]
        return other.p1 in vx and other.p2 in vx and other.p3 in vx

    def get_intersecting_edges(self, edge):
        """
        This function takes outer edge/line as an input and it returns all triangle edges it
        intersects with.
        :param edge: Edge
        :return: List of all edges in triangle such that the intersection of edge and the edges
        inside the list is not empty.
        """
        result = []
        for edge_ in self.edges:
            if edge.is_intersect(edge_):
                result.append(edge_)
        return result

    def __repr__(self):
        return 'Triangle[' + str(self.p1) + ", " + str(self.p2) + ", " + str(self.p3) + ']'

    def __str__(self):
        return repr(self)


def test():
    less_comparator = Point.less_radial(Point(1, 2))
    p1 = Point(3,5)
    p2 = Point(5,3)
    p3 = Point(10, 6)

    print(less_comparator(p1, p2))
    print(less_comparator(p2, p3))


test()
