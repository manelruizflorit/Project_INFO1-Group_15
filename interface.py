from LEBL import *

import tkinter as tk
from tkinter import messagebox
from matplotlib import *

# Global variables
my_airports = []
my_flights = []
bcn_structure = None

# LEBL FUNCTIONS

def load_lebl():
    global bcn_structure
    bcn_structure = LoadAirportStructure("LEBL.txt")
    if bcn_structure == -1:
        messagebox.showerror("Error", "LEBL.txt not found!")
    else:
        print("Barcelona Airport structure loaded.")


def assign_gate_click():
    selection = list_box_arrivals.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Select a flight first!")
        return
    if bcn_structure is None:
        messagebox.showerror("Error", "Airport structure not loaded!")
        return

    index = selection[0]
    flight = my_flights[index]
    result = AssignGate(bcn_structure, flight)

    if result == 0:
        occ = GateOccupancy(bcn_structure)
        assigned_gate = "Unknown"
        for g in occ:
            if g[2] == flight.aircraft_id:
                assigned_gate = g[0]
        messagebox.showinfo("Success", f"Flight {flight.aircraft_id} assigned to Gate {assigned_gate}")
    else:
        messagebox.showerror("Failed", "No gate available or Airline not found in terminals.")


# AIRPORT FUNCTIONS

def refresh_list():
    list_box_airports.delete(0, tk.END)
    for a in my_airports:
        status = "Schengen" if a.schengen else "Non-Schengen"
        list_box_airports.insert(tk.END, f"{a.code} - Lat: {a.lat} / Lon: {a.lon} ({status})")


def load_file():
    global my_airports
    my_airports = LoadAirports("Airports.txt")
    for a in my_airports:
        SetSchengen(a)
    refresh_list()


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


def remove_selection():
    selection = list_box_airports.curselection()
    if selection:
        index = selection[0]
        code_to_remove = my_airports[index].code
        RemoveAirport(my_airports, code_to_remove)
        refresh_list()


def save_file():
    SaveSchengenAirports(my_airports, "Schengen_results.txt")
    messagebox.showinfo("Success", "Schengen airports saved!")


def show_plot():
    PlotAirports(my_airports)


def google_earth():
    ShowAirports(my_airports)

# ARRIVALS FUNCTIONS

def refresh_arrivals():
    list_box_arrivals.delete(0, tk.END)
    for f in my_flights:
        list_box_arrivals.insert(tk.END, f"{f.aircraft_id} {f.origin_airport} {f.landing_time} {f.airline_company}")


def load_arrivals():
    global my_flights
    my_flights = LoadArrivals("Arrivals.txt")
    refresh_arrivals()


def save_flights():
    SaveFlights(my_flights, "Saved_flights.txt")
    messagebox.showinfo("Success", "Arrivals saved!")


def plot_arrivals():
    PlotArrivals(my_flights)


def plot_airlines():
    PlotAirlines(my_flights)


def plot_types():
    PlotFlightsType(my_flights)


def map_flights():
    ShowFlights(my_flights)


def map_long():
    ShowLongDistanceFlights(my_flights)


# WINDOW SETUP


window = tk.Tk()
window.title("Airport Manager")
window.geometry("900x650")
window.configure(padx=10, pady=10)

# Both columns share the window equally
window.grid_columnconfigure(0, weight=1, uniform="half")
window.grid_columnconfigure(1, weight=1, uniform="half")
window.grid_rowconfigure(1, weight=1)

# LEFT COLUMN

# --- Add Airport ---
frame_inputs = tk.LabelFrame(window, text="Add Airport", padx=10, pady=10)
frame_inputs.grid(row=0, column=0, sticky="nsew", pady=5, padx=(0, 5))
frame_inputs.grid_columnconfigure(1, weight=1)

tk.Label(frame_inputs, text="ICAO").grid(row=0, column=0, sticky="w")
entry_code = tk.Entry(frame_inputs)
entry_code.grid(row=0, column=1, sticky="ew", pady=2)

tk.Label(frame_inputs, text="Latitude").grid(row=1, column=0, sticky="w")
entry_lat = tk.Entry(frame_inputs)
entry_lat.grid(row=1, column=1, sticky="ew", pady=2)

tk.Label(frame_inputs, text="Longitude").grid(row=2, column=0, sticky="w")
entry_lon = tk.Entry(frame_inputs)
entry_lon.grid(row=2, column=1, sticky="ew", pady=2)

tk.Button(frame_inputs, text="Add Airport", bg="lightblue",
          command=add_airport).grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

# --- Airports list ---
frame_list_airports = tk.LabelFrame(window, text="Airports", padx=10, pady=10)
frame_list_airports.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
frame_list_airports.grid_rowconfigure(0, weight=1)
frame_list_airports.grid_columnconfigure(0, weight=1)

list_box_airports = tk.Listbox(frame_list_airports)
list_box_airports.grid(row=0, column=0, sticky="nsew")

scrollbar_airports = tk.Scrollbar(frame_list_airports, orient="vertical",
                                  command=list_box_airports.yview)
scrollbar_airports.grid(row=0, column=1, sticky="ns")
list_box_airports.config(yscrollcommand=scrollbar_airports.set)

# --- Airport buttons ---
frame_airport = tk.LabelFrame(window, text="Airport Actions", padx=10, pady=10)
frame_airport.grid(row=2, column=0, sticky="nsew", pady=5, padx=(0, 5))
frame_airport.grid_columnconfigure(0, weight=1)
frame_airport.grid_columnconfigure(1, weight=1)

tk.Button(frame_airport, text="Load Airports",
          command=load_file).grid(row=0, column=0, sticky="ew", padx=3, pady=3)
tk.Button(frame_airport, text="Remove Selection",
          command=remove_selection).grid(row=0, column=1, sticky="ew", padx=3, pady=3)
tk.Button(frame_airport, text="Plot Airports",
          command=show_plot).grid(row=1, column=0, sticky="ew", padx=3, pady=3)
tk.Button(frame_airport, text="Open on Map",
          command=google_earth).grid(row=1, column=1, sticky="ew", padx=3, pady=3)
tk.Button(frame_airport, text="Save Schengen",
          command=save_file).grid(row=2, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

# RIGHT COLUMN

# --- Arrivals list ---
frame_list_arrivals = tk.LabelFrame(window, text="Arrivals", padx=10, pady=10)
frame_list_arrivals.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(5, 0), pady=5)
frame_list_arrivals.grid_rowconfigure(0, weight=1)
frame_list_arrivals.grid_columnconfigure(0, weight=1)

list_box_arrivals = tk.Listbox(frame_list_arrivals)
list_box_arrivals.grid(row=0, column=0, sticky="nsew")

scrollbar_arrivals = tk.Scrollbar(frame_list_arrivals, orient="vertical",
                                  command=list_box_arrivals.yview)
scrollbar_arrivals.grid(row=0, column=1, sticky="ns")
list_box_arrivals.config(yscrollcommand=scrollbar_arrivals.set)

# --- Arrivals buttons ---
frame_flights = tk.LabelFrame(window, text="Arrivals Actions", padx=10, pady=10)
frame_flights.grid(row=2, column=1, sticky="nsew", padx=(5, 0), pady=5)
frame_flights.grid_columnconfigure(0, weight=1)
frame_flights.grid_columnconfigure(1, weight=1)

tk.Button(frame_flights, text="Load Arrivals",
          command=load_arrivals).grid(row=0, column=0, sticky="ew", padx=3, pady=3)
tk.Button(frame_flights, text="Save Flights",
          command=save_flights).grid(row=0, column=1, sticky="ew", padx=3, pady=3)

tk.Button(frame_flights, text="Plot per Hour",
          command=plot_arrivals).grid(row=1, column=0, sticky="ew", padx=3, pady=3)
tk.Button(frame_flights, text="Plot per Airline",
          command=plot_airlines).grid(row=1, column=1, sticky="ew", padx=3, pady=3)

tk.Button(frame_flights, text="Plot Schengen",
          command=plot_types).grid(row=2, column=0, sticky="ew", padx=3, pady=3)
tk.Button(frame_flights, text="Flights on Map",
          command=map_flights).grid(row=2, column=1, sticky="ew", padx=3, pady=3)

tk.Button(frame_flights, text="Long Distance Flights on Map",
          command=map_long).grid(row=3, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

tk.Button(frame_flights, text="ASSIGN GATE", bg="orange", font=("Arial", 11, "bold"),
          command=assign_gate_click).grid(row=4, column=0, columnspan=2, sticky="ew", padx=3, pady=8)

# START

load_lebl()
window.mainloop()

