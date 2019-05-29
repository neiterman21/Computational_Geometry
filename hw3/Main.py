def main():
    from geolib.DataPreprocessing import get_input, plot_state
    obstacle_points, curve_points, plot = get_input()
    if plot:
        plot_state(obstacle_points, curve_points)


if __name__ == "__main__":
    main()