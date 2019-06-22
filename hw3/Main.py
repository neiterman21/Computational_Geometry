from hw3.geolib.DataPreprocessing import get_input, plot_state
from hw3.geolib.Algorithms import triangulate, make_curve, compute_route, reduce_route


def main():

    obstacle_points, curve_points, plot = get_input()
    route = []

    print("obstacle_points = " + str(obstacle_points))
    print("curve_points = " + str(obstacle_points))

    triangles, edges = triangulate(obstacle_points)

    route = compute_route(triangles, make_curve(curve_points))
    print("route = " + str(route))

    route = reduce_route(route)
    print("reduced routes = " + str(route))

    if plot:
        plot_state(obstacle_points, curve_points, triangles, route)


if __name__ == "__main__":
    main()