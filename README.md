# Satellite tracker

Calculate the ISS position from a CelesTrak TLE, convert its TEME position to
WGS84 latitude/longitude, and display its ground position on a 2D world map.

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe main.py
```

The console prints the position, velocity, latitude, longitude, and altitude.
The map opens in a Matplotlib window. It is a snapshot at the UTC time shown;
run the program again for an updated position.

Save a map without opening a window:

```powershell
.\venv\Scripts\python.exe main.py --save satellite_map.png --no-show
```

Add `--offline` to use `Data/satellite_data.txt` without a network request.
Otherwise, the existing loader refreshes the TLE after two hours. The map uses
Cartopy's bundled Natural Earth background and needs no map tiles or API key.

## Coordinate conversion

- `tracker.py` propagates the TLE with SGP4 at a timezone-aware UTC instant.
- `coordinates.py` rotates TEME into an Earth-fixed frame using Greenwich mean
  sidereal time, then calculates geodetic latitude and altitude on WGS84.
- `satellite_map.py` plots longitude horizontally and latitude vertically in
  a Plate Carree projection. The marker is the ground point below the ISS.

Longitude is in `[-180, 180)`, positive east. Latitude is positive north.
Altitude is in kilometers above the WGS84 ellipsoid. The rotation approximates
UT1 with UTC and ignores polar motion, which is suitable for this world map
but is not a precision Earth-orientation transformation. Position accuracy also
depends on the age of the TLE.

References: [SGP4 reference frame](https://pypi.org/project/sgp4/),
[Skyfield satellite coordinates](https://rhodesmill.org/skyfield/earth-satellites.html),
[Cartopy map API](https://cartopy.readthedocs.io/stable/reference/generated/cartopy.mpl.geoaxes.GeoAxes.html).

## Checks

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\venv\Scripts\python.exe -m pytest -q
```

Tests check known Earth coordinates, longitude wrapping, Earth rotation,
agreement with Skyfield using a fixed TLE and UTC times, and map rendering.
