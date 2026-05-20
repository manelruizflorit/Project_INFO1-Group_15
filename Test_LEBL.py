from LEBL import *
if __name__ == "__main__":

    # Tests loading the full airport structure from the file
    print("=" * 50)
    print("TEST: LoadAirportStructure")
    print("=" * 50)

    # Loads the airport structure and checks if it was successful
    bcn = LoadAirportStructure("LEBL.txt")

    if bcn == -1:
        print("ERROR: Could not load LEBL.txt")
    else:
        # Prints the airport code and number of terminals
        print(f"Airport code: {bcn.code}")
        print(f"Number of terminals: {len(bcn.terminals)}")
        for t in bcn.terminals:
            # Prints each terminal's name, loaded airlines, and boarding areas with gate ranges
            print(f"\n  Terminal: {t.name}")
            print(f"  Airlines loaded: {len(t.airlines)}")
            if t.airlines:
                print(f"  First 5 airlines: {t.airlines[:5]}")
            for area in t.boarding_areas:
                print(f"    Area {area.name} [{area.type}]: {len(area.gates)} gates "
                      f"({area.gates[0].name} ... {area.gates[-1].name})")

    # Tests that SetGates returns -1 when the end gate is not greater than the start gate
    print("\n" + "=" * 50)
    print("TEST: SetGates (error case: end <= init)")
    print("=" * 50)
    # Creates a dummy area and calls SetGates with an invalid range
    dummy_area = BoardingArea("X", "Schengen")
    result = SetGates(dummy_area, 10, 5, "TEST")
    print(f"SetGates(10, 5) returned: {result}  (expected -1)")

    # Tests IsAirlineInTerminal with a valid code, an unknown code, and an empty string
    print("\n" + "=" * 50)
    print("TEST: IsAirlineInTerminal")
    print("=" * 50)
    if bcn != -1 and bcn.terminals:
        t = bcn.terminals[0]
        if t.airlines:
            # Checks that a known airline returns True
            test_code = t.airlines[0]
            print(f"'{test_code}' in {t.name}: {IsAirlineInTerminal(t, test_code)}  (expected True)")
        # Checks that an unknown code returns False
        print(f"'XXX' in {t.name}: {IsAirlineInTerminal(t, 'XXX')}  (expected False)")
        # Checks that an empty string returns False
        print(f"'' in {t.name}: {IsAirlineInTerminal(t, '')}  (expected False)")

    # Tests SearchTerminal with a known airline, an unknown one, and verifies the returned terminal name
    print("\n" + "=" * 50)
    print("TEST: SearchTerminal")
    print("=" * 50)
    if bcn != -1:
        if bcn.terminals and bcn.terminals[0].airlines:
            # Checks that a known airline returns the correct terminal name
            code = bcn.terminals[0].airlines[0]
            print(f"SearchTerminal('{code}'): '{SearchTerminal(bcn, code)}'  (expected {bcn.terminals[0].name})")
        # Checks that an unknown airline returns an empty string
        print(f"SearchTerminal('ZZZ'): '{SearchTerminal(bcn, 'ZZZ')}'  (expected '')")

    # Tests GateOccupancy at the start, when all gates should be free
    print("\n" + "=" * 50)
    print("TEST: GateOccupancy (initial state)")
    print("=" * 50)
    if bcn != -1:
        # Counts total, occupied, and free gates
        occ = GateOccupancy(bcn)
        total = len(occ)
        occupied = sum(1 for g in occ if g[1])
        print(f"Total gates: {total}, Occupied: {occupied}, Free: {total - occupied}")

    # Tests AssignGate by loading arrivals and assigning gates to the first 20 aircraft
    print("\n" + "=" * 50)
    print("TEST: AssignGate")
    print("=" * 50)
    if bcn != -1:
        # Loads the arrivals list and skips the test if the file is missing
        arrivals = LoadArrivals("arrivals.txt")
        if not arrivals:
            print("No arrivals loaded (check arrivals.txt). Skipping AssignGate test.")
        else:
            assigned = 0
            failed = 0
            # Tries to assign a gate to each of the first 20 aircraft
            for ac in arrivals[:20]:
                res = AssignGate(bcn, ac)
                if res == 0:
                    assigned += 1
                else:
                    failed += 1
            print(f"Tried to assign 20 aircraft: {assigned} OK, {failed} failed")

            # Prints the number of occupied gates and lists them with their aircraft
            occ = GateOccupancy(bcn)
            occupied = sum(1 for g in occ if g[1])
            print(f"Gates now occupied: {occupied}")
            print("Sample occupied gates:")
            for g in occ:
                if g[1]:
                    print(f"  {g[0]} -> {g[2]}")