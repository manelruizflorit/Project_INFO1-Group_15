from LEBL import *
if __name__ == "__main__":

    print("=" * 50)
    print("TEST: LoadAirportStructure")
    print("=" * 50)

    bcn = LoadAirportStructure("LEBL.txt")

    if bcn == -1:
        print("ERROR: Could not load LEBL.txt")
    else:
        print(f"Airport code: {bcn.code}")
        print(f"Number of terminals: {len(bcn.terminals)}")
        for t in bcn.terminals:
            print(f"\n  Terminal: {t.name}")
            print(f"  Airlines loaded: {len(t.airlines)}")
            if t.airlines:
                print(f"  First 5 airlines: {t.airlines[:5]}")
            for area in t.boarding_areas:
                print(f"    Area {area.name} [{area.type}]: {len(area.gates)} gates "
                      f"({area.gates[0].name} ... {area.gates[-1].name})")

    print("\n" + "=" * 50)
    print("TEST: SetGates (error case: end <= init)")
    print("=" * 50)
    dummy_area = BoardingArea("X", "Schengen")
    result = SetGates(dummy_area, 10, 5, "TEST")
    print(f"SetGates(10, 5) returned: {result}  (expected -1)")

    print("\n" + "=" * 50)
    print("TEST: IsAirlineInTerminal")
    print("=" * 50)
    if bcn != -1 and bcn.terminals:
        t = bcn.terminals[0]
        if t.airlines:
            test_code = t.airlines[0]
            print(f"'{test_code}' in {t.name}: {IsAirlineInTerminal(t, test_code)}  (expected True)")
        print(f"'XXX' in {t.name}: {IsAirlineInTerminal(t, 'XXX')}  (expected False)")
        print(f"'' in {t.name}: {IsAirlineInTerminal(t, '')}  (expected False)")

    print("\n" + "=" * 50)
    print("TEST: SearchTerminal")
    print("=" * 50)
    if bcn != -1:
        if bcn.terminals and bcn.terminals[0].airlines:
            code = bcn.terminals[0].airlines[0]
            print(f"SearchTerminal('{code}'): '{SearchTerminal(bcn, code)}'  (expected {bcn.terminals[0].name})")
        print(f"SearchTerminal('ZZZ'): '{SearchTerminal(bcn, 'ZZZ')}'  (expected '')")

    print("\n" + "=" * 50)
    print("TEST: GateOccupancy (initial state)")
    print("=" * 50)
    if bcn != -1:
        occ = GateOccupancy(bcn)
        total = len(occ)
        occupied = sum(1 for g in occ if g[1])
        print(f"Total gates: {total}, Occupied: {occupied}, Free: {total - occupied}")

    print("\n" + "=" * 50)
    print("TEST: AssignGate")
    print("=" * 50)
    if bcn != -1:
        arrivals = LoadArrivals("arrivals.txt")
        if not arrivals:
            print("No arrivals loaded (check arrivals.txt). Skipping AssignGate test.")
        else:
            assigned = 0
            failed = 0
            for ac in arrivals[:20]:
                res = AssignGate(bcn, ac)
                if res == 0:
                    assigned += 1
                else:
                    failed += 1
            print(f"Tried to assign 20 aircraft: {assigned} OK, {failed} failed")

            occ = GateOccupancy(bcn)
            occupied = sum(1 for g in occ if g[1])
            print(f"Gates now occupied: {occupied}")
            print("Sample occupied gates:")
            for g in occ:
                if g[1]:
                    print(f"  {g[0]} -> {g[2]}")

