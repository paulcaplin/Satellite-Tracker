import requests
from datetime import datetime, timezone
import timeCheck as tC
# IMPORT LIVE ISS TLE using CelesTrak

ISS = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"

# write the time down when accessed.
if tC.safe_to_download():
    response = requests.get(ISS)
    response.raise_for_status()

    lines = response.text.strip().splitlines()

    name = lines[0]
    line1 = lines[1]
    line2 = lines[2]

    # write the time down when accessed.
    now = datetime.now(timezone.utc)
    now_string = str(now)

    with open("Data/satellite_data.txt", "w") as f:
        f.write(name + "\n")
        f.write(line1 + "\n")
        f.write(line2 + "\n")
        f.write(now_string)

else:
    print("TLE is less than two hours old. Using existing data.")


