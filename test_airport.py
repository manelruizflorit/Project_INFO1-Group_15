# -*- coding: utf-8 -*-
from airport import *

# Marks the start of the Step 2 test block
print("--- Step 2 ---")

# Creates a test airport for LEBL, sets its Schengen status, and prints it to the console
a = Airport("LEBL", 41.297, 2.083)
SetSchengen(a)
PrintAirport(a)

# Loads the full airport list from the file into memory once
my_list = LoadAirports("Files/Airports.txt")

# Adds the LEBL test airport to the loaded list
AddAirport(my_list, a)
print(my_list)

# Creates a second test airport, sets its Schengen status, prints it, and adds it to the list
a1 = Airport("LZER", 44.297, 2.453)
SetSchengen(a1)
PrintAirport(a1)
AddAirport(my_list, a1)


# Marks the start of the Step 4 and 5 test block
print("\n--- Step 4 & 5 ---")

# Prints the total number of airports currently in the list
print(f"Loaded {len(my_list)} airports with decimals.")

# Displays the stacked bar chart of Schengen vs non-Schengen airports
PlotAirports(my_list)

# Saves only the Schengen airports from the list back to the file
SaveSchengenAirports(my_list, "Files/Airports.txt")
print("Schengen list saved to Airports.txt")