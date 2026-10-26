import argparse
from datetime import datetime, timezone
from pathlib import Path

from coordinates import position_to_geodetic
from tleLoader import get_tle_lines
from tracker import calculate_position


def main(argv=None):
    parser = argparse.ArgumentParser(description="Show the ISS on a 2D world map.")
    parser.add_argument("--save", type=Path, metavar="PATH", help="Save the map image.")
    parser.add_argument("--no-show", action="store_true", help="Skip opening the map window.")
    parser.add_argument("--offline", action="store_true", help="Use the cached TLE without downloading.")
    args = parser.parse_args(argv)

    if args.no_show:
        import matplotlib
        matplotlib.use("Agg")

    from satellite_map import create_satellite_map
    import matplotlib.pyplot as plt

    line1, line2 = get_tle_lines(offline=args.offline)

    # Use exactly the same instant for propagation and Earth's rotation.
    at_time = datetime.now(timezone.utc)
    error_code, position, velocity = calculate_position(line1, line2, at_time)

    if error_code != 0:
        raise RuntimeError(f"SGP4 failed with error code {error_code}")

    latitude, longitude, altitude = position_to_geodetic(position, at_time)
    print("Position (TEME, km):", position)
    print("Velocity (TEME, km/s):", velocity)
    print(f"Time (UTC): {at_time.isoformat()}")
    print(f"Latitude: {latitude:.6f} degrees (north positive)")
    print(f"Longitude: {longitude:.6f} degrees (east positive)")
    print(f"Altitude (WGS84): {altitude:.3f} km")

    figure = create_satellite_map(latitude, longitude, altitude, at_time)
    if args.save:
        figure.savefig(args.save, dpi=150, facecolor=figure.get_facecolor())
        print(f"Map saved to: {args.save.resolve()}")
    if not args.no_show:
        plt.show()
    plt.close(figure)


if __name__ == "__main__":
    main()
