import math
from idlelib.debugger_r import close_remote_debugger
from math import radians, cos

from airport import *

# Represents an arriving aircraft with its ID, origin airport, landing time and airline company
class Aircraft:
    def __init__(self, aircraft_id, origin_airport, landing_time, airline_company, destination_airport, deparature_time):
        self.aircraft_id = aircraft_id #string of the aircraft
        self.airline_company = airline_company #3 characters with the ICAO code of the airline
        self.origin_airport = origin_airport #4 characters with the ICAO code of the airport the aircraft is coming from
        self.landing_time = landing_time # 5 characters with the format: hh:mm
        self.destination_airport = destination_airport #4 characters with the ICAO code of the airport the aircraft is coming from
        self.deparature_time = deparature_time  # 5 characters with the format: hh:mm


# Opens a text file and reads arrival data line by line, skipping the header and any malformed lines
# Returns a list of Aircraft objects, or an empty list if the file doesn't exist
def LoadArrivals(filename):
    arrivals_list = []
    linea = False
    # Returns an empty list if the file doesn't exist
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as q:
        lines = q.readlines()

        # Returns empty list if the file has only a header or is empty
        if len(lines) <= 1:
            return []

        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) == 4:
                # Skips the line if any field has an incorrect length
                if len(parts[0]) > 6 or len(parts[1]) != 4 or len(parts[3]) != 3:
                    linea = True
                elif linea == False:
                    # Creates a new Aircraft object and adds it to the list
                    aircraft_id = str(parts[0]).upper()
                    new_aircraft = Aircraft(aircraft_id, parts[1], parts[2], parts[3], None, None)
                    arrivals_list.append(new_aircraft)
                else:
                    linea = False

    return arrivals_list

# Counts the number of arrivals per hour of the day and displays a bar chart
# Shows an error message and returns if the list is empty
def PlotArrivals(aircrafts):
    # We check if the list is empty and create an error message
    if not aircrafts:
        print("Error: The arrivals list is empty. The graphic cannot be generated.")
        return

    # Creates a list with a 0 for every hour of the day
    arrivals_per_hour = [0] * 24

    # Checks every aircraft's arrival time and codes
    for aircraft in aircrafts:
        try:
            # Takes only the hours in the time for every arrival and adds them up
            hour_str = aircraft.landing_time.split(':')[0]
            hour = int(hour_str)

            if 0 <= hour <= 23:
                arrivals_per_hour[hour] += 1
        except (ValueError, IndexError):
            # Skips if a time doesn't have the right value
            continue

    # Creates the labels for the axes
    hours_labels = [f"{i:02d}:00" for i in range(24)]

    # Makes the bar plot to show everything and sets colors to the bars
    plt.figure(figsize=(10, 6))
    plt.bar(hours_labels, arrivals_per_hour, color='skyblue', edgecolor='black')

    # Add titles and improves design
    plt.title('Arrivals per hour in LEBL')
    plt.xlabel('Time of the day')
    plt.ylabel('Number of arrivals')
    plt.xticks(rotation=45)  # We turn the labels a bit just so we can read them better
    plt.yticks(range(0, max(arrivals_per_hour) + 2))  # We adjust the y labels so we can see whole numbers
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# Writes the aircraft list to a file in the same format as the input file
# Returns -1 if the list is empty or if writing fails, 0 on success
def SaveFlights(aircrafts, filename):
    # Returns error code if the list is empty
    if not aircrafts:
        print("Error: The aircraft list is empty. No file created.")
        return -1  # error code

    try:
        with open(filename, 'w') as f:
            # Writes a header
            f.write("AIRCRAFT ORIGIN TIME AIRLINE\n")

            for aircraft in aircrafts:
                # Replaces empty fields with a placeholder
                a_id = aircraft.aircraft_id if aircraft.aircraft_id else "-"
                origin = aircraft.origin_airport if aircraft.origin_airport else "-"
                time = aircraft.landing_time if aircraft.landing_time else "00:00"
                airline = aircraft.airline_company if aircraft.airline_company else "-"

                # Writes lines in same format as the input
                f.write(f"{a_id} {origin} {time} {airline}\n")

        return 0

    except Exception as e:
        print(f"Error writing file: {e}")
        return -1

# Counts the number of flights per airline and displays a bar chart
# Shows an error message and returns nothing if the list is empty
def PlotAirlines(aircrafts):
    # Checks if the list is empty
    if not aircrafts:
        print("Error: The aircraft list is empty. The graphic cannot be generated.")
        return

    # Creates two empty vectors
    airlines = []
    counts = []

    # Counts manually
    for aircraft in aircrafts:
        airline = aircraft.airline_company
        if airline in airlines:
            index = airlines.index(airline)
            counts[index] += 1
        else:
            airlines.append(airline)
            counts.append(1)

    # Plots the two created lists
    plt.figure(figsize=(10, 6))
    plt.bar(airlines, counts, edgecolor='black')

    plt.title('Flights per Airline')
    plt.xlabel('Airline (ICAO Code)')
    plt.ylabel('Number of Flights')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# Counts Schengen and non-Schengen flights based on origin airport and displays a stacked bar chart
# Shows an error message and returns if the list is empty
def PlotFlightsType(aircrafts):
    # Checks if the list is empty
    if not aircrafts:
        print("Error: The aircraft list is empty. The graphic cannot be generated.")
        return

    # Creates two counters
    schengen_count = 0
    non_schengen_count = 0

    # Counts manually
    for aircraft in aircrafts:

        if IsSchengenAirport(aircraft.origin_airport) == True:
            schengen_count += 1
        else:
            non_schengen_count += 1

    # Takes the data for plot
    labels = ["Flights"]
    schengen_values = [schengen_count]
    non_schengen_values = [non_schengen_count]

    # Plots the data (two vectors)
    plt.figure(figsize=(10, 6))
    plt.bar(labels, schengen_values, label = "Schengen", edgecolor='black')
    plt.bar(labels, non_schengen_values, bottom = schengen_values, label="Non-Schengen", edgecolor='black')

    plt.title('Flights by origin airport (Schengen vs Non-Schengen)')
    plt.ylabel('Number of flights')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# Searches the Airports.txt file for the given ICAO code and returns its latitude and longitude as a list
# Returns empty if the code is not found or an error occurs
def Coordenates(Airport_code):
    # Returns early if no code is provided
    if not Airport_code:
        print("Error, there's no airport ICAO code")
        return
    coordenadas = [0,0]
    try:
        with open("Airports.txt", 'r') as f:
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
                    # Checks if the code matches and converts coordinates to decimal
                    if code == str(Airport_code):
                        if parts[1][0] in ['N', 'S', 'E', 'W']:
                            lat_dec = ConvertToDecimal(parts[1])
                            lon_dec = ConvertToDecimal(parts[2])
                        else:
                            lat_dec = float(parts[1])
                            lon_dec = float(parts[2])
        # Stores the result in the coordinates list
        coordenadas[0] = lat_dec
        coordenadas[1] = lon_dec
    except ValueError:
        return []
    return coordenadas

# Generates a KML file (flights.kml) with a line for each flight from its origin airport to LEBL
# Lines are colored cyan for Schengen origins and red for non-Schengen
# Returns 0 on success, -1 on failure or empty list
def MapFlights(flights):
    if not flights:
        return -1
    filename = "flights.kml"
    try:
        f = open(filename, "w")

        f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write("<Document>\n")

        i = 0
        while i < len(flights):
            flight = flights[i]
            origin = flight.origin_airport
            # Sets the pin color based on the airport's Schengen status
            if IsSchengenAirport(origin):
                color = "ff00ffff"
            else:
                color = "ffff0000"

            # Fixed coordinates for LEBL as the destination airport
            lat_final = 41.2969
            lon_final = 2.0784

            # Gets the origin airport coordinates from the file
            cordenadas = Coordenates(origin)

            lon_inicial = cordenadas[1]
            lat_inicial = cordenadas[0]

            # Writes a placemark with a line from the origin airport to LEBL
            f.write("   <Placemark>\n")
            f.write("   <name>" + str(flight.aircraft_id) + "</name>\n")
            f.write("   <Style><LineStyle><color>" + color + "</color><width>2</width></LineStyle></Style>\n")
            f.write("   <LineString>\n")
            f.write("   <coordinates>\n")

            f.write("   " + str(lon_inicial) + "," + str(lat_inicial) + ",0 ")
            f.write(str(lon_final) + "," + str(lat_final) + ",0\n")
            f.write("   </coordinates>\n")
            f.write("   </LineString>\n")
            f.write("   </Placemark>\n")

            i += 1
        f.write("</Document>\n")
        f.write("</kml>\n")
        f.close()

        return 0
    except IOError:
        return -1

# Calls MapFlights to generate the KML file and opens it with the system's default application
def ShowFlights(list):
    show = MapFlights(list)
    if show == 0:
        route_kml = os.path.join(os.getcwd(), "flights.kml")
        os.startfile(route_kml)

# Calculates the great-circle distance in km between the given airport and LEBL using the Haversine formula
def Haversine(Origin_airport_code):
    # Gets the coordinates of both the origin airport and LEBL
    cords = Coordenates(Origin_airport_code)
    leblcords = Coordenates("LEBL")
    earth_radius = 6371
    # Calculates the differences in latitude and longitude
    d_lat = abs(cords[0]-leblcords[0])
    d_lon = abs(cords[1]-leblcords[1])
    # Applies the Haversine formula to get the distance
    a = math.sin(math.radians(d_lat) / 2)**2 + math.cos(math.radians(cords[0]))*math.cos(math.radians(leblcords[0]))*math.sin(math.radians(d_lon) / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_radius * c
    return d

# Filters the arrivals list and returns only aircraft coming from airports more than 2000 km away from LEBL
# Returns an empty list if the input is empty
def LongDistanceArrivals(arrivals):
    long_distance =[]
    # Returns empty list if no arrivals are provided
    if not arrivals:
        return []
    i = 0
    while i < len(arrivals):
        origen = arrivals[i].origin_airport
        # Adds the aircraft to the list if its origin is more than 2000 km away
        if Haversine(origen) > 2000:
            long_distance.append(arrivals[i])
        i += 1
    return long_distance

# Filters long distance arrivals and opens their flight paths in Google Earth via a KML file
def ShowLongDistanceFlights(aircrafts):
    flights = LongDistanceArrivals(aircrafts)
    show = MapFlights(flights)
    if show == 0:
        route_kml = os.path.join(os.getcwd(), "flights.kml")
        os.startfile(route_kml)

def LoadDepartures(filename):
    departures_list = []
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as q:
        lines = q.readlines()

        if len(lines) <= 1:
            return []

        for i in range(1, len(lines)):  # ← len(lines) no len(line)
            line = lines[i].strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 4:
                if len(parts[0]) > 6 or len(parts[1]) != 4 or len(parts[3]) != 3:
                    continue
                aircraft_id = str(parts[0]).upper()
                # Creates Aircraft with departure data and None for arrival fields
                new_aircraft = Aircraft(aircraft_id, "LEBL", None, parts[3], parts[1], parts[2])
                departures_list.append(new_aircraft)

    return departures_list

def MergeMovements(arrivals, departures):
    # Returns error code if either list is empty
    if not arrivals or not departures:
        return -1

    merged_list = []

    for a in arrivals:
        arrival_hour = a.landing_time.split(":")[0]
        for d in departures:
            deparature_hour = d.deparature_time.split(":")[0]
            # Checks if same aircraft ID and landing time is before departure time
            if a.aircraft_id == d.aircraft_id and arrival_hour < deparature_hour:
                # Creates a merged Aircraft with both arrival and departure data
                new_aircraft = Aircraft(
                    a.aircraft_id,
                    a.origin_airport,
                    a.landing_time,
                    a.airline_company,
                    d.destination_airport,
                    d.deparature_time
                )
                merged_list.append(new_aircraft)

    return merged_list


def NightAircraft(aircrafts):
    if not aircrafts:
        return -1

    night_list = []

    for aircraft in aircrafts:
        if aircraft.landing_time is None and aircraft.destination_airport is not None:
            night_list.append(aircraft)

    if not night_list:
        return -1

    return night_list

