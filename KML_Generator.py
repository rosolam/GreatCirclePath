import numpy as np

# Define the pole coordinates (in degrees)
POLE_LAT = 59.682122
POLE_LON = -138.646087

# Convert pole coordinates to radians for calculations
pole_lat_rad = POLE_LAT * np.pi / 180
pole_lon_rad = POLE_LON * np.pi / 180

# Step 1: Define the great circle path
theta = np.linspace(0, 2 * np.pi, 360)  # 360 points for a smooth path

# Compute latitude (phi) and longitude (lambda) in radians
# Great circle as the equator in the coordinate system where (POLE_LAT, POLE_LON) is the pole
sin_pole_lat = np.sin(pole_lat_rad)
cos_pole_lat = np.cos(pole_lat_rad)
sin_pole_lon = np.sin(pole_lon_rad)
cos_pole_lon = np.cos(pole_lon_rad)

# Parametric equations for the great circle (rotated equator)
phi = np.arcsin(cos_pole_lat * np.cos(theta))
lam = np.arctan2(np.sin(theta), -sin_pole_lat * np.cos(theta)) + pole_lon_rad

# Convert to degrees (Google Earth expects degrees)
lat = phi * 180 / np.pi
lon = lam * 180 / np.pi

# Ensure longitude is in the range [-180, 180]
lon = (lon + 180) % 360 - 180

# Combine into a list of (longitude, latitude) pairs (Google Earth expects lon,lat order)
coordinates = list(zip(lon, lat))

# Step 2: Generate the KML file
kml_file = "great_circle_ancient_sites.kml"

with open(kml_file, "w") as f:
    # Write the KML header
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('  <Document>\n')
    f.write('    <name>Great Circle Path - Ancient Sites</name>\n')
    
    # Define the style for the path (a red line)
    f.write('    <Style id="pathStyle">\n')
    f.write('      <LineStyle>\n')
    f.write('        <color>ff0000ff</color>\n')  # Red line (ARGB: ff0000ff = red)
    f.write('        <width>4</width>\n')
    f.write('      </LineStyle>\n')
    f.write('    </Style>\n')
    
    # Define the Placemark for the great circle path
    f.write('    <Placemark>\n')
    f.write('      <name>Ancient Sites Great Circle</name>\n')
    f.write('      <styleUrl>#pathStyle</styleUrl>\n')
    f.write('      <LineString>\n')
    f.write('        <tessellate>1</tessellate>\n')  # Allows the path to follow the Earth's surface
    f.write('        <coordinates>\n')
    
    # Write the coordinates in the format: longitude,latitude,altitude
    for lon, lat in coordinates:
        f.write(f"          {lon},{lat},0\n")
    
    # Close the coordinates, LineString, Placemark
    f.write('        </coordinates>\n')
    f.write('      </LineString>\n')
    f.write('    </Placemark>\n')
    
    # Updated list of ancient sites with all locations from the screenshot
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
    
    for name, lon, lat in ancient_sites:
        f.write('    <Placemark>\n')
        f.write(f'      <name>{name}</name>\n')
        f.write('      <Point>\n')
        f.write(f'        <coordinates>{lon},{lat},0</coordinates>\n')
        f.write('      </Point>\n')
        f.write('    </Placemark>\n')
    
    # Close the Document and KML tags
    f.write('  </Document>\n')
    f.write('</kml>\n')

print(f"KML file '{kml_file}' generated successfully. Load it into Google Earth to explore the path!")