from datetime import datetime, timedelta, timezone
from math import sqrt

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
from pyproj import Transformer
from skyfield.api import EarthSatellite, load, wgs84

import main
from coordinates import (
    WGS84_FLATTENING,
    WGS84_RADIUS_KM,
    ecef_to_geodetic,
    julian_date,
    position_to_geodetic,
    teme_to_ecef,
)
from satellite_map import create_satellite_map
from tracker import calculate_position

# Fixed inputs keep these checks reproducible and independent of the TLE cache.
LINE1 = "1 25544U 98067A   26299.20906838  .00006121  00000+0  11890-3 0  9995"
LINE2 = "2 25544  51.6337  11.7282 0006920 310.9581  49.0809 15.49059765592065"
AT_TIME = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
POLAR_RADIUS_KM = WGS84_RADIUS_KM * (1 - WGS84_FLATTENING)


@pytest.mark.parametrize("position, expected", [
    ((WGS84_RADIUS_KM, 0, 0), (0, 0, 0)),
    ((0, WGS84_RADIUS_KM, 0), (0, 90, 0)),
    ((0, -WGS84_RADIUS_KM, 0), (0, -90, 0)),
    ((-WGS84_RADIUS_KM, 0, 0), (0, -180, 0)),
    ((0, 0, POLAR_RADIUS_KM), (90, 0, 0)),
    ((0, 0, -POLAR_RADIUS_KM - 400), (-90, 0, 400)),
    ((WGS84_RADIUS_KM + 400, 0, 0), (0, 0, 400)),
])
def test_known_earth_coordinates(position, expected):
    assert ecef_to_geodetic(position) == pytest.approx(expected, abs=1e-8)


@pytest.mark.parametrize("position", [
    (-2700, -4300, 3850),
    (1000, 2000, -6300),
    (-1, 1, 6800),
])
def test_geodetic_conversion_against_proj(position):
    transform = Transformer.from_crs("EPSG:4978", "EPSG:4979", always_xy=True)
    lon, lat, altitude_m = transform.transform(*(value * 1000 for value in position))
    assert ecef_to_geodetic(position) == pytest.approx(
        (lat, lon, altitude_m / 1000), abs=1e-5,
    )


def test_rotation_at_j2000_and_preserved_radius():
    at_time = datetime(2000, 1, 1, 12, tzinfo=timezone.utc)
    # GMST at J2000 is 280.460618375 degrees; rotate TEME by its negative.
    assert teme_to_ecef((1, 0, 0), at_time) == pytest.approx(
        (0.1815596529, 0.9833799329, 0), abs=1e-9,
    )
    original = (2000, -5000, 3800)
    rotated = teme_to_ecef(original, AT_TIME)
    assert sqrt(sum(v * v for v in rotated)) == pytest.approx(
        sqrt(sum(v * v for v in original)), abs=1e-9,
    )


def test_equivalent_timezones_produce_same_position():
    local_time = AT_TIME.astimezone(timezone(timedelta(hours=-5)))
    assert julian_date(local_time) == julian_date(AT_TIME)
    assert calculate_position(LINE1, LINE2, local_time) == calculate_position(
        LINE1, LINE2, AT_TIME,
    )


def test_reject_naive_time():
    with pytest.raises(ValueError, match="timezone-aware"):
        calculate_position(LINE1, LINE2, datetime(2026, 10, 26))


@pytest.mark.parametrize("position", [(0, 0, 0), (float("nan"), 1, 2), (1, float("inf"), 2)])
def test_reject_invalid_geodetic_position(position):
    with pytest.raises(ValueError):
        ecef_to_geodetic(position)


@pytest.mark.parametrize("hour", [0, 6, 12, 18])
def test_satellite_coordinates_against_skyfield(hour):
    at_time = AT_TIME.replace(hour=hour)
    timescale = load.timescale(builtin=True)
    satellite = EarthSatellite(LINE1, LINE2, "ISS", timescale)
    reference = wgs84.geographic_position_of(satellite.at(timescale.from_datetime(at_time)))

    error, position, _ = calculate_position(LINE1, LINE2, at_time)
    assert error == 0
    latitude, longitude, altitude = position_to_geodetic(position, at_time)
    assert latitude == pytest.approx(reference.latitude.degrees, abs=0.0001)
    longitude_error = (longitude - reference.longitude.degrees + 180) % 360 - 180
    # UTC approximates UT1; allow its sub-second Earth-rotation difference.
    assert abs(longitude_error) < 0.005
    assert altitude == pytest.approx(reference.elevation.km, abs=0.001)
    assert -180 <= longitude < 180


@pytest.mark.parametrize("latitude, longitude", [(35.5, -97.2), (-50, 179.9), (51, -179.9)])
def test_map_renders_with_longitude_on_x_axis(tmp_path, latitude, longitude):
    figure = create_satellite_map(latitude, longitude, 420, AT_TIME)
    try:
        assert tuple(figure.axes[0].collections[-1].get_offsets()[0]) == (longitude, latitude)
        output = tmp_path / "map.png"
        figure.savefig(output)
        assert output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    finally:
        plt.close(figure)


def test_main_saves_map_without_window(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(main, "get_tle_lines", lambda **kwargs: (LINE1, LINE2))
    output = tmp_path / "iss.png"
    main.main(["--offline", "--no-show", "--save", str(output)])
    console = capsys.readouterr().out
    assert "Latitude:" in console
    assert "Longitude:" in console
    assert "Altitude (WGS84):" in console
    assert output.is_file()


def test_main_stops_on_sgp4_error(monkeypatch):
    monkeypatch.setattr(main, "get_tle_lines", lambda **kwargs: (LINE1, LINE2))
    monkeypatch.setattr(main, "calculate_position", lambda *args: (6, (0, 0, 0), (0, 0, 0)))
    with pytest.raises(RuntimeError, match="SGP4 failed with error code 6"):
        main.main(["--offline", "--no-show"])
