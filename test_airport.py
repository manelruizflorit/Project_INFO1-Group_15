# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 23:19:06 2026

@author: inesm
"""
from airport import *

print("Testing Step 2 ")
my_airport = Airport("LEBL", 41.2974, 2.0832)
SetSchengen(my_airport)
PrintAirport(my_airport)
print("TEST when non schengen airports")
my_airport = Airport("KZBL", 45.3453, 9.0895)
SetSchengen(my_airport)
PrintAirport(my_airport)


print("Testing Step 4 ")

# 1. Load from file
# Make sure you have created Airports.txt (see below)
list_of_airports = LoadAirports("Airports.txt")
print(f"Loaded {len(list_of_airports)} airports from file.")

# 2. Add a new airport
new_one = Airport("TRGH", 34.0097, 6.5479) # Paris CDG
AddAirport(list_of_airports, new_one)
print(f"After adding LFPG, total: {len(list_of_airports)}")

# 3. Remove an airport (Example: BIKF if it exists in your file)
res = RemoveAirport(list_of_airports, "BIKF")
if res == 0:
    print("BIKF removed successfully.")

NbSchengen = NbSchengenAirports(list_of_airports, "Schengen_Results.txt")
Nbtotal = len(list_of_airports)



# 4. Save Schengen only
# We must update the Schengen status for all before saving
for a in list_of_airports:
    SetSchengen(a)

status = SaveSchengenAirports(list_of_airports, "Schengen_Results.txt")
if status == 0:
    print("Schengen airports saved to 'Schengen_Results.txt'!")
else:
    print("No Schengen airports to save.")
    
