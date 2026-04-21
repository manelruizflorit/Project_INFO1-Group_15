import os
from fileinput import filename

import matplotlib.pyplot as plt

# --- STEP 1: CLASS DEFINITION ---
class Airport:
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat  # Sera un nombre décimal (float)
        self.lon = lon  # Sera un nombre décimal (float)
        self.schengen = False

def IsSchengenAirport(code):
    if not code:
        return False
    # List of prefixes for Schengen countries
    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 
                      'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    return code[:2].upper() in schengen_codes

def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.code)

def PrintAirport(airport):
    status = "Schengen" if airport.schengen else "Non-Schengen"
    print(f"ICAO: {airport.code} / Lat: {airport.lat} / Lon: {airport.lon} / Zone: {status}")

# --- STEP 3: CONVERTER & FILE MANAGEMENT ---

def ConvertToDecimal(coord_str):
    """ Converts N635906 to decimal degrees """
    direction = coord_str[0]
    if len(coord_str) == 7:
        # proces latitude
        # IL FAUT METTRE int() ICI POUR TRANSFORMER LE TEXTE EN NOMBRE
        deg = int(coord_str[1:3])  # "63" -> 63
        minutes = int(coord_str[3:5])  # "59" -> 59
        seconds = int(coord_str[5:7])  # "06" -> 6
    else:
        # proces longitude
        # IL FAUT METTRE int() ICI POUR TRANSFORMER LE TEXTE EN NOMBRE
        deg = int(coord_str[1:4])  # "63" -> 63
        minutes = int(coord_str[4:6])  # "59" -> 59
        seconds = int(coord_str[6:8])  # "06" -> 6

    
    # Maintenant que ce sont des nombres, le calcul fonctionne !
    decimal = deg + (minutes / 60.0) + (seconds / 3600.0)
    
    if direction == 'S' or direction == 'W':
        decimal = -decimal
        
    return round(decimal, 6)
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
                
                # Si ça commence par une lettre (N, S, E, W), on convertit
                if parts[1][0] in ['N', 'S', 'E', 'W']:
                    lat_dec = ConvertToDecimal(parts[1])
                    lon_dec = ConvertToDecimal(parts[2])
                # Sinon, c'est que c'est DÉJÀ un nombre décimal ! On le transforme juste en float
                else:
                    lat_dec = float(parts[1])
                    lon_dec = float(parts[2])
                    
                new_airport = Airport(code, lat_dec, lon_dec)
                airports_list.append(new_airport)
                    
    return airports_list

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

# --- STEP 5: GRAPHICS ---

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
    plt.bar("Airports", nb_ns, bottom=nb_s, color='red', label='No Schengen')
    plt.title("Schengen Airport")
    plt.ylabel("Count")
    plt.legend()
    plt.show()

# --- LIST HELPERS ---

def AddAirport(airports, airport):
    for a in airports:
        if a.code == airport.code:
            return # Already exists
    airports.append(airport)

def RemoveAirport(airports, code):
    for i in range(len(airports)):
        if airports[i].code == code:
            airports.pop(i)
            return 0
    return -1
def MapAirports(airports):
    # This function allows us to see in google earth the airports that we want, distinguished as shengen and non shengen by colors
    airports = LoadAirports(airports)
    if not airports:
        return -1
    filename = "airports.kml"
    try:
    # We create a KML file to edit it.
        with open(filename, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            file.write('<Document>\n')
    # We differentiate from Shengen to non shengen airports with colors
            i = 0
            while i < len(airports):
                SetSchengen(airports[i])
                if airports[i].schengen :
                    pin_color = "ff00ffff"
                else:
                    pin_color = "ffff0000"
    # It generates a Placemark for every airport defining it for google Earth
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

def ShowAirports(list):
    resultat = MapAirports(list)
    if resultat == 0:
        ruta_kml = os.path.join(os.getcwd(), "airports.kml")
        os.startfile(ruta_kml)

