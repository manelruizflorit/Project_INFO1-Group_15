# -*- coding: utf-8 -*-
from airport import *

# Test manual
print("--- Step 2 ---")
a = Airport("LEBL", 41.297, 2.083)
SetSchengen(a)
PrintAirport(a)

# 1. On charge la liste initiale UNE SEULE FOIS
my_list = LoadAirports("Files/Airports.txt")

# 2. On ajoute les aéroports à la liste en mémoire
AddAirport(my_list, a)
print(my_list)

a1 = Airport("LZER", 44.297, 2.453)
SetSchengen(a1)
PrintAirport(a1)
AddAirport(my_list, a1)




# Test file & plot
print("\n--- Step 4 & 5 ---")

# --- LIGNE SUPPRIMÉE ICI ---
# my_list = LoadAirports("Airports.txt") <- C'est elle qui effaçait tout !

print(f"Loaded {len(my_list)} airports with decimals.")

# Show Plot
PlotAirports(my_list)

# 3. On sauvegarde le résultat final dans le fichier texte
SaveSchengenAirports(my_list, "Files/Airports.txt")
print("Schengen list saved to Airports.txt")
