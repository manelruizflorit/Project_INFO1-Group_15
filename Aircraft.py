import math
from idlelib.debugger_r import close_remote_debugger
from math import radians, cos

from airport import *

#We define a new class, aircaft:

class Aircraft:
    def __init__(self, aircraft_id, origin_airport, landing_time, airline_company):
        self.aircraft_id = aircraft_id #string of the aircraft
        self.airline_company = airline_company #3 characters with the ICAO code of the airline
        self.origin_airport = origin_airport #4 characters with the ICAO code of the airport the aircraft is coming from
        self.landing_time = landing_time # 5 characters with the format: hh:mm



def LoadArrivals(filename):
    arrivals_list = []
    linea = False
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as q:
        lines = q.readlines()

        if len(lines) <= 1:
            return []

        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) == 4:
                if len(parts[0]) > 6 or len(parts[1]) != 4 or len(parts[3]) != 3: #we need sharuk to improve our filter on time and numbers
                    linea = True
                elif linea == False:
                    aircraft_id = str(parts[0]).upper()
                    new_aircraft = Aircraft(aircraft_id, parts[1], parts[2], parts[3])
                    arrivals_list.append(new_aircraft)
                else:
                    linea = False

    return arrivals_list

def PlotArrivals(aircrafts):
    aircrafts = LoadArrivals(aircrafts)
    # We check if the list is empty and create an error message
    if not aircrafts:
        print("Error: The arrivals list is empty. The graphic cannot be generated.")
        return

    # We create a list with a 0 for every hour of the day
    arrivals_per_hour = [0] * 24

    # We check every aircraft's arrival time and codes
    for aircraft in aircrafts:
        try:
            # We take only the hours in the time for every arrival and add them up
            hour_str = aircraft.landing_time.split(':')[0]
            hour = int(hour_str)

            if 0 <= hour <= 23:
                arrivals_per_hour[hour] += 1
        except (ValueError, IndexError):
            # We skip if a time doesn't have the right value
            continue

    # We create the labels for the axes
    hours_labels = [f"{i:02d}:00" for i in range(24)]

    # We make the bar plot to show everything and set colors to the bars
    plt.figure(figsize=(10, 6))
    plt.bar(hours_labels, arrivals_per_hour, color='skyblue', edgecolor='black')

    # We add titles and imporve design
    plt.title('Arrivals per hour in LEBL')
    plt.xlabel('Time of the day')
    plt.ylabel('Number of arrivals')
    plt.xticks(rotation=45)  # We turn the labels a bit just so we can read them better
    plt.yticks(range(0, max(arrivals_per_hour) + 2))  # We adjust the y labels so we can see whole numbers
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def SaveFlights(aircrafts, filename):
    aircrafts = LoadArrivals(aircrafts)
    # If the list is empty → error
    if not aircrafts:
        print("Error: The aircraft list is empty. No file created.")
        return -1  # error code

    try:
        with open(filename, 'w') as f:
            # Write header (adjust if your input header is different)
            f.write("ID ORIGIN TIME AIRLINE\n")

            for aircraft in aircrafts:
                # Replace empty fields
                aircraft_id = aircraft.aircraft_id if aircraft.aircraft_id else "-"
                origin = aircraft.origin_airport if aircraft.origin_airport else "-"
                time = aircraft.landing_time if aircraft.landing_time else "00:00"
                airline = aircraft.airline_company if aircraft.airline_company else "-"

                # Write line in same format as input
                f.write(f"{aircraft_id} {origin} {time} {airline}\n")

        return 0  # success

    except Exception as e:
        print(f"Error writing file: {e}")
        return -1


def PlotAirlines(aircrafts):
    aircrafts = LoadArrivals(aircrafts)
    # Check if empty
    if not aircrafts:
        print("Error: The aircraft list is empty. The graphic cannot be generated.")
        return

    # Create empty vectors
    airlines = []
    counts = []

    # Count manually
    for aircraft in aircrafts:
        airline = aircraft.airline_company if aircraft.airline_company.exists else "-"

        if airline in airlines:
            index = airlines.index(airline)
            counts[index] += 1
        else:
            airlines.append(airline)
            counts.append(1)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(airlines, counts, edgecolor='black')

    plt.title('Flights per Airline')
    plt.xlabel('Airline (ICAO Code)')
    plt.ylabel('Number of Flights')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def PlotFlightsType(aircrafts):
    aircrafts = LoadArrivals(aircrafts)
    # Check if empty
    if not aircrafts:
        print("Error: The aircraft list is empty. The graphic cannot be generated.")
        return

    # Create counters
    schengen_count = 0
    non_schengen_count = 0

    # Count manually
    for aircraft in aircrafts:

        if IsSchengenAirport(aircraft.origin_airport) == True:
            schengen_count += 1
        else:
            non_schengen_count += 1

    #Data for plot
    labels = ["Flights"]
    schengen_values = [schengen_count]
    non_schengen_values = [non_schengen_count]

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(labels, schengen_values, label = "Schengen", edgecolor='black')
    plt.bar(labels, non_schengen_values, bottom = schengen_values, label="Non-Schengen", edgecolor='black')

    plt.title('Flights by origin airport (Schengen vs Non-Schengen)')
    plt.ylabel('Number of flights')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def Coordenates(Airport_code):
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
                    if code == str(Airport_code):
                        if parts[1][0] in ['N', 'S', 'E', 'W']:
                            lat_dec = ConvertToDecimal(parts[1])
                            lon_dec = ConvertToDecimal(parts[2])
                        else:
                            lat_dec = float(parts[1])
                            lon_dec = float(parts[2])
        coordenadas[0] = lat_dec
        coordenadas[1] = lon_dec
    except ValueError:
        return []
    return coordenadas

def MapFlights(flights):
    flights = LoadArrivals(flights)
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
            if IsSchengenAirport(origin):
                color = "ff00ffff"
            else:
                color = "ffff0000"

            lat_final = 41.2969
            lon_final = 2.0784

            cordenadas = Coordenates(origin)

            lon_inicial = cordenadas[1]
            lat_inicial = cordenadas[0]


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

def ShowFlights(list):
    show = MapFlights(list)
    if show == 0:
        route_kml = os.path.join(os.getcwd(), "flights.kml")
        os.startfile(route_kml)

def Haversine(Origin_airport_code):
    cords = Coordenates(Origin_airport_code)
    leblcords = Coordenates("LEBL")
    earth_radius = 6371
    d_lat = abs(cords[0]-leblcords[0])
    d_lon = abs(cords[1]-leblcords[1])
    a = math.sin(math.radians(d_lat) / 2)**2 + math.cos(math.radians(cords[0]))*math.cos(math.radians(leblcords[0]))*math.sin(math.radians(d_lon) / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_radius * c
    return d

def LongDistanceArrivals(aircrafts):
    flights = LoadArrivals(aircrafts)
    long_distance_aircrafts =[]
    if not aircrafts:
        return []
    i = 0
    while i < len(flights):
        origen = flights[i].origin_airport
        avion = flights[i].aircraft_id
        if Haversine(origen) > 2000:
            long_distance_aircrafts.append(avion)
    i += 1
    return long_distance_aircrafts

