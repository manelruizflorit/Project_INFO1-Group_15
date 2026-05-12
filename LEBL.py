import os
from Aircraft import *

# ==========================================
# CLASSES
# ==========================================

class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""


class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type   # "Schengen" or "non-Schengen"
        self.gates = []


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []      # List of ICAO airline codes (3-char)


class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


# ==========================================
# FUNCTIONS
# ==========================================

def SetGates(area, init_gate, end_gate, prefix):
    # If end_gate is not greater than init_gate, return error
    if end_gate <= init_gate:
        return -1

    # Drop previous list of gates
    area.gates = []

    for i in range(init_gate, end_gate + 1):
        gate_name = prefix + str(i)
        area.gates.append(Gate(gate_name))

    return 0


def LoadAirlines(terminal, t_name):
    # Build the file name
    filename = t_name + "_Airlines.txt"

    try:
        with open(filename, 'r') as f:
            terminal.airlines = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) >= 2:
                    terminal.airlines.append(parts[1].strip())
        return 0

    except FileNotFoundError:
        return -1


def LoadAirportStructure(filename):
    try:
        with open(filename, 'r') as f:
            lines = [l.rstrip('\n') for l in f.readlines()]
    except FileNotFoundError:
        return -1

    if not lines:
        return -1

    # First line: "LEBL 2 terminals"
    bcn = BarcelonaAP(lines[0].split()[0])

    current_terminal = None

    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("Terminal"):
            # "Terminal T1 5 boarding areas"
            t_name = stripped.split()[1]
            current_terminal = Terminal(t_name)
            bcn.terminals.append(current_terminal)
            LoadAirlines(current_terminal, t_name)

        elif stripped.startswith("Area"):
            # "Area A Schengen Gates 1 - 11"
            # "Area D non-Schengen Gates 1 - 11"
            if current_terminal is None:
                continue

            area_name = stripped.split()[1]

            # The type is everything between the area name and "Gates"
            gates_idx = stripped.index("Gates")
            area_type = stripped[stripped.index(area_name) + len(area_name):gates_idx].strip()

            # Gate numbers are after "Gates": "1 - 11"
            after_gates = stripped[gates_idx + len("Gates"):].strip()
            range_parts = after_gates.split('-')
            init_gate = int(range_parts[0].strip())
            end_gate = int(range_parts[1].strip())

            new_area = BoardingArea(area_name, area_type)
            current_terminal.boarding_areas.append(new_area)

            # Unique prefix so gate names encode terminal + area
            prefix = current_terminal.name + area_name + "G"
            SetGates(new_area, init_gate, end_gate, prefix)

    return bcn


def GateOccupancy(bcn):
    # Returns a list of [gate_name, occupied, aircraft_id] for every gate
    occupancy_list = []
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                occupancy_list.append([gate.name, gate.occupied, gate.aircraft_id])
    return occupancy_list


def IsAirlineInTerminal(terminal, name):
    # Return False if name is empty
    if name == "":
        return False

    if name in terminal.airlines:
        return True

    return False


def SearchTerminal(bcn, name):
    # Return empty string if name is invalid
    if name == "":
        return ""

    for terminal in bcn.terminals:
        if IsAirlineInTerminal(terminal, name):
            return terminal.name

    # Airline not found in any terminal
    return ""


def AssignGate(bcn, aircraft):
    # 1. Find the terminal for this airline
    req_terminal = SearchTerminal(bcn, aircraft.airline_company)
    if req_terminal == "":
        return -1

    # 2. Determine Schengen type of the origin airport
    if IsSchengenAirport(aircraft.origin_airport):
        req_type = "Schengen"
    else:
        req_type = "non-Schengen"

    # 3. Find first free gate in the correct terminal + area type
    for terminal in bcn.terminals:
        if terminal.name != req_terminal:
            continue
        for area in terminal.boarding_areas:
            if area.type != req_type:
                continue
            for gate in area.gates:
                if not gate.occupied:
                    gate.occupied = True
                    gate.aircraft_id = aircraft.aircraft_id
                    return 0

    # No free gate found
    return -1


