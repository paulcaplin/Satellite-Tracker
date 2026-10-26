"""Draw the satellite's ground position on a 2D world map."""

from datetime import timezone

import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def create_satellite_map(latitude, longitude, altitude_km, at_time, name="ISS"):
    """Return a Matplotlib figure; map x is longitude and map y is latitude."""
    projection = ccrs.PlateCarree()
    figure = plt.figure(figsize=(13, 7.5), facecolor="#f4f6f8")
    axes = figure.add_subplot(111, projection=projection)
    figure.subplots_adjust(left=0.06, right=0.95, bottom=0.12, top=0.82)
    axes.set_global()
    # Cartopy bundles this Natural Earth image, so no map download is needed.
    axes.stock_img()

    grid = axes.gridlines(
        draw_labels=True,
        xlocs=range(-180, 181, 60),
        ylocs=range(-90, 91, 30),
        linewidth=0.6,
        color="#334155",
        alpha=0.35,
        linestyle="--",
    )
    grid.top_labels = False
    grid.right_labels = False
    grid.xlabel_style = {"size": 9, "color": "#334155"}
    grid.ylabel_style = {"size": 9, "color": "#334155"}

    axes.scatter(
        longitude, latitude, s=300, color="#ef4444", alpha=0.25,
        edgecolors="none", transform=projection, zorder=5,
    )
    axes.scatter(
        longitude, latitude, s=85, color="#dc2626", edgecolors="white",
        linewidths=1.5, transform=projection, zorder=6,
        label=f"{name} ground position",
    )
    axes.legend(loc="lower left", framealpha=0.95, fontsize=10)

    north_south = "N" if latitude >= 0 else "S"
    east_west = "E" if longitude >= 0 else "W"
    figure.suptitle(
        f"{name} | Current satellite position",
        x=0.06, y=0.96, ha="left", fontsize=21, fontweight="bold", color="#0f172a",
    )
    figure.text(
        0.06, 0.875,
        f"Latitude  {abs(latitude):.4f}° {north_south}     "
        f"Longitude  {abs(longitude):.4f}° {east_west}     "
        f"Altitude  {altitude_km:.1f} km",
        fontsize=12, color="#334155",
    )
    utc = at_time.astimezone(timezone.utc)
    figure.text(
        0.06, 0.035,
        f"Position at {utc:%Y-%m-%d %H:%M:%S} UTC  |  "
        "Marker shows the point on Earth directly below the satellite.",
        fontsize=10, color="#475569",
    )
    return figure
