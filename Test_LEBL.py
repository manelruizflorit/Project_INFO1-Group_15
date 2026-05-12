from LEBL import *
# ==========================================
# 3. TEST SECTION
# This code only runs if you play this file directly.
# It proves that all our commands above actually work.[cite: 1]
# ==========================================

if __name__ == "__main__":
    print("--- STARTING TESTS ---")

    print("\n1. Testing LoadAirportStructure...")
    bcn_airport = LoadAirportStructure("LEBL.txt")

    if bcn_airport == -1:
        print("ERROR: Could not load LEBL.txt. Make sure the file is in the exact same folder as this Python file.")
    else:
        print("SUCCESS: Loaded Airport " + bcn_airport.code)

        for term in bcn_airport.terminals:
            print("  -> Terminal " + term.name + " has " + str(len(term.boarding_areas)) + " areas and " + str(
                len(term.airlines)) + " airlines logged.")

        print("\n2. Testing Airline Searches...")
        test_airline = "AEE"
        term_found = SearchTerminal(bcn_airport, test_airline)

        if term_found != "":
            print("SUCCESS: Found airline " + test_airline + " in Terminal " + term_found)
        else:
            print("WARNING: Could not find " + test_airline)

        print("\n3. Testing AssignGate...")


        # We build a fake 'dummy' airplane just to test the parking code
        class MockAircraft:
            def __init__(self, flight_id, company, origin):
                self.id = flight_id
                self.airline_company = company
                self.origin_airport = origin


        test_flight = MockAircraft("AEE123", "AEE", "LGAV")

        assignment_result = AssignGate(bcn_airport, test_flight)

        if assignment_result == 0:
            print("SUCCESS: Airplane " + test_flight.id + " found an empty gate and parked.")
        else:
            print("ERROR: Failed to assign gate. No empty gates, or terminal not found.")

        print("\n4. Testing GateOccupancy...")
        all_gates = GateOccupancy(bcn_airport)

        print("Total gates generated in the whole airport: " + str(len(all_gates)))

        # Let's search the list to prove the plane actually parked
        occupied_gates = []
        for g in all_gates:
            if g[1] == True:  # g[1] is the 'occupied' true/false status
                occupied_gates.append(g)

        if len(occupied_gates) > 0:
            print("Occupied Gates Found:")
            for g in occupied_gates:
                print("  -> Gate " + g[0] + " is currently occupied by airplane " + g[2])
        else:
            print("No gates are currently occupied.")
    print("\n--- TESTS FINISHED ---")
