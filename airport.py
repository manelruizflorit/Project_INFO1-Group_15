import os
from fileinput import filename

import matplotlib.pyplot as plt

# Definition of our Airport class with four categories: ICAO code, latitude, longitude, Schengen zone or not (Always starts with false)
class Airport:
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.schengen = False

# Takes an ICAO code and checks if the first two letters match any Schengen country prefix
# Returns True if it does, False if not or if the code is empty
def IsSchengenAirport(code):
    if not code:
        return False
    # List of prefixes for Schengen countries
    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 
                      'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    return code[:2].upper() in schengen_codes

# Takes an airport object and updates its schengen attribute by calling IsSchengenAirport with its code
def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.code)

# Prints the airport's code, latitude, longitude, and Schengen status to the console in a readable format
def PrintAirport(airport):
    status = "Schengen" if airport.schengen else "Non-Schengen"
    print(f"ICAO: {airport.code} / Lat: {airport.lat} / Lon: {airport.lon} / Zone: {status}")

# Converts a coordinate string in the format used in the data file (e.g. N635906) into a decimal degrees float
# Handles both latitude (7 characters) and longitude (8 characters), and applies a negative sign for South or West directions
def ConvertToDecimal(coord_str):
    """ Converts N635906 to decimal degrees """
    direction = coord_str[0]
    if len(coord_str) == 7:
        # Handles latitude
        # It uses int() to convert the string into a number
        deg = int(coord_str[1:3])  # "63" -> 63
        minutes = int(coord_str[3:5])  # "59" -> 59
        seconds = int(coord_str[5:7])  # "06" -> 6
    else:
        # Handles longitude
        # It uses int() to convert the string into a number
        deg = int(coord_str[1:4])  # "63" -> 63
        minutes = int(coord_str[4:6])  # "59" -> 59
        seconds = int(coord_str[6:8])  # "06" -> 6

    # The calculation works now as the code is in numbers
    decimal = deg + (minutes / 60.0) + (seconds / 3600.0)
    
    if direction == 'S' or direction == 'W':
        decimal = -decimal
        
    return round(decimal, 6)

# Opens a text file and reads airport data line by line (skipping the header)
# For each line, it breaks down the code and coordinates (converting from string format to decimal if needed) and returns a list of Airport objects
# Returns an empty list if the file doesn't exist
def LoadAirports(filename):
    airports_list = []
    if not os.path.exists(filename):
        return []

    with open(filename, 'r') as f:
        lines = f.readlines()
        
        if len(lines) <= 1:
            return []

        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) == 3:
                code = parts[0]
                
                # If the latitude and longitude start with a NSEW letter, it pulls the ConvertToDecimal function on it
                if parts[1][0] in ['N', 'S', 'E', 'W']:
                    lat_dec = ConvertToDecimal(parts[1])
                    lon_dec = ConvertToDecimal(parts[2])
                # If the latitude and longitude are already in decimal numbers, it pulls the numbers itseld
                else:
                    lat_dec = float(parts[1])
                    lon_dec = float(parts[2])
                    
                new_airport = Airport(code, lat_dec, lon_dec)
                airports_list.append(new_airport)
                    
    return airports_list

# Filters a list of airports to keep only the Schengen ones, then writes them to a file in the same format as the input file
# Returns -1 if there are no Schengen airports to save
def SaveSchengenAirports(airports, filename):
    schengen_only = []
    # Loop to find only Schengen airports
    for a in airports:
        if IsSchengenAirport(a.code):
            schengen_only.append(a)

    if len(schengen_only) == 0:
        return -1 # Error code
    
    with open(filename, 'w') as f:
        f.write("CODE LAT LON\n")
        for a in schengen_only:
            f.write(f"{a.code} {a.lat} {a.lon}\n")
    return 0

# Counts how many airports in the list are Schengen and how many are not
# Then displays a stacked bar chart using matplotlib to visualize the split
def PlotAirports(airports):
    nb_s = 0
    nb_ns = 0
    # Simple loop to count
    for a in airports:
        if IsSchengenAirport(a.code):
            nb_s = nb_s + 1
        else:
            nb_ns = nb_ns + 1

    # Plotting
    plt.bar("Airports", nb_s, color='blue', label='Schengen')
    plt.bar("Airports", nb_ns, bottom=nb_s, color='red', label='Non Schengen')
    plt.title("Schengen Airport")
    plt.ylabel("Count")
    plt.legend()
    plt.show()

# Adds an airport to the list only if no airport with the same code already exists in it
# Does nothing if it's a duplicate
def AddAirport(airports, airport):
    for a in airports:
        if a.code == airport.code:
            return # Already exists
    airports.append(airport)

# Searches the list for an airport matching the given code and removes it
# Returns 0 on success, -1 if the airport wasn't found.
def RemoveAirport(airports, code):
    for i in range(len(airports)):
        if airports[i].code == code:
            airports.pop(i)
            return 0
    return -1

# Generates a KML file (airports.kml) that can be opened in Google Earth
# Each airport is added as a placemark with a colored pin (cyan for Schengen, red for non-Schengen)
# Returns 0 on success, -1 on failure or empty list
def MapAirports(airports):
    if not airports:
        return -1
    filename = "airports.kml"
    try:
        with open(filename, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            file.write('<Document>\n')
            i = 0
            while i < len(airports):
                SetSchengen(airports[i])
                if airports[i].schengen :
                    pin_color = "ff00ffff"
                else:
                    pin_color = "ffff0000"
                airport = airports[i]
                file.write('  <Placemark>\n')
                file.write('    <name>' + airport.code + '</name>\n')
                file.write('    <Style>')
                file.write('      <IconStyle>\n')
                file.write('        <color>' + pin_color + '</color>\n')
                file.write('        <Icon>\n')
                file.write('          <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>\n')
                file.write('        </Icon>\n')
                file.write('      </IconStyle>\n')
                file.write('    </Style>')
                file.write('    <Point>\n')
                coords = str(airport.lon) + "," + str(airport.lat)
                file.write('      <coordinates>' + coords + '</coordinates>\n')
                file.write('    </Point>\n')
                file.write('  </Placemark>\n')
                i += 1
            file.write('</Document>\n')
            file.write('</kml>\n')
        return 0
    except IOError:
        return -1

# Calls MapAirports to generate the KML file
# Opens the file directly with the system's default application (Google Earth) using os.startfile
def ShowAirports(list):
    resultat = MapAirports(list)
    if resultat == 0:
        ruta_kml = os.path.join(os.getcwd(), "airports.kml")
        os.startfile(ruta_kml)
