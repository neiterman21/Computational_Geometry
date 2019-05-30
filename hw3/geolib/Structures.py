class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __str__(self):
        return repr(self)

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass


class Edge:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.left_adj_triangle = None       # The direction is p1p2
        self.right_adj_triangle = None

    def __eq__(self, other):
        return (self.p1 == other.p1 and self.p2 == other.p2) \
               or (self.p2 == other.p1 and self.p1 == other.p2)

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




