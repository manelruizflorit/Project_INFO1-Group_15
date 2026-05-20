import tkinter as tk
from tkinter import messagebox
from Aircraft import *
from airport import *
from LEBL import *
from matplotlib import *

# Global variables to store the airport list, flights list, and Barcelona airport structure in memory
my_airports = []
my_flights = []
bcn_airport = None


# Clears the airport display box and refills it with the current list
def refresh_list():
    list_box_airports.delete(0, tk.END)
    for a in my_airports:
        # Formats each airport as a readable string with its Schengen status
        status = "Schengen" if a.schengen else "Non-Schengen"
        list_box_airports.insert(tk.END, f"{a.code} - Lat: {a.lat} / Lon: {a.lon} ({status})")


# Loads the airport list from the file, sets Schengen status for each, and refreshes the display
def load_file():
    global my_airports
    my_airports = LoadAirports("Airports.txt")
    for a in my_airports:
        # Updates the Schengen status for each loaded airport
        SetSchengen(a)
    refresh_list()


# Reads the input fields, creates a new airport, adds it to the list, and clears the fields
def add_airport():
    code = entry_code.get().strip().upper()
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())

        # Creates the airport, sets its Schengen status, and adds it to the list
        new_airport = Airport(code, lat, lon)
        SetSchengen(new_airport)
        AddAirport(my_airports, new_airport)

        refresh_list()
        # Clears the input fields after adding
        entry_code.delete(0, tk.END)
        entry_lat.delete(0, tk.END)
        entry_lon.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Latitude and longitude must be numbers!")


# Removes the airport selected in the list box from the airport list and refreshes the display
def remove_selection():
    # Gets the index of the clicked row
    selection = list_box_airports.curselection()
    if selection:
        index = selection[0]
        code_to_remove = my_airports[index].code
        RemoveAirport(my_airports, code_to_remove)
        refresh_list()


# Saves only the Schengen airports to a file and shows a confirmation message
def save_file():
    SaveSchengenAirports(my_airports, "Schengen_results.txt")
    messagebox.showinfo("Success", "Schengen airports saved!")


# Displays the stacked bar chart of Schengen vs non-Schengen airports
def show_plot():
    PlotAirports(my_airports)


# Generates the KML file and opens the airports in Google Earth
def google_earth():
    ShowAirports(my_airports)


# Clears the arrivals display box and refills it with the current flights list
def refresh_arrivals():
    list_box_arrivals.delete(0, tk.END)
    for f in my_flights:
        # Formats each flight as a readable string with its key fields
        list_box_arrivals.insert(tk.END, f"{f.aircraft_id} {f.origin_airport} {f.landing_time} {f.airline_company}")


# Loads the arrivals list from the file and refreshes the arrivals display
def load_arrivals():
    global my_flights
    my_flights = LoadArrivals("Arrivals.txt")
    refresh_arrivals()


# Saves the current flights list to a file and shows a confirmation message
def save_flights():
    SaveFlights(my_flights, "Saved_flights.txt")
    messagebox.showinfo("Success", "Arrivals saved!")


# Displays the bar chart of arrivals per hour of the day
def plot_arrivals():
    PlotArrivals(my_flights)


# Displays the bar chart of flights per airline
def plot_airlines():
    PlotAirlines(my_flights)


# Displays the stacked bar chart of Schengen vs non-Schengen flights
def plot_types():
    PlotFlightsType(my_flights)


# Generates the KML file and opens all flight paths in Google Earth
def map_flights():
    ShowFlights(my_flights)


# Filters long distance flights and opens their paths in Google Earth
def Longdistanceflights():
    ShowLongDistanceFlights(my_flights)


# Loads the LEBL airport structure from the file and stores it in the global variable
def load_bcn_airport():
    global bcn_airport
    bcn_airport = LoadAirportStructure("LEBL.txt")
    # Shows an error if the file could not be loaded
    if bcn_airport == -1:
        messagebox.showerror("Error", "Could not load LEBL.txt. Make sure the file exists.")
        bcn_airport = None
    else:
        messagebox.showinfo("Success", f"Airport {bcn_airport.code} loaded successfully!")


# Assigns a gate to the flight selected in the arrivals list box
def assign_gate():
    global bcn_airport

    # Checks that the airport structure is loaded before proceeding
    if bcn_airport is None:
        messagebox.showerror("Error", "Airport structure not loaded. Please load LEBL airport first.")
        return

    # Checks that a flight is selected in the list
    selection = list_box_arrivals.curselection()
    if not selection:
        messagebox.showerror("Error", "Please select a flight from the Arrivals list.")
        return

    # Gets the selected aircraft and tries to assign it a gate
    index = selection[0]
    aircraft = my_flights[index]
    result = AssignGate(bcn_airport, aircraft)

    # Shows an error if no gate could be assigned, or a confirmation if successful
    if result == -1:
        messagebox.showerror("Error", f"Could not assign a gate for flight {aircraft.aircraft_id}.\n"
                                      "No free gates available or airline not found.")
    else:
        messagebox.showinfo("Gate Assigned",
                            f"Gate successfully assigned to flight {aircraft.aircraft_id}!")


# Placeholder for the gate occupancy display, to be implemented later
def show_gate_occupancy():
    pass


# ==========================================
# WINDOW SETUP
# ==========================================

# Creates the main window and sets its title, size, and padding
window = tk.Tk()
window.title("Airport Manager")
window.geometry("800x750")
window.configure(padx=10, pady=10)

# Input frame with fields for ICAO code, latitude, and longitude
frame_inputs = tk.LabelFrame(window, text="Add Airport", padx=10, pady=10)
frame_inputs.grid(row=0, column=0, sticky="ew", pady=5)

tk.Label(frame_inputs, text="ICAO").grid(row=0, column=0)
entry_code = tk.Entry(frame_inputs)
entry_code.grid(row=0, column=1)

tk.Label(frame_inputs, text="Latitude ").grid(row=1, column=0)
entry_lat = tk.Entry(frame_inputs)
entry_lat.grid(row=1, column=1)

tk.Label(frame_inputs, text="Longitude ").grid(row=2, column=0)
entry_lon = tk.Entry(frame_inputs)
entry_lon.grid(row=2, column=1)

tk.Button(frame_inputs, text="Add Airport", bg="lightblue", command=add_airport).grid(row=3, column=0, columnspan=2, pady=5)

# List box displaying all currently loaded airports
frame_list_airports = tk.LabelFrame(window, text="Airports", padx=10, pady=10)
frame_list_airports.grid(row=1, column=0, sticky="nsew")

list_box_airports = tk.Listbox(frame_list_airports, height=12)
list_box_airports.pack(fill="both", expand=True)

# List box displaying all currently loaded arrivals
frame_list_arrivals = tk.LabelFrame(window, text="Arrivals", padx=10, pady=10)
frame_list_arrivals.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

list_box_arrivals = tk.Listbox(frame_list_arrivals, height=12)
list_box_arrivals.pack(fill="both", expand=True)

# Buttons for airport operations: load, remove, plot, map, and save
frame_airport = tk.LabelFrame(window, text="Airports", padx=10, pady=10)
frame_airport.grid(row=2, column=0, sticky="ew", pady=5)

tk.Button(frame_airport, text="Load Airports", width=20, command=load_file).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_airport, text="Remove Selection", width=20, command=remove_selection).grid(row=0, column=1, padx=5)
tk.Button(frame_airport, text="Plot Airports", width=20, command=show_plot).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_airport, text="Open Airports on Map", width=20, command=google_earth).grid(row=1, column=1, padx=5)
tk.Button(frame_airport, text="Save Schengen", width=42, command=save_file).grid(row=2, column=0, columnspan=2, pady=5)

# Buttons for flight operations: load, save, plot by hour, by airline, by type, map, and long distance
frame_flights = tk.LabelFrame(window, text="Arrivals", padx=10, pady=10)
frame_flights.grid(row=2, column=1, sticky="nsew", pady=10, padx=10)

tk.Button(frame_flights, text="Load Arrivals", width=20, command=load_arrivals).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_flights, text="Save Flights", width=20, command=save_flights).grid(row=0, column=1)

tk.Button(frame_flights, text="Plot per Hour", width=20, command=plot_arrivals).grid(row=1, column=0, pady=5)
tk.Button(frame_flights, text="Plot per Airline", width=20, command=plot_airlines).grid(row=1, column=1)

tk.Button(frame_flights, text="Plot Schengen", width=20, command=plot_types).grid(row=2, column=0, pady=5)
tk.Button(frame_flights, text="Flights on Map", width=20, command=map_flights).grid(row=2, column=1)

tk.Button(frame_flights, text="Long Distance Flights on Map", width=40, command=Longdistanceflights).grid(row=3, columnspan=2)

# Buttons for gate management: load airport structure, assign gate, and show occupancy
frame_gates = tk.LabelFrame(window, text="Gate Management", padx=10, pady=10)
frame_gates.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5, padx=0)

tk.Button(frame_gates, text="Load LEBL Airport", width=20, bg="lightyellow", command=load_bcn_airport).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_gates, text="Assign Gate", width=20, bg="lightgreen", command=assign_gate).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_gates, text="Show Gate Occupancy", width=20, bg="lightsalmon", command=show_gate_occupancy).grid(row=0, column=2, padx=5, pady=5)

# Configures the window to resize correctly
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

# Starts the main event loop
window.mainloop()