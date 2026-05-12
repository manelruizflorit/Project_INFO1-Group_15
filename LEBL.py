# LEBL.py

import os
from airport import IsSchengenAirport
from Aircraft import Aircraft, LoadArrivals

# ==========================================
# CLASSES
# ==========================================

class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""


class BoardingArea:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.gates = []


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []


class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


# ==========================================
# FUNCTIONS
# ==========================================

def SetGates(area, init_gate, end_gate, prefix):
    # If the end gate number is not greater than the init gate number, return -1[cite: 1]
    if end_gate <= init_gate:
        return -1

    # If the area had a previous list of gates, drop it[cite: 1]
    area.gates = []

    for i in range(init_gate, end_gate + 1):
        # Create the name using basic string addition
        gate_name = prefix + str(i)
        new_gate = Gate(gate_name)
        area.gates.append(new_gate)

    return 0


def LoadAirlines(terminal, t_name):
    # Build the file name as required[cite: 1]
    filename = t_name + "_Airlines.txt"

    try:
        with open(filename, 'r') as file:
            # Drop previous list of airlines if it existed[cite: 1]
            terminal.airlines = []

            for line in file:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    terminal.airlines.append(parts[1].strip())
        return 0
    except FileNotFoundError:
        # If the file does not exist, an error code shall be returned[cite: 1]
        return -1


def LoadAirportStructure(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if len(lines) == 0:
            return -1

        first_line = lines[0].split()
        bcn = BarcelonaAP(first_line[0])

        current_terminal = None

        for i in range(1, len(lines)):
            line = lines[i].strip()

            if line.startswith("Terminal"):
                parts = line.split()
                t_name = parts[1]
                current_terminal = Terminal(t_name)
                bcn.terminals.append(current_terminal)

                # Call LoadAirlines immediately[cite: 1]
                LoadAirlines(current_terminal, t_name)

            elif line.startswith("Area"):
                parts = line.split()
                area_name = parts[1]
                type = parts[2]

                gate_parts = line.split('Gates')
                numbers_part = gate_parts[1].strip()

                start_and_end = numbers_part.split('-')
                init_gate = int(start_and_end[0].strip())
                end_gate = int(start_and_end[1].strip())

                new_area = BoardingArea(area_name, type)
                if current_terminal != None:
                    current_terminal.boarding_areas.append(new_area)

                # Use different prefixes for each boarding area to easily locate a gate[cite: 1]
                prefix = current_terminal.name + area_name + "G"
                SetGates(new_area, init_gate, end_gate, prefix)

        return bcn

    except FileNotFoundError:
        return -1


def GateOccupancy(bcn):
    # Returns a list of gates with their names, their status and the id of the aircraft[cite: 1]
    occupancy_list = []

    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                gate_info = [gate.name, gate.occupied, gate.aircraft_id]
                occupancy_list.append(gate_info)

    return occupancy_list


def IsAirlineInTerminal(terminal, name):
    # If the name of the airline is a null string then False and an error code must be returned[cite: 1]
    if name == "":
        return False, -1

    if name in terminal.airlines:
        return True
    else:
        return False


def SearchTerminal(bcn, name):
    for terminal in bcn.terminals:
        result = IsAirlineInTerminal(terminal, name)

        # This safely ignores the (False, -1) tuple without crashing
        if result == True:
            return terminal.name

    return ""
    # If the airline is not found, the return name shall be a null string[cite: 1]
    return ""


def AssignGate(bcn, aircraft):
    # 1. Check the airline-terminal assignment using SearchTerminal[cite: 1]
    req_terminal = SearchTerminal(bcn, aircraft.airline_company)

    if req_terminal == "":
        return -1

    # 2. Check if the origin airport is Schengen using YOUR airport.py function
    is_schengen = IsSchengenAirport(aircraft.origin_airport)

    if is_schengen == True:
        req_type = "Schengen"
    else:
        req_type = "non-Schengen"

    # 3. Looks for the first gate that is not occupied in the correct boarding area[cite: 1]
    for terminal in bcn.terminals:
        if terminal.name == req_terminal:
            for area in terminal.boarding_areas:
                if area.type == req_type:
                    for gate in area.gates:
                        if gate.occupied == False:
                            # Update the occupancy boolean and the aircraft field[cite: 1]
                            gate.occupied = True
                            # IMPORTANT: Using aircraft.aircraft_id to match your aircraft.py class!
                            gate.aircraft_id = aircraft.aircraft_id
                            return 0

    # If there is no more free gates, an error code shall be returned[cite: 1]
    return -1


# ==========================================
# TEST SECTION
# ==========================================
if __name__ == "__main__":
    print("--- STARTING VERSION 3 INTEGRATION TESTS ---")

    # 1. Load the Airport
    bcn_airport = LoadAirportStructure("LEBL.txt")

    if bcn_airport == -1:
        print(
            "ERROR: Could not load LEBL.txt. Make sure LEBL.txt, T1_Airlines.txt, and T2_Airlines.txt are in the folder.")
    else:
        print("SUCCESS: Loaded Airport " + bcn_airport.code)

        # 2. Load the real aircraft from your Arrivals text file!
        # Make sure "Arrivals.txt" is in your folder.
        real_flights = LoadArrivals("Arrivals.txt")

        if not real_flights:
            print("WARNING: Could not load Arrivals.txt. Place the file in the folder to test gate assignment.")
        else:
            print("SUCCESS: Loaded " + str(len(real_flights)) + " aircraft from Arrivals.txt")

            # 3. Try to assign gates to the first 10 planes that landed
            success_count = 0
            fail_count = 0

            # We only test the first 10 so we don't spam the console
            planes_to_test = real_flights[:10]

            for plane in planes_to_test:
                result = AssignGate(bcn_airport, plane)
                if result == 0:
                    success_count += 1
                else:
                    fail_count += 1

            print("\nAssignment Results for first 10 planes:")
            print("- Successfully parked: " + str(success_count))
            print("- Failed to park: " + str(fail_count) + " (Usually means airline not found in T1/T2 txt files)")

            # 4. Check the occupancy list
            all_gates = GateOccupancy(bcn_airport)
            occupied_gates = []

            for g in all_gates:
                if g[1] == True:  # g[1] is the occupied status
                    occupied_gates.append(g)

            print("\nOccupied Gates List:")
            if len(occupied_gates) > 0:
                for g in occupied_gates:
                    print("-> Gate " + g[0] + " is occupied by flight " + g[2])
            else:
                print("-> No gates are currently occupied.")

    print("\n--- TESTS FINISHED ---")