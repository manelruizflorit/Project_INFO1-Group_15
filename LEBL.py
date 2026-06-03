import os
from Aircraft import *

# ==========================================
# CLASSES
# ==========================================

# Represents a single gate with a name, an occupancy boolean, and the ID of the aircraft occupying it
class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False       # Starts as free
        self.aircraft_id = ""       # Empty until a plane is assigned


# Represents a boarding area with a name, a Schengen type, and a list of Gate objects
class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type   # "Schengen" or "non-Schengen"
        self.gates = []


# Represents a terminal with a name, a list of BoardingArea objects, and a list of airline ICAO codes operating in it
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []      # List of ICAO airline codes (3-char)


# Represents the Barcelona airport with its ICAO code and a list of Terminal objects
class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


# ==========================================
# FUNCTIONS
# ==========================================

# Clears any existing gates in the area and fills it with new Gate objects named by combining the prefix and gate number
# Returns -1 if the end gate is not greater than the start gate
def SetGates(area, init_gate, end_gate, prefix):
    # Returns error if the gate range is invalid
    if end_gate <= init_gate:
        return -1

    # Drops the previous list of gates
    area.gates = []

    # Creates a new gate for each number in the range and adds it to the area
    for i in range(init_gate, end_gate + 1):
        gate_name = prefix + str(i)
        area.gates.append(Gate(gate_name))

    return 0


# Reads the airlines file for the given terminal name and updates the terminal's airline list with the ICAO codes found
# Returns -1 if the file doesn't exist, 0 on success
def LoadAirlines(terminal, t_name):
    # Builds the file name from the terminal name
    filename = str(t_name) + "_Airlines.txt"

    try:
        with open(filename, 'r') as f:
            # Drops the previous list of airlines
            terminal.airlines = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Splits by tab and takes the ICAO code in the second column
                parts = line.split('\t')
                if len(parts) >= 2:
                    terminal.airlines.append(parts[1].strip())
        return 0

    except FileNotFoundError:
        return -1


# Reads the airport structure file and builds a BarcelonaAP object with all its terminals, boarding areas, and gates
# Calls SetGates and LoadAirlines along the way, returns -1 if the file doesn't exist
def LoadAirportStructure(filename):
    try:
        with open(filename, 'r') as f:
            lines = [l.rstrip('\n') for l in f.readlines()]
    except FileNotFoundError:
        return -1

    if not lines:
        return -1

    # First line contains the airport code
    bcn = BarcelonaAP(lines[0].split()[0])

    current_terminal = None

    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("Terminal"):
            # Creates a new terminal and loads its airlines from file
            t_name = stripped.split()[1]
            current_terminal = Terminal(t_name)
            bcn.terminals.append(current_terminal)
            LoadAirlines(current_terminal, t_name)

        elif stripped.startswith("Area"):
            if current_terminal is None:
                continue

            # Reads the area name and type from the line
            area_name = stripped.split()[1]
            gates_idx = stripped.index("Gates")
            area_type = stripped[stripped.index(area_name) + len(area_name):gates_idx].strip()

            # Reads the gate range from the line
            after_gates = stripped[gates_idx + len("Gates"):].strip()
            range_parts = after_gates.split('-')
            init_gate = int(range_parts[0].strip())
            end_gate = int(range_parts[1].strip())

            # Creates the boarding area and fills it with gates using a unique prefix
            new_area = BoardingArea(area_name, area_type)
            current_terminal.boarding_areas.append(new_area)
            prefix = current_terminal.name + area_name + "G"
            SetGates(new_area, init_gate, end_gate, prefix)

    return bcn


# Loops through all terminals, boarding areas, and gates and returns a list with each gate's name, occupancy status, and aircraft ID
def GateOccupancy(bcn):
    occupancy_list = []
    # Loops through every terminal, area, and gate to collect their status
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                occupancy_list.append([gate.name, gate.occupied, gate.aircraft_id])
    return occupancy_list


# Checks if a given airline name is in the terminal's airline list
# Returns False and an error code if the name is empty, True if found, False otherwise
def IsAirlineInTerminal(terminal, name):
    # Returns False and error code if the name is empty
    if name == "":
        return False, -1

    # Returns True if the airline is in the list
    if name in terminal.airlines:
        return True

    return False


# Loops through all terminals to find which one the given airline operates in
# Returns the terminal name if found, or an empty string if not
def SearchTerminal(bcn, name):
    # Returns empty string if the airline name is invalid
    if name == "":
        return ""

    # Checks each terminal until the airline is found
    for terminal in bcn.terminals:
        if IsAirlineInTerminal(terminal, name):
            return terminal.name

    return ""


# Finds the correct terminal and gate type for the aircraft, then assigns the first free matching gate
# Returns -1 if no terminal is found or no free gate is available, 0 on success
def AssignGate(bcn, aircraft):
    # Finds the terminal for this airline
    req_terminal = SearchTerminal(bcn, aircraft.airline_company)
    if req_terminal == "":
        return -1

    # Determines whether the flight is Schengen or non-Schengen
    if IsSchengenAirport(aircraft.origin_airport):
        req_type = "Schengen"
    else:
        req_type = "non-Schengen"

    # Loops through terminals and areas to find the first free gate of the correct type
    for terminal in bcn.terminals:
        if terminal.name != req_terminal:
            continue
        for area in terminal.boarding_areas:
            if area.type != req_type:
                continue
            for gate in area.gates:
                # Assigns the gate and marks it as occupied
                if not gate.occupied:
                    gate.occupied = True
                    gate.aircraft_id = aircraft.aircraft_id
                    return 0

    return -1


def AssignNightGates(bcn, aircrafts):
    # Assigns a gate to each aircraft in the list using AssignGate
    # All aircraft in the list are assumed to be departure-only (night aircraft)
    # Returns -1 if the input list is empty, 0 on success
    if not aircrafts:
        return -1

    for aircraft in aircrafts:
        AssignGate(bcn, aircraft)

    return 0


def FreeGate(bcn, id):
    # Finds the gate assigned to the given aircraft ID and sets it to free
    # Returns -1 if the aircraft is not found in any gate, 0 on success
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                if gate.aircraft_id == id:
                    gate.occupied = False
                    gate.aircraft_id = ""
                    return 0

    return -1


def AssignGatesAtTime(bcn, aircrafts, time):
    # Frees gates of aircraft that have already departed before the given time
    # Then assigns gates to aircraft landing in the one-hour window starting at time
    # Returns the number of aircraft that could not be assigned a gate due to full occupancy
    not_assigned = 0

    # Calculates the end of the one-hour period
    hour = int(time.split(':')[0])
    next_hour = (hour + 1) % 24
    time_end = str(next_hour) + ":00"

    # Frees gates of aircraft that have already departed before the current time
    for aircraft in aircrafts:
        if aircraft.deparature_time is not None and aircraft.deparature_time <= time:
            FreeGate(bcn, aircraft.aircraft_id)

    # Assigns gates to aircraft landing in the one-hour period [time, time_end)
    for aircraft in aircrafts:
        if aircraft.landing_time is not None and time <= aircraft.landing_time < time_end:
            result = AssignGate(bcn, aircraft)
            if result == -1:
                not_assigned += 1

    return not_assigned


# Plots the total number of gates assigned per terminal per hour and the number of unassigned aircraft per hour
def PlotDayOccupancy(bcn, aircrafts):
    # Checks if the list is empty
    if not aircrafts:
        print("Error: The aircraft list is empty. The graphic cannot be generated.")
        return

    hours = []
    i = 0
    while i < 24:
        if i < 10:
            hours.append("0" + str(i) + ":00")
        else:
            hours.append(str(i) + ":00")
        i += 1
    not_assigned_per_hour = []

    # One list of gate counts per terminal per hour
    terminal_names = []
    terminal_counts = []
    for terminal in bcn.terminals:
        terminal_names.append(terminal.name)
        terminal_counts.append([])

    for hour in hours:
        # Assigns gates for this hour and records unassigned count
        not_assigned = AssignGatesAtTime(bcn, aircrafts, hour)
        not_assigned_per_hour.append(not_assigned)

        # Counts occupied gates per terminal after assignment
        i = 0
        for terminal in bcn.terminals:
            count = 0
            for area in terminal.boarding_areas:
                for gate in area.gates:
                    if gate.occupied:
                        count += 1
            terminal_counts[i].append(count)
            i += 1

    # Builds the stacked bar chart
    plt.figure(figsize=(14, 6))
    bottom = [0] * 24
    i = 0
    for t_name in terminal_names:
        plt.bar(hours, terminal_counts[i], bottom=bottom, label="Terminal " + t_name, edgecolor="black")
        j = 0
        while j < 24:
            bottom[j] = bottom[j] + terminal_counts[i][j]
            j += 1
        i += 1

    # Plots the unassigned aircraft as a line on top
    plt.plot(hours, not_assigned_per_hour, color="red", marker="o", label="Not assigned", linewidth=2)

    plt.title("Gate occupancy per terminal throughout the day")
    plt.xlabel("Time of the day")
    plt.ylabel("Number of gates assigned / aircraft not assigned")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()
