from Aircraft import *

print("--- Test LoadArrivals ---")
result = LoadArrivals("Arrivals.txt")
print("File not found:", result == [])

result = LoadArrivals("Arrivals.txt")
print("Loaded arrivals:", len(result), "flights")

print("\n--- Test SaveFlights ---")
code = SaveFlights([], "SaveFlights.txt")
print("Empty list returns -1:", code == -1)

code = SaveFlights(result, "Saved_flights.txt")
print("Saved correctly:", code == 0)

print("\n--- Test LoadDepartures ---")
deps = LoadDepartures("Departures.txt")
print("Loaded departures:", len(deps), "flights")

print("\n--- Test MergeMovements ---")
code = MergeMovements([], [])
print("Empty lists return -1:", code == -1)

merged = MergeMovements(result, deps)
print("Merged movements:", len(merged), "flights")

print("\n--- Test NightAircraft ---")
code = NightAircraft([])
print("Empty list returns -1:", code == -1)

night = NightAircraft(merged)
print("Night aircraft:", len(night), "flights")

print("\n--- Test Haversine ---")
dist = Haversine("LEMD")
print("Distance LEMD-LEBL (km):", round(dist, 1))

dist = Haversine("EGLL")
print("Distance EGLL-LEBL (km):", round(dist, 1))

print("\n--- Test LongDistanceArrivals ---")
long = LongDistanceArrivals([])
print("Empty list returns []:", long == [])

long = LongDistanceArrivals(result)
print("Long distance arrivals:", len(long), "flights")

print("\n--- Test MapFlights ---")
code = MapFlights([])
print("Empty list returns -1:", code == -1)

code = MapFlights(result)
print("KML generated correctly:", code == 0)

print("\n--- Test PlotArrivals ---")
PlotArrivals(result)

print("\n--- Test PlotAirlines ---")
PlotAirlines(result)

print("\n--- Test PlotFlightsType ---")
PlotFlightsType(result)