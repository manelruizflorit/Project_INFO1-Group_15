# LEBL.py

# ==========================================
# CLASSES
# ==========================================

from Aircraft import *

#We define the new classes

class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""


class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type  # 'Schengen' or 'non-Schengen'
        self.gates = []


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []  # List of airline ICAO codes


class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []

# ==========================================
# FUNCTIONS
# ==========================================

def SetGates(area, init_gate, end_gate, prefix):

#Updates the list of gates of the boarding area.

    # Return error code -1 if end gate is not greater than init gate
    if end_gate <= init_gate:
        return -1

    # Drop previous list of gates if it existed
    area.gates = []

    for i in range(init_gate, end_gate + 1):
        # Concatenate prefix and gate number
        gate_name = f"{prefix}{i}"
        new_gate = Gate(gate_name)
        area.gates.append(new_gate)

    return 0


def LoadAirlines(terminal, t_name):
    """
    Reads information from the corresponding Airlines text file.
    """
    filename = f"{t_name}_Airlines.txt"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Drop previous list of airlines if it existed[cite: 1]
            terminal.airlines = []

            for line in file:
                # Assuming the format is "Name \t ICAO"[cite: 1]
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    terminal.airlines.append(parts[1].strip())
        return 0
    except FileNotFoundError:
        # Return error code if file does not exist[cite: 1]
        return -1


def LoadAirportStructure(filename):
    """
    Builds a BarcelonaAP object from the LEBL.txt file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not lines:
            return -1

        # First line has the ICAO code[cite: 1]
        airport_code = lines[0].split()[0]
        bcn = BarcelonaAP(airport_code)

        current_terminal = None

        # Loop through the rest of the lines
        for i in range(1, len(lines)):
            line = lines[i].strip()

            if line.startswith("Terminal"):
                parts = line.split()
                t_name = parts[1]
                current_terminal = Terminal(t_name)
                bcn.terminals.append(current_terminal)

                # Load the airlines for this terminal immediately[cite: 1]
                LoadAirlines(current_terminal, t_name)

            elif line.startswith("Area"):
                parts = line.split()
                area_name = parts[1]
                area_type = parts[2]  # 'Schengen' or 'non-Schengen'[cite: 1]

                # Parse the gate range (e.g., 'Gates 1 - 11')[cite: 1]
                gate_str = line.split('Gates')[1].strip()
                init_str, end_str = gate_str.split('-')
                init_g = int(init_str.strip())
                end_g = int(end_str.strip())

                new_area = BoardingArea(area_name, area_type)
                if current_terminal:
                    current_terminal.boarding_areas.append(new_area)

                # Create a unique prefix[cite: 1]
                prefix = f"{current_terminal.name}{area_name}G"
                SetGates(new_area, init_g, end_g, prefix)

        return bcn

    except FileNotFoundError:
        return -1  # Error code if file does not exist[cite: 1]


def GateOccupancy(bcn):
    """
    Returns a list of gates with their names, status, and aircraft ID.
    """
    occupancy_list = []
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                # Compile a dictionary/tuple of the gate's state[cite: 1]
                occupancy_list.append({
                    'name': gate.name,
                    'occupied': gate.occupied,
                    'aircraft_id': gate.aircraft_id
                })
    return occupancy_list


def IsAirlineInTerminal(terminal, name):
    """
    Returns True if the airline is in the terminal's list, False otherwise.
    """
    if not name:
        # Return False and an error code if the string is null[cite: 1]
        return False, -1

    return name in terminal.airlines


def SearchTerminal(bcn, name):
    """
    Returns the name of the terminal where the airline must board.
    """
    for terminal in bcn.terminals:
        # Check using IsAirlineInTerminal[cite: 1]
        result = IsAirlineInTerminal(terminal, name)

        # Handle the tuple return if name was null
        is_in = result[0] if isinstance(result, tuple) else result

        if is_in:
            return terminal.name

    return ""  # Return a null string if not found[cite: 1]


def AssignGate(bcn, aircraft):
    """
    Assigns the first free gate in the correct area to an aircraft.
    """
    # 1. Determine the correct terminal[cite: 1]
    req_terminal_name = SearchTerminal(bcn, aircraft.airline_company)

    if not req_terminal_name:
        return -1  # Airline not found in any terminal

    # 2. Determine Schengen/non-Schengen[cite: 1]
    # NOTE: You will need to import your IsSchengenAirport function from Version 1 here
    # Example: from airport import IsSchengenAirport
    # is_schengen = IsSchengenAirport(aircraft.origin_airport)

    # Placeholder for the Schengen check:
    is_schengen = True
    req_type = "Schengen" if is_schengen else "non-Schengen"

    # 3. Search for the first available gate[cite: 1]
    for terminal in bcn.terminals:
        if terminal.name == req_terminal_name:
            for area in terminal.boarding_areas:
                if area.type == req_type:
                    for gate in area.gates:
                        if not gate.occupied:
                            # Update occupancy and aircraft ID[cite: 1]
                            gate.occupied = True
                            gate.aircraft_id = aircraft.id
                            return 0  # Success

    # Return error code if no free gates are found[cite: 1]
    return -1


# ==========================================
# TEST SECTION
# ==========================================
if __name__ == "__main__":
    print("Testing LEBL Structure...")
    # Make sure you have LEBL.txt, T1_Airlines.txt, and T2_Airlines.txt in the same directory
    bcn_airport = LoadAirportStructure("LEBL.txt")

    if bcn_airport != -1:
        print(f"Successfully loaded airport: {bcn_airport.code}")
        for term in bcn_airport.terminals:
            print(
                f"- {term.name} loaded with {len(term.airlines)} airlines and {len(term.boarding_areas)} boarding areas.")
    else:
        print("Failed to load airport structure. Check file paths.")