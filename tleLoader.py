import requests
from datetime import datetime, timezone
import timeCheck as tC

ISS = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"


def get_tle_lines(*, offline=False):
    if not offline and tC.safe_to_download():
        response = requests.get(ISS, timeout=15)
        response.raise_for_status()

        lines = response.text.strip().splitlines()

        name = lines[0]
        line1 = lines[1]
        line2 = lines[2]

        now_string = str(datetime.now(timezone.utc))

        tC.TLE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with tC.TLE_FILE.open("w") as f:
            f.write(name + "\n")
            f.write(line1 + "\n")
            f.write(line2 + "\n")
            f.write(now_string + "\n")

        print("Downloaded a new TLE.")
    else:
        print("Using the existing TLE.")

    with tC.TLE_FILE.open("r") as f:
        lines = f.read().splitlines()

    return lines[1], lines[2]
