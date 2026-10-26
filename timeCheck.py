from datetime import datetime, timezone, timedelta
from pathlib import Path

TLE_FILE = Path(__file__).resolve().parent / "Data" / "satellite_data.txt"
WAIT_TIME = timedelta(hours=2)


def safe_to_download() -> bool:
    if not TLE_FILE.exists():
        print("TLE file does not exist. Safe to download.")
        return True

    lines = TLE_FILE.read_text().splitlines()

    if not lines:
        raise ValueError("TLE file is empty.")

    saved_time = datetime.fromisoformat(lines[-1].strip())

    # Make sure both times are timezone-aware and in UTC.
    saved_time = saved_time.astimezone(timezone.utc)
    current_time = datetime.now(timezone.utc)

    elapsed_time = current_time - saved_time

    print(f"TLE saved at: {saved_time}")
    print(f"Current time: {current_time}")
    print(f"Time elapsed: {elapsed_time}")

    if elapsed_time >= WAIT_TIME:
        print("Safe to download a new TLE.")
        return True

    remaining_time = WAIT_TIME - elapsed_time
    print(f"Wait {remaining_time} before downloading again.")
    return False


# if safe_to_download():
#     print("Download code can run here.")
# else:
#     print("Use the existing TLE data.")
