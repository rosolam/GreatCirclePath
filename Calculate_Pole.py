import numpy as np
from scipy.optimize import minimize, differential_evolution

# Earth's radius in kilometers
EARTH_RADIUS = 6371.0

# Ancient sites: (name, longitude, latitude)
ancient_sites = [
    ("Giza", 31.13, 29.98),
    ("Siwa", 25.519545, 29.203171),
    ("Tassili n'Ajjer", 8.3333, 25.1667),
    ("Paratoari", -71.4567, -12.6706),
    ("Ollantaytambo", -72.26333, -13.25806),
    ("Machu Picchu", -72.54, -13.16),
    ("Nazca", -75.13, -14.69),
    ("Easter Island", -109.35, -27.11),
    ("Aneityum Island", 169.818238, -20.192937),
    ("Preah Vihear", 104.68028, 14.39056),
    ("Sukhothai", 99.7000, 17.0167),
    ("Pyay", 95.22, 18.85),
    ("Khajuraho", 79.9250, 24.8500),
    ("Mohenjo Daro", 68.1389, 27.3292),
    ("Persepolis", 52.8900, 29.9350),
    ("Ur", 46.1018, 30.9575),
    ("Petra", 35.44, 30.33)
]

def latlon_to_cartesian(lon, lat):
    """Convert latitude and longitude to Cartesian coordinates."""
    lon_rad = np.radians(lon)
    lat_rad = np.radians(lat)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    return np.array([x, y, z])

def cartesian_to_latlon(vec):
    """Convert Cartesian coordinates to latitude and longitude."""
    x, y, z = vec / np.linalg.norm(vec)
    lat = np.degrees(np.arcsin(z))
    lon = np.degrees(np.arctan2(y, x))
    if lon < -180:
        lon += 360
    elif lon > 180:
        lon -= 360
    return lon, lat

def great_circle_distance_to_plane(point, pole):
    """Calculate the great-circle distance from a point to the plane defined by the pole."""
    point = point / np.linalg.norm(point)
    pole = pole / np.linalg.norm(pole)
    dot = np.abs(np.dot(point, pole))
    dot = min(max(dot, -1.0), 1.0)
    angular_distance = np.pi / 2 - np.arccos(dot)
    return abs(angular_distance * EARTH_RADIUS)

def objective_function(pole_params, points):
    """Objective function to minimize: sum of squared distances to the equator."""
    lon_pole, lat_pole = pole_params
    pole = latlon_to_cartesian(lon_pole, lat_pole)
    distances = [great_circle_distance_to_plane(point, pole) for point in points]
    return sum(d ** 2 for d in distances)

def compute_total_sum_of_squares(points):
    """Compute the total sum of squares: sum of squared distances to current equator."""
    current_north_pole = np.array([0, 0, 1])  # Current north pole in Cartesian
    distances = [great_circle_distance_to_plane(point, current_north_pole) for point in points]
    return sum(d ** 2 for d in distances)

# Convert all sites to Cartesian coordinates
site_points = [latlon_to_cartesian(lon, lat) for _, lon, lat in ancient_sites]

# Bounds for longitude (-180 to 180) and latitude (-90 to 90)
bounds = [(-180, 180), (-90, 90)]

# Use differential evolution for global optimization
result = differential_evolution(
    objective_function,
    bounds,
    args=(site_points,),
    strategy='best1bin',
    maxiter=1000,
    popsize=15,
    tol=0.01,
    disp=False
)

# Refine with local optimization
result_refined = minimize(
    objective_function,
    result.x,
    args=(site_points,),
    method='SLSQP',
    bounds=bounds,
    options={'disp': False}
)

# Extract the optimal pole coordinates
optimal_lon, optimal_lat = result_refined.x
optimal_pole = latlon_to_cartesian(optimal_lon, optimal_lat)

# Compute residual sum of squares (sum of squared distances to new equator)
distances = [great_circle_distance_to_plane(point, optimal_pole) for point in site_points]
residual_sum_of_squares = sum(d ** 2 for d in distances)

# Compute total sum of squares (sum of squared distances to current equator)
total_sum_of_squares = compute_total_sum_of_squares(site_points)

# Compute R^2
r_squared = 1 - residual_sum_of_squares / total_sum_of_squares if total_sum_of_squares != 0 else 0

# Print the result
print(f"Optimal new north pole coordinates:")
print(f"Longitude: {optimal_lon:.6f}°")
print(f"Latitude: {optimal_lat:.6f}°")
print(f"Total distance to equator: {sum(distances):.2f} km")
print(f"R^2 value: {r_squared:.4f}")

# List distances for each site
print("\nDistances from each site to the new equator:")
for (name, lon, lat), distance in zip(ancient_sites, distances):
    print(f"{name}: {distance:.2f} km")