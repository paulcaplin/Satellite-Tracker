from datetime import datetime, timezone
from sgp4.api import Satrec

from coordinates import julian_date


def calculate_position(line1, line2, at_time=None):
    """Return SGP4's error code, TEME position (km), and velocity (km/s)."""
    sat = Satrec.twoline2rv(line1, line2)

    if at_time is None:
        at_time = datetime.now(timezone.utc)
    jd, fr = julian_date(at_time)

    result = sat.sgp4(jd, fr)

    return result
