# LEBL.py

# ==========================================
# 1. OUR BUILDING BLOCKS (CLASSES)
# Think of these as blueprints for the objects in our airport.
# ==========================================

class Gate:
    # This runs when we create a new Gate
    def __init__(self, name):
        self.name = name
        self.occupied = False  # By default, a new gate is empty
        self.aircraft_id = ""  # No airplane is parked here yet


class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type  # This will be 'Schengen' or 'non-Schengen'
        self.gates = []  # A blank list to hold the Gate objects later


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []  # A blank list to hold BoardingArea objects
        self.airlines = []  # A blank list to hold airline codes


class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []  # A blank list to hold Terminal objects


# ==========================================
# 2. OUR ACTIONS (FUNCTIONS)
# These are the commands that make our airport work.
# ==========================================

def SetGates(area, start_number, end_number, prefix_text):
    # Check if the end number is mistakenly smaller than the start number[cite: 1]
    if end_number <= start_number:
        return -1  # This is our error code

    # Erase any old gates that might have been in this area[cite: 1]
    area.gates = []

    # Loop from the start number to the end number.
    # (We add +1 because Python's 'range' stops right before the last number)
    for number in range(start_number, end_number + 1):
        # Combine the text and the number. Example: "T1AreaA" + "1" = "T1AreaA1"[cite: 1]
        gate_name = prefix_text + str(number)

        # Create a new Gate object using our blueprint from above
        new_gate = Gate(gate_name)

        # Add this new gate into the area's list of gates
        area.gates.append(new_gate)

    return 0  # 0 means success


def LoadAirlines(terminal, terminal_name):
    # Build the file name, like "T1_Airlines.txt"[cite: 1]
    file_to_open = terminal_name + "_Airlines.txt"

    # We use 'try' so the program doesn't crash if the file is missing
    try:
        # Open the file in 'r' (read) mode
        with open(file_to_open, 'r') as file:

            # Empty the terminal's airline list to start fresh[cite: 1]
            terminal.airlines = []

            # Read the file one line at a time
            for line in file:
                # Remove extra spaces, then split the line wherever there is a Tab space ('\t')[cite: 1]
                pieces = line.strip().split('\t')

                # Make sure the line actually has two pieces (Name and Code)
                if len(pieces) >= 2:
                    # The code is the second piece (index 1). Add it to our list.
                    airline_code = pieces[1].strip()
                    terminal.airlines.append(airline_code)

        return 0  # Success

    except FileNotFoundError:
        return -1  # Error: The file was not found[cite: 1]


def LoadAirportStructure(filename):
    try:
        with open(filename, 'r') as file:
            # Read every line in the file and save it in a list called 'lines'
            lines = file.readlines()

        # If the file is completely empty, return an error
        if len(lines) == 0:
            return -1

        # The very first line (index 0) has the airport code[cite: 1]
        first_line_words = lines[0].split()
        airport_code = first_line_words[0]

        # Create our main Airport object
        my_airport = BarcelonaAP(airport_code)

        # We need a variable to keep track of which terminal we are currently building
        current_terminal = None

        # Loop through all the other lines, starting from line 1
        for i in range(1, len(lines)):
            # Remove invisible characters like "new line" from the text
            line_text = lines[i].strip()

            # If the line starts with the word "Terminal"[cite: 1]
            if line_text.startswith("Terminal"):
                words = line_text.split()
                t_name = words[1]  # The second word is the name (e.g., "T1")

                # Create the terminal and add it to the airport
                current_terminal = Terminal(t_name)
                my_airport.terminals.append(current_terminal)

                # Read the airlines for this terminal from the other text files[cite: 1]
                LoadAirlines(current_terminal, t_name)

            # If the line starts with the word "Area"[cite: 1]
            elif line_text.startswith("Area"):
                words = line_text.split()
                area_name = words[1]  # e.g., "A"
                area_type = words[2]  # e.g., "Schengen"

                # We need to split the line specifically around the word 'Gates' to get the numbers[cite: 1]
                gate_parts = line_text.split('Gates')
                numbers_part = gate_parts[1].strip()  # This gets us something like "1 - 11"

                # Split that piece around the dash symbol to get the start and end numbers[cite: 1]
                start_and_end = numbers_part.split('-')
                start_gate_number = int(start_and_end[0].strip())
                end_gate_number = int(start_and_end[1].strip())

                # Create the Area object and add it to our current terminal
                new_area = BoardingArea(area_name, area_type)
                if current_terminal != None:
                    current_terminal.boarding_areas.append(new_area)

                # Create the prefix text, like "T1" + "A" + "G" = "T1AG"[cite: 1]
                prefix_text = current_terminal.name + area_name + "G"

                # Use our SetGates function to generate all the gates for this area[cite: 1]
                SetGates(new_area, start_gate_number, end_gate_number, prefix_text)

        # Give back the fully built airport object
        return my_airport

    except FileNotFoundError:
        return -1  # Error[cite: 1]


def GateOccupancy(my_airport):
    # We will put all the gate info into this blank list
    occupancy_list = []

    # Go inside the airport to find the terminals...
    for terminal in my_airport.terminals:
        # Go inside each terminal to find the areas...
        for area in terminal.boarding_areas:
            # Go inside each area to find the gates...
            for gate in area.gates:
                # Make a small list of 3 items for this specific gate[cite: 1]
                gate_info = [gate.name, gate.occupied, gate.aircraft_id]

                # Add this small list into our big master list
                occupancy_list.append(gate_info)

    return occupancy_list


def IsAirlineInTerminal(terminal, airline_name):
    # If the user passed a blank name, the rules say to return False and an error code[cite: 1]
    if airline_name == "":
        return False, -1

        # Check if the name exists inside the terminal's list of airlines
    if airline_name in terminal.airlines:
        return True
    else:
        return False


def SearchTerminal(my_airport, airline_name):
    # Check every terminal in the airport
    for terminal in my_airport.terminals:

        # Use our function from above to see if it is in this terminal
        check_result = IsAirlineInTerminal(terminal, airline_name)

        # Because IsAirlineInTerminal can sometimes return two things (False and -1),
        # we check if 'check_result' is a 'tuple' (a group of items).
        if type(check_result) is tuple:
            is_inside = check_result[0]  # Grab just the first item (the True/False part)
        else:
            is_inside = check_result  # Otherwise, it's already just True or False

        # If we found it, return the name of the terminal we are currently looking at[cite: 1]
        if is_inside == True:
            return terminal.name

    # If the loop finishes and we never found it, return a blank string[cite: 1]
    return ""


def AssignGate(my_airport, aircraft):
    # Step 1: Find out which terminal this airplane belongs in[cite: 1]
    required_terminal_name = SearchTerminal(my_airport, aircraft.airline_company)

    # If the terminal name comes back blank, we can't park the plane. Return error.
    if required_terminal_name == "":
        return -1

        # Step 2: Determine if it needs a Schengen or non-Schengen gate[cite: 1]
    # (Note: In the final version, you will hook this up to your Version 1 code.
    # For now, we will pretend every flight is Schengen so the code runs without crashing).
    is_schengen = True

    if is_schengen == True:
        required_type = "Schengen"
    else:
        required_type = "non-Schengen"

    # Step 3: Dig through the airport to find a gate that matches the rules[cite: 1]
    for terminal in my_airport.terminals:
        if terminal.name == required_terminal_name:  # Did we find the right terminal?

            for area in terminal.boarding_areas:
                if area.type == required_type:  # Did we find the right area type?

                    for gate in area.gates:
                        if gate.occupied == False:  # Is the gate empty?

                            # We found an empty gate! Park the plane here.[cite: 1]
                            gate.occupied = True
                            gate.aircraft_id = aircraft.id
                            return 0  # 0 means Success

    # If we searched the whole matching area and found no empty gates, return error[cite: 1]
    return -1

