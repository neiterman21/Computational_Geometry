# Chan's Convex Hull O(n log h) - Tom Switzer <thomas.switzer@gmail.com>
import sys
import numpy as np
from matplotlib import pyplot as plt

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

def turn(p, q, r):
    """Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
    return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

def _rtangent(hull, p):
    """Return the index of the point in hull that the right tangent line from p
    to hull touches.
    """
    l, r = 0, len(hull)
    l_prev = turn(p, hull[0], hull[-1])
    l_next = turn(p, hull[0], hull[(l + 1) % r])
    while l < r:
        c = (l + r) / 2
        c_prev = turn(p, hull[c], hull[(c - 1) % len(hull)])
        c_next = turn(p, hull[c], hull[(c + 1) % len(hull)])
        c_side = turn(p, hull[l], hull[c])
        if c_prev != TURN_RIGHT and c_next != TURN_RIGHT:
            return c
        elif c_side == TURN_LEFT and (l_next == TURN_RIGHT or
                                      l_prev == l_next) or \
                c_side == TURN_RIGHT and c_prev == TURN_RIGHT:
            r = c               # Tangent touches left chain
        else:
            l = c + 1           # Tangent touches right chain
            l_prev = -c_next    # Switch sides
            l_next = turn(p, hull[l], hull[(l + 1) % len(hull)])
    return l

def pars_args():
    if len(sys.argv) <= 1:
        print ("There are too few arguments")
        exit(1)
    lines = open(sys.argv[1],"r").readlines()
    merged_line = ""
    for line in lines:
        merged_line = merged_line + line
    merged_line = merged_line.replace('\n'," ").replace('\r',"").replace('\t',"").replace('  '," ")
    raw_num_arr = merged_line.strip("\n").split(" ")
    print(merged_line)
    hull = []
    for i in range(int(raw_num_arr[0])):
        print(raw_num_arr[2*i + 1], raw_num_arr[2*i+2])
        hull.append([int(raw_num_arr[2*i + 1]) , int(raw_num_arr[2*i+2])])
    q = [int(raw_num_arr[-3]), int(raw_num_arr[-2])] 

    return hull , q

def main():
    hull , q = pars_args()
    index = _rtangent(hull , q)
    print(index)
    hull.append(q)
    data = np.array(hull)
    x, y = data.T
    plt.scatter(x,y)
    plt.plot([q[0],hull[index][0] ],[q[1], hull[index][1]] , 'k-')
    plt.show()

if __name__ == "__main__":
    main()
    raw_input()
