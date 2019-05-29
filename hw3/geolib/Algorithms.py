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


def triangulate(points):
    """
    This function takes as input a list of Points.
    :param points: List of points.
    :return: List of triangles.
    """
    pass


def compute_route(triangles, points):
    pass


def reduce_edges(edges):
    pass


