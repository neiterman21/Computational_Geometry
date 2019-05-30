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
