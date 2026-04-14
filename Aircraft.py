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
