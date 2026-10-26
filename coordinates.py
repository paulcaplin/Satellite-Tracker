"""Convert SGP4 TEME positions in kilometers to WGS84 ground coordinates."""

from datetime import timezone
from math import atan2, copysign, cos, degrees, hypot, isfinite, sin, sqrt

from sgp4.api import jday
from sgp4.propagation import gstime

WGS84_RADIUS_KM = 6378.137
WGS84_FLATTENING = 1 / 298.257223563
WGS84_ECCENTRICITY_SQUARED = WGS84_FLATTENING * (2 - WGS84_FLATTENING)


def julian_date(at_time):
    """Convert a timezone-aware datetime to the two-part UTC Julian date."""
    if at_time.utcoffset() is None:
        raise ValueError("Use a timezone-aware datetime for the satellite position.")
    utc = at_time.astimezone(timezone.utc)
    return jday(
        utc.year, utc.month, utc.day, utc.hour, utc.minute,
        utc.second + utc.microsecond / 1e6,
    )


def _position_components(position):
    x, y, z = position
    if not all(isfinite(value) for value in (x, y, z)):
        raise ValueError("Position coordinates must be finite numbers in kilometers.")
    return x, y, z


def teme_to_ecef(position, at_time):
    """Rotate a TEME position into Earth's rotating frame at the given time.

    This map-level approximation uses UTC in place of UT1 and ignores polar
    motion. The position and at_time must describe the same instant.
    """
    x, y, z = _position_components(position)
    jd, fraction = julian_date(at_time)
    angle = gstime(jd + fraction)  # Greenwich mean sidereal time, in radians.

    return (
        cos(angle) * x + sin(angle) * y,
        -sin(angle) * x + cos(angle) * y,
        z,
    )


def ecef_to_geodetic(position):
    """Return WGS84 (latitude degrees, longitude degrees, altitude km).

    Latitude is geodetic, positive north; longitude is positive east and is
    normalized to [-180, 180). Altitude is above the WGS84 ellipsoid.
    """
    x, y, z = _position_components(position)
    horizontal = hypot(x, y)
    if horizontal < 1e-12:
        if z == 0:
            raise ValueError("Latitude and longitude are undefined at Earth's center.")
        polar_radius = WGS84_RADIUS_KM * (1 - WGS84_FLATTENING)
        # Longitude is arbitrary at a pole; use zero consistently.
        return copysign(90.0, z), 0.0, abs(z) - polar_radius

    e2 = WGS84_ECCENTRICITY_SQUARED
    latitude = atan2(z, horizontal * (1 - e2))
    for _ in range(15):
        normal_radius = WGS84_RADIUS_KM / sqrt(1 - e2 * sin(latitude) ** 2)
        updated = atan2(z + e2 * normal_radius * sin(latitude), horizontal)
        if abs(updated - latitude) < 1e-12:
            latitude = updated
            break
        latitude = updated

    longitude = (degrees(atan2(y, x)) + 180) % 360 - 180
    # This form avoids division by cos(latitude) near the poles.
    altitude = (
        horizontal * cos(latitude) + z * sin(latitude)
        - WGS84_RADIUS_KM * sqrt(1 - e2 * sin(latitude) ** 2)
    )
    return degrees(latitude), longitude, altitude


def position_to_geodetic(position, at_time):
    """Convert a TEME position to (latitude degrees, longitude degrees, altitude km)."""
    return ecef_to_geodetic(teme_to_ecef(position, at_time))
