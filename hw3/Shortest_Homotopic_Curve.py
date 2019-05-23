import sys
from matplotlib import pyplot as plt

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

# # python3.5 does not supports CMP function.
# def turn(p, q, r):
#     """Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
#     return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

def orient(p, q, r):
    """Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
    qr = q[0] * r[1] - q[1] * r[0]
    pr = p[0] * r[1] - p[1] * r[0]
    pq = p[0] * q[1] - p[1] * q[0]
    det = qr - pr + pq
    if det > 0: return 1
    if det < 0: return -1
    return 0

def line2numbers(line):
    """ Function takes string line and converts it into list of integers. """
    l = [x for x in line.strip("\n").split(" ")]
    l = filter_(l, lambda a: a != '')
    l = map_(l, lambda a: int(a))
    return l

def numbers2points(numbers):
    """ It converts list of integer numbers to list of 2d points. """
    error_msg(len(numbers) % 2 == 1, "An odd number of numbers was supplied" + 
                                                  " cannot construct the hull.")
    return [[numbers[i], numbers[i + 1]] for i in range(0, len(numbers), 2)]


def error_msg(condition, msg):
    """ Function checks the condition, and if it false then it prints relevant 
    error on the screen and exits the program. """
    if condition:
        print("Error: " + msg)
        exit(1)

def get_input():
    """ Responsible to verify the input of the program and retrieving an input
    information."""

    # Check the number of supplied arguments
   # error_msg(len(sys.argv) <= 1, "No input file was supplied. ")

    # Verify the the filename is legal and open operation is done. 
    try:    lines = open("input_example.txt","r").readlines()
    except: error_msg(True, "Could not file {}".format(sys.argv[1]))
    
    # Verify that file contains at least 3 lines.
    error_msg(len(lines) < 3, "The supplied input file has an illegal format")
    
    # Construct data
    total_number_of_obstical_points = line2numbers(lines[0])[0]

    line_ = ""
    for line in lines[1:2]:   line_ += line.strip("\n")
    obstical_points = numbers2points(line2numbers(line_))

    total_number_of_poligon_points = line2numbers(lines[2])[0]
    line_ = ""
    for line in lines[3:]:   line_ += line.strip("\n")
    poligon_points = numbers2points(line2numbers(line_))

    # Verify the content of the file.
    #cerror_msg(total_number_of_points != len(points), 
    #                            "The supplied input file has an illegal format")
    #error_msg(len(query_point) <= 1,
    #                            "The supplied input file has an illegal format")
    
    # Check if user wants to plot the data on the screen.
    plot = True
   # try:    plot = sys.argv[2] == 'plot'
   # except: pass         

    return total_number_of_poligon_points, poligon_points,total_number_of_obstical_points ,obstical_points, plot

def plot_state(tnpp, ppoints , tnop, opointes):
    """ Shows the convex hull and the query point on the screen. """ 
    x = []
    y = []
    for point in ppoints:
        x.append(point[0])
        y.append(point[1])
    x.append(ppoints[0][0])
    y.append(ppoints[0][1])
    plt.scatter(x, y);
    plt.plot(x, y, 'ro-')

    x = []
    y = []
    for point in opointes:
        x.append(point[0])
        y.append(point[1])
    plt.scatter(x, y);
    plt.plot(x, y , 'bo')

#    if tangent_point:    
#        plt.plot([query_point[0], tangent_point[0]], 
#                 [query_point[1], tangent_point[1]], 'bo-')
#    else:
#        plt.plot(query_point[0], query_point[1], 'bo')

    plt.show()

def filter_(iterable, truthy):
    result = []
    for el in iterable:
        if(truthy(el)):
            result.append(el)
    return result

def map_(iterable, operation):
    result = []
    for el in iterable:
        result.append(operation(el))
    return result

def main():
    tnpp, ppoints , tnop, opointes ,plot = get_input()
    #index = rtangent(points, query_point)

    if plot:    plot_state(tnpp, ppoints , tnop, opointes)
    print("Index: " + str(index))
    print("Tangent point: " + str(points[index]));

def convex_hull(points):
    """Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list. 
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    
    main()

