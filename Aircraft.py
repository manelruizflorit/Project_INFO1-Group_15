import os
import matplotlib.pyplot as plt

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
                if len(parts[0]) != 5 or len(parts[1]) != 4 or len(parts[3]) != 3: #we need sharuk to improve our filter on time and numbers
                    linea = True

                elif linea == False:
                    aircraft_id = str(parts[0]).upper()
                    new_aircraft = Aircraft(aircraft_id, parts[1], parts[2], parts[3])
                    arrivals_list.append(new_aircraft)

                else:
                    linea = False

    return arrivals_list



def PlotArrivals(aircrafts):
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
    # Check if empty
    if not aircrafts:
        print("Error: The aircraft list is empty. The graphic cannot be generated.")
        return

    # Create empty vectors
    airlines = []
    counts = []

    # Count manually
    for aircraft in aircrafts:
        airline = aircraft.airline_company if aircraft.airline_company else "-"

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
