from numpy import dot, array, arccos
from numpy.linalg import norm
from hw3.geolib.FunctionaHelpers import orient, point_on_line


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vec = array([x, y])
        self.label = 'None'
        self.triangle_ = None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"

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

            alpha1 = arccos(dot(u, axis) / norm(u) / norm(axis))
            alpha2 = arccos(dot(v, axis) / norm(v) / norm(axis))

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
        self.twin = None
        self.label = str([self.p1.label, self.p2.label])

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
        if point_on_line(self.p1, self.p2, other.p1) or \
                point_on_line(self.p1, self.p2, other.p2) or \
                point_on_line(other.p1, other.p2, self.p1) or \
                point_on_line(other.p1, other.p2, self.p1):
            return True

        test_orient_1 = orient(self.p1, self.p2, other.p1) * -1 == orient(self.p1, self.p2, other.p2)
        test_orient_2 = orient(other.p1, other.p2, self.p1) * -1 == orient(other.p1, other.p2, self.p2)

        return test_orient_1 and test_orient_2

    def __repr__(self):
        if self.p1.label == 'None' or self.p2.label == 'None':
            return 'Edge[' + str(self.p1) + ", " + str(self.p2) + ']'
        return str(self.label)

    def __str__(self):
        return repr(self)

    @staticmethod
    def create_edge(p1, p2):
        e = Edge(p1, p2)
        e_twin = Edge(p2, p1)
        e.twin = e_twin
        e_twin.twin = e
        return e


class Triangle:

    def __init__(self, e1, e2, e3):
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.p1 = self.e1.p1
        self.p2 = self.e2.p1
        self.p3 = self.e3.p1
        self.adj_triangles = [None, None, None]
        self.edges = [self.e1, self.e2, self.e3]
        self.points = [self.p1, self.p2, self.p3]
        self.label = str([self.p1.label, self.p2.label, self.p3.label])
        self.points_vec = [self.p1.vec, self.p2.vec, self.p3.vec]

    def is_point_inside(self, q):
        """
        This function queries whether the point inside the triangle.
        :param q: Point
        :return: True if and only if the point inside the triangle.
        """

        return orient(self.p1, self.p2, q) == orient(self.p2, self.p3, q) == orient(self.p3, self.p1, q)

    def is_edge_inside(self, e):
        return self.is_point_inside(e.p1) and self.is_point_inside(e.p2)

    def get_intersecting_edges_indices(self, edge):
        result = []
        for i in [0, 1, 2]:
            if edge.is_intersect(self.edges[i]):
                result.append(i)
        return result

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

    def __eq__(self, other):
        return other.p1 in self.points and other.p2 in self.points and other.p3 in self.points

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self.label

    def __str__(self):
        return repr(self)

    @staticmethod
    def set_adj_triangles(t1, t2):
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if t1.edges[i] == t2.edges[j]:
                    t1.adj_triangles[i] = t2
                    t2.adj_triangles[j] = t1
                    return


def test():
    p1 = Point(0, 0)
    p2 = Point(4, 4)
    p3 = Point(5, 5)

    print(orient(p1, p2, p3))


test()
