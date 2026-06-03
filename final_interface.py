import tkinter as tk
from tkinter import messagebox
from Aircraft import *
from airport import *
from LEBL import *
from matplotlib import *

# Global variables to store the airport list, flights list, and Barcelona airport structure in memory
my_airports = []
my_arrivals = []
my_departures = []
my_flights = []
bcn_airport = None


# Clears the airport display box and refills it with the current list
def refresh_list():
    list_box_airports.delete(0, tk.END)
    for a in my_airports:
        status = "Schengen" if a.schengen else "Non-Schengen"
        list_box_airports.insert(tk.END, f"{a.code} - Lat: {a.lat} / Lon: {a.lon} ({status})")


# Loads the airport list from the file, sets Schengen status for each, and refreshes the display
def load_file():
    global my_airports
    my_airports = LoadAirports("Airports.txt")
    for a in my_airports:
        SetSchengen(a)
    refresh_list()


# Reads the input fields, creates a new airport, adds it to the list, and clears the fields
def add_airport():
    code = entry_code.get().strip().upper()
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        new_airport = Airport(code, lat, lon)
        SetSchengen(new_airport)
        AddAirport(my_airports, new_airport)
        refresh_list()
        entry_code.delete(0, tk.END)
        entry_lat.delete(0, tk.END)
        entry_lon.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Latitude and longitude must be numbers!")


# Removes the airport selected in the list box from the airport list and refreshes the display
def remove_selection():
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


# Clears the arrivals display box and refills it with the current arrivals list
def refresh_arrivals():
    list_box_arrivals.delete(0, tk.END)
    for f in my_arrivals:
        list_box_arrivals.insert(tk.END, f"{f.aircraft_id} {f.origin_airport} {f.landing_time} {f.airline_company}")


# Clears the departures display box and refills it with the current departures list
def refresh_departures():
    list_box_departures.delete(0, tk.END)
    for f in my_departures:
        list_box_departures.insert(tk.END, f"{f.aircraft_id} {f.destination_airport} {f.deparature_time} {f.airline_company}")


# Loads the arrivals list from the file and refreshes the arrivals display
def load_arrivals():
    global my_arrivals
    my_arrivals = LoadArrivals("Arrivals.txt")
    refresh_arrivals()


# Loads the departures list from the file and refreshes the departures display
def load_departures():
    global my_departures
    my_departures = LoadDepartures("Departures.txt")
    refresh_departures()


# Merges arrivals and departures into a single flights list and shows a confirmation message
def merge_movements():
    global my_flights
    result = MergeMovements(my_arrivals, my_departures)
    if result == -1:
        messagebox.showerror("Error", "Could not merge...")
    else:
        my_flights = result
        messagebox.showinfo("Success", f"Merged {len(my_flights)} movements successfully!")


# Saves the current arrivals list to a file and shows a confirmation message
def save_flights():
    SaveFlights(my_arrivals, "Saved_flights.txt")
    messagebox.showinfo("Success", "Arrivals saved!")


# Displays the bar chart of arrivals per hour of the day
def plot_arrivals():
    PlotArrivals(my_arrivals)


# Displays the bar chart of flights per airline
def plot_airlines():
    PlotAirlines(my_arrivals)


# Displays the stacked bar chart of Schengen vs non-Schengen flights
def plot_types():
    PlotFlightsType(my_arrivals)


# Generates the KML file and opens all flight paths in Google Earth
def map_flights():
    ShowFlights(my_arrivals)


# Filters long distance flights and opens their paths in Google Earth
def long_distance_flights():
    ShowLongDistanceFlights(my_arrivals)


# Loads the LEBL airport structure from the file and stores it in the global variable
def load_bcn_airport():
    global bcn_airport
    bcn_airport = LoadAirportStructure("LEBL.txt")
    if bcn_airport == -1:
        messagebox.showerror("Error", "Could not load LEBL.txt. Make sure the file exists.")
        bcn_airport = None
    else:
        messagebox.showinfo("Success", f"Airport {bcn_airport.code} loaded successfully!")


# Assigns a gate to the arrival selected in the arrivals list box
def assign_gate():
    global bcn_airport
    if bcn_airport is None:
        messagebox.showerror("Error", "Airport structure not loaded. Please load LEBL airport first.")
        return
    selection = list_box_arrivals.curselection()
    if not selection:
        messagebox.showerror("Error", "Please select a flight from the Arrivals list.")
        return
    index = selection[0]
    aircraft = my_arrivals[index]
    result = AssignGate(bcn_airport, aircraft)
    if result == -1:
        messagebox.showerror("Error", f"Could not assign a gate for flight {aircraft.aircraft_id}.\n"
                                       "No free gates available or airline not found.")
    else:
        messagebox.showinfo("Gate Assigned", f"Gate successfully assigned to flight {aircraft.aircraft_id}!")


# Assigns gates to all night aircraft and shows a confirmation message
def assign_night_gates():
    global bcn_airport
    if bcn_airport is None:
        messagebox.showerror("Error", "Airport structure not loaded. Please load LEBL airport first.")
        return
    night = NightAircraft(my_departures)  # <-- cambia my_flights por my_departures
    if night == -1:
        messagebox.showerror("Error", "No departures loaded or no night aircraft found.")
        return
    result = AssignNightGates(bcn_airport, night)
    if result == -1:
        messagebox.showerror("Error", "Could not assign night gates.")
    else:
        messagebox.showinfo("Success", f"Night gates assigned to {len(night)} aircraft!")


# Displays the gate occupancy plot for the full day
def show_gate_occupancy():
    global bcn_airport
    if bcn_airport is None:
        messagebox.showerror("Error", "Airport structure not loaded. Please load LEBL airport first.")
        return
    if not my_flights:
        messagebox.showerror("Error", "No merged flights loaded. Please load and merge movements first.")
        return
    PlotDayOccupancy(bcn_airport, my_flights)

#alex project exam
def count_departures_before():
    count = 0
    hour = int(entry_hour.get())
    i = 0
    while i < len(my_departures):
        departure_hour = int(my_departures[i].deparature_time.split(":")[0])
        if departure_hour < hour:
            count += 1
        i += 1
    print(count)
    messagebox.showinfo("Success", f"Number of departures before: {count}")


# ==========================================
# WINDOW SETUP
# ==========================================

window = tk.Tk()
window.title("Airport Manager - LEBL")
window.geometry("900x800")
window.configure(padx=10, pady=10)

# Input frame with fields for ICAO code, latitude, and longitude
frame_inputs = tk.LabelFrame(window, text="Add Airport", padx=10, pady=10)
frame_inputs.grid(row=0, column=0, sticky="ew", pady=5)

tk.Label(frame_inputs, text="ICAO").grid(row=0, column=0)
entry_code = tk.Entry(frame_inputs)
entry_code.grid(row=0, column=1)

tk.Label(frame_inputs, text="Latitude").grid(row=1, column=0)
entry_lat = tk.Entry(frame_inputs)
entry_lat.grid(row=1, column=1)

tk.Label(frame_inputs, text="Longitude").grid(row=2, column=0)
entry_lon = tk.Entry(frame_inputs)
entry_lon.grid(row=2, column=1)

tk.Button(frame_inputs, text="Add Airport", bg="lightblue", command=add_airport).grid(row=3, column=0, columnspan=2, pady=5)

# List boxes for airports, arrivals, and departures
frame_lists = tk.LabelFrame(window, text="Data", padx=10, pady=10)
frame_lists.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5)

# Configures the columns inside frame_lists to expand equally
frame_lists.grid_columnconfigure(0, weight=1)
frame_lists.grid_columnconfigure(1, weight=1)
frame_lists.grid_columnconfigure(2, weight=1)
frame_lists.grid_rowconfigure(1, weight=1)

tk.Label(frame_lists, text="Airports").grid(row=0, column=0)
list_box_airports = tk.Listbox(frame_lists, height=12)
list_box_airports.grid(row=1, column=0, padx=5, sticky="nsew")

tk.Label(frame_lists, text="Arrivals").grid(row=0, column=1)
list_box_arrivals = tk.Listbox(frame_lists, height=12)
list_box_arrivals.grid(row=1, column=1, padx=5, sticky="nsew")

tk.Label(frame_lists, text="Departures").grid(row=0, column=2)
list_box_departures = tk.Listbox(frame_lists, height=12)
list_box_departures.grid(row=1, column=2, padx=5, sticky="nsew")

# Buttons for airport operations
frame_airport = tk.LabelFrame(window, text="Airports", padx=10, pady=10)
frame_airport.grid(row=2, column=0, sticky="ew", padx=5,pady=5)

tk.Button(frame_airport, text="Load Airports", width=20, command=load_file).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_airport, text="Remove Selection", width=20, command=remove_selection).grid(row=0, column=1, padx=5)
tk.Button(frame_airport, text="Plot Airports", width=20, command=show_plot).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_airport, text="Open Airports on Map", width=20, command=google_earth).grid(row=1, column=1, padx=5)
tk.Button(frame_airport, text="Save Schengen", width=42, command=save_file).grid(row=2, column=0, columnspan=2, pady=5)

# Buttons for flight operations
frame_flights = tk.LabelFrame(window, text="Flights", padx=10, pady=10)
frame_flights.grid(row=2, column=1, sticky="nsew", pady=5, padx=10)

tk.Button(frame_flights, text="Load Arrivals", width=20, command=load_arrivals).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_flights, text="Load Departures", width=20, command=load_departures).grid(row=0, column=1, padx=5)
tk.Button(frame_flights, text="Merge Movements", width=42, bg="lightyellow", command=merge_movements).grid(row=1, column=0, columnspan=2, pady=5)

tk.Button(frame_flights, text="Plot per Hour", width=20, command=plot_arrivals).grid(row=2, column=0, pady=5)
tk.Button(frame_flights, text="Plot per Airline", width=20, command=plot_airlines).grid(row=2, column=1)
tk.Button(frame_flights, text="Plot Schengen", width=20, command=plot_types).grid(row=3, column=0, pady=5)
tk.Button(frame_flights, text="Flights on Map", width=20, command=map_flights).grid(row=3, column=1)
tk.Button(frame_flights, text="Long Distance Flights on Map", width=42, command=long_distance_flights).grid(row=4, columnspan=2, pady=5)
tk.Button(frame_flights, text="Save Arrivals", width=42, command=save_flights).grid(row=5, columnspan=2)

#alex project exam
entry_hour = tk.Entry(frame_flights, width=5)
entry_hour.grid(row=6, column=0, pady=5)
tk.Button(frame_flights, text="Departures before introduced hour", command=count_departures_before).grid(row=6, column=1)

# Buttons for gate management
frame_gates = tk.LabelFrame(window, text="Gate Management", padx=10, pady=10)
frame_gates.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

tk.Button(frame_gates, text="Load LEBL Airport", width=20, bg="lightyellow", command=load_bcn_airport).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_gates, text="Assign Gate", width=20, bg="lightgreen", command=assign_gate).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_gates, text="Assign Night Gates", width=20, bg="lightgreen", command=assign_night_gates).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame_gates, text="Show Day Occupancy", width=20, bg="lightsalmon", command=show_gate_occupancy).grid(row=0, column=3, padx=5, pady=5)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()