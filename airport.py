# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 23:02:17 2026

@author: inesm
"""

import os

# --- STEP 1: CLASS DEFINITION ---
class Airport:
    def __init__(self, code, lat, lon):
        """
        Constructor for the Airport class.
        """
        self.code = code
        self.lat = lat
        self.lon = lon
        self.schengen = False  # Default value

def IsSchengenAirport(code):
    """
    Checks if the ICAO code belongs to a Schengen country.
    """
    if not code:
        return False
    
    # List of prefixes for Schengen countries
    schengen_codes = [
        'LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 
        'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 
        'ES', 'LS'
    ]
    return code[:2].upper() in schengen_codes

def SetSchengen(airport):
    """
    Sets the Schengen attribute of an airport object.
    """
    airport.schengen = IsSchengenAirport(airport.code)

def PrintAirport(airport):
    """
    Prints airport data to the console.
    """
    status = "Schengen" if airport.schengen else "Non-Schengen"
    print(f"ICAO: {airport.code} | Lat: {airport.lat} | Lon: {airport.lon} | Zone: {status}")

# --- STEP 3: FILE & LIST MANAGEMENT ---

def LoadAirports(filename):
    """
    Reads airports from a text file and returns a list of objects.
    """
    airports_list = []

    with open(filename, 'r') as f:
        lines = f.readlines()
        # Skip header, process each line
        for line in lines[1:]:
            parts = line.split()
            if len(parts) == 3:
                code = parts[0]
                lat = parts[1] # Latitude string
                lon = parts[2] # Longitude string
                airports_list.append(Airport(code, lat, lon))
    return airports_list

def SaveSchengenAirports(airports, filename):
    """
    Saves only Schengen airports to a new file.
    """
    # Filter only Schengen airports
    schengen_list = [a for a in airports if IsSchengenAirport(a.code)]

    if not schengen_list:
        return -1 # Error: list is empty
    
    with open(filename, 'w') as f:
        f.write("CODE LAT LON\n")
        for a in schengen_list:
            f.write(f"{a.code} {a.lat} {a.lon}\n")
    return 0 # Success

def NbSchengenAirports(airports, filename):
    
    schengen_list = [a for a in airports if IsSchengenAirport(a.code)]
    return len(schengen_list)

def AddAirport(airports, airport):
    """
    Adds an airport to the list if not already present.
    """
    for a in airports:
        if a.code == airport.code:
            print(f"Airport {airport.code} already in list.")
            return
    airports.append(airport)

def RemoveAirport(airports, code):
    """
    Removes an airport from the list by its code.
    """
    for i in range(len(airports)):
        if airports[i].code == code:
            airports.pop(i)
            return 0 # Success
    return -1 # Error: not found