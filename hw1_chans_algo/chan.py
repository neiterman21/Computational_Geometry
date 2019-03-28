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

def naive_solution(hull, query_point):
    """ Naive solution, works in O(n^2), we go counterclock-wise and check that 
    all of the points are from the left of the tangent. """
    size = len(hull)
    for i in range(0, size):
        next_i = (i + 1) % size
        counter_left = 0
        counter_right = 0
        for j in range(0, size):
            if orient(query_point, hull[i], hull[j]) in [TURN_LEFT]:
                counter_left += 1
        if counter_left >= size - 1:
            return i
    return None

def naive_solution_2(hull, query_point):
    """ Naive solution, works in O(n)"""
    size = len(hull)
    for i in range(0, size):
        next_i = (i + 1) % size
        prev_i = (i - 1) % size
        if orient(query_point, hull[i], hull[next_i]) in [TURN_LEFT, TURN_NONE] and \
            orient(query_point, hull[i], hull[prev_i]) in [TURN_LEFT, TURN_NONE]:
                return i
    return None

def rtangent(hull, p):
    """Return the index of the point in hull that the right tangent line from p
    to hull touches.
    """
    l, r = 0, len(hull)
    l_prev = orient(p, hull[0], hull[-1])
    l_next = orient(p, hull[0], hull[(l + 1) % r])
    while l < r:
        c = int((l + r) / 2)
        c_prev = orient(p, hull[c], hull[(c - 1) % len(hull)])
        c_next = orient(p, hull[c], hull[(c + 1) % len(hull)])
        c_side = orient(p, hull[l], hull[c])
        if c_prev != TURN_RIGHT and c_next != TURN_RIGHT:
            return c
        elif c_side == TURN_LEFT and (l_next == TURN_RIGHT or
                                      l_prev == l_next) or \
                c_side == TURN_RIGHT and c_prev == TURN_RIGHT:
            r = c               # Tangent touches left chain
        else:
            l = c + 1           # Tangent touches right chain
            l_prev = -c_next    # Switch sides
            l_next = orient(p, hull[l], hull[(l + 1) % len(hull)])
    return l


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
    error_msg(len(sys.argv) <= 1, "No input file was supplied. ")

    # Verify the the filename is legal and open operation is done. 
    try:    lines = open(sys.argv[1],"r").readlines()
    except: error_msg(True, "Could not file {}".format(sys.argv[1]))
    
    # Verify that file contains at least 3 lines.
    error_msg(len(lines) < 3, "The supplied input file has an illegal format")
    
    # Construct data
    total_number_of_points = line2numbers(lines[0])[0]

    line_ = ""
    for line in lines[1: -1]:   line_ += line.strip("\n")
    points = numbers2points(line2numbers(line_))
    # print(points)

    query_point = line2numbers(lines[-1])

    # Verify the content of the file.
    error_msg(total_number_of_points != len(points), 
                                "The supplied input file has an illegal format")
    error_msg(len(query_point) <= 1,
                                "The supplied input file has an illegal format")
    
    # Check if user wants to plot the data on the screen.
    plot = False
    try:    plot = sys.argv[2] == 'plot'
    except: pass         

    return total_number_of_points, points, query_point, plot

def plot_state(points, query_point, tangent_point):
    """ Shows the convex hull and the query point on the screen. """ 
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    x.append(points[0][0])
    y.append(points[0][1])
    plt.scatter(x, y);
    plt.plot(x, y, 'ro-')
    if tangent_point:    
        plt.plot([query_point[0], tangent_point[0]], 
                 [query_point[1], tangent_point[1]], 'bo-')
    else:
        plt.plot(query_point[0], query_point[1], 'bo')
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
    tnp, points , query_point, plot = get_input()
    index = rtangent(points, query_point)

    if plot:    plot_state(points, query_point, points[index])
    print("Index: " + str(index))
    print("Tangent point: " + str(points[index]));


def orient_test_1():
    p1 = [0, 0]
    p2 = [1, 1]
    p3 = [1, 2]
    p4 = [2, 2]
    p5 = [1, -2]

    assert(orient(p1, p2, p3) == 1)
    assert(orient(p1, p2, p4) == 0)
    assert(orient(p1, p2, p5) == -1)

def rtangent_vs_naive():
    tnp, points , query_point, plot = get_input()
    index1  = naive_solution(points, query_point)
    index2  = rtangent(points, query_point)
    assert(index1 == index2)
    assert(points[index1] == points[index2])

def rtangent_vs_naive_2():
    tnp, points , query_point, plot = get_input()
    index1 = naive_solution_2(points, query_point)
    index2 = rtangent(points, query_point)
    assert(index1 == index2)
    assert(points[index1] == points[index2])

def test_naive():
    tnp, points , query_point, plot = get_input()
    index = naive_solution(points, query_point)
    if plot:    plot_state(points, query_point, points[index])
    print("index: " + str(index));
    print("point: " + str(points[index]));

def test_naive_2():
    tnp, points , query_point, plot = get_input()
    index = naive_solution_2(points, query_point)
    if plot:    plot_state(points, query_point, points[index])
    print("index: " + str(index));
    print("point: " + str(points[index]));

def test_rtangent():
    tnp, points , query_point, plot = get_input()
    index = points[rtangent(points, query_point)]
    if plot:    plot_state(points, query_point, points[index])
    print("index: " + str(index));
    print("point: " + str(points[index]));

if __name__ == "__main__":
    # orient_test_1()
    # test_naive()
    # test_naive_2()
    # rtangent_vs_naive()
    # rtangent_vs_naive_2()
    main()

