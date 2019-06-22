import numpy as np

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def extrema(iterable, key=None, comparator=None, type_='min'):

    if not key or not comparator:
        return iterable

    result = iterable[0]
    for item in iterable[1:]:
        if type_ == 'min' and comparator(key(item), key(result)):
            result = item
        elif type_ == 'max' and comparator(key(result), key(item)):
            result = item
    return result


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


def merge_sort(iterable, key=None, comparator=None):

    if not key or not comparator:
        return iterable

    if len(iterable) > 1:
        mid = len(iterable) // 2
        left_iterable = iterable[:mid]
        right_iterable = iterable[mid:]

        merge_sort(left_iterable, key, comparator)
        merge_sort(right_iterable, key, comparator)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(left_iterable) and j < len(right_iterable):
            if comparator(key(left_iterable[i]), key(right_iterable[j])):
                iterable[k] = left_iterable[i]
                i += 1
            else:
                iterable[k] = right_iterable[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left_iterable):
            iterable[k] = left_iterable[i]
            i += 1
            k += 1

        while j < len(right_iterable):
            iterable[k] = right_iterable[j]
            j += 1
            k += 1


def filter_(iterable, truthy):
    """
    Helper function. Functional programming - filter.
    :param iterable: Array to filter
    :param truthy: The condition to filter by.
    :return: New filtered array that contains elements that satisfy the truthy.
    """
    result = []
    for el in iterable:
        if truthy(el):
            result.append(el)
    return result


def map_(iterable, operation):
    """
    Helper function. Functional programming - map.
    :param iterable: Array to map to.
    :param operation: The operation that the map function should perform.
    :return: New array after the map operation.
    """
    result = []
    for el in iterable:
        result.append(operation(el))
    return result


def compute_big_rectangle(points):

    from hw3.geolib.Structures import Point
    from math import pi

    min_x = min(points, key=lambda point: point.x).x - pi/4
    min_y = min(points, key=lambda point: point.y).y - pi/4

    max_x = max(points, key=lambda point: point.x).x + pi/4
    max_y = max(points, key=lambda point: point.y).y + pi/4

    return [Point(min_x, min_y), Point(min_x, max_y), Point(max_x, min_y), Point(max_x, max_y)]


def point_on_line(e_start, e_end, p):
    if orient(e_start, e_end, p) == 0:
        v = np.subtract(p.vec, e_start.vec)
        u = np.subtract(e_end.vec, e_start.vec)
        if np.linalg.norm(v) < np.linalg.norm(u):
            return True
    return False

