import tkinter as tk
from tkinter import messagebox
from airport import * # Import all your function
# Global variable to store our list of airports in memory
my_airports = []

# --- 1. INTERFACE FUNCTIONS ---

def refresh_list():
    """Clears the display area and fills it with the updated list"""
    list_box.delete(0, tk.END)
    for a in my_airports:
        status = "Schengen" if a.schengen else "Non-Schengen"
        list_box.insert(tk.END, f"{a.code} - Lat: {a.lat} / Lon: {a.lon} ({status})")

def load_file():
    """Loads the text file"""
    global my_airports
    my_airports = LoadAirports("Airports.txt")
    for a in my_airports:
        SetSchengen(a) # Updates the Schengen status
    refresh_list()

def add_airport():
    """Adds an airport from the text fields"""
    code = entry_code.get().strip().upper()
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        
        new_airport = Airport(code, lat, lon)
        SetSchengen(new_airport)
        AddAirport(my_airports, new_airport)
        
        refresh_list()
        # Clear the fields after adding
        entry_code.delete(0, tk.END)
        entry_lat.delete(0, tk.END)
        entry_lon.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Latitude and longitude must be numbers!")

def remove_airport():
    """Removes the selected row from the list"""
    selection = list_box.curselection() # Gets the clicked row
    if selection:
        index = selection[0]
        code_to_remove = my_airports[index].code
        RemoveAirport(my_airports, code_to_remove)
        refresh_list()

def save_file():
    """Saves only Schengen airports to the file"""
    SaveSchengenAirports(my_airports, "Airports.txt")
    messagebox.showinfo("Success", "Schengen airports saved!")

def show_plot():
    """Displays the matplotlib graph"""
    PlotAirports(my_airports)


# --- 2. WINDOW CREATION (GUI) ---

window = tk.Tk()
window.title("Airport Manager")
window.geometry("400x550")

# --- Add Section ---
tk.Label(window, text="ICAO Code:").pack(pady=(10, 0))
entry_code = tk.Entry(window)
entry_code.pack()

tk.Label(window, text="Latitude:").pack()
entry_lat = tk.Entry(window)
entry_lat.pack()

tk.Label(window, text="Longitude:").pack()
entry_lon = tk.Entry(window)
entry_lon.pack()

tk.Button(window, text="Add this airport", bg="lightgreen", command=add_airport).pack(pady=10)

# --- Display Section (List) ---
tk.Label(window, text="List of airports in memory:").pack()
list_box = tk.Listbox(window, width=50, height=10)
list_box.pack(pady=5)

# --- Action Buttons ---
tk.Button(window, text="1. Load from file", command=load_file).pack(fill='x', padx=20, pady=2)
tk.Button(window, text="2. Remove selection", command=remove_airport).pack(fill='x', padx=20, pady=2)
tk.Button(window, text="3. Show plot", command=show_plot).pack(fill='x', padx=20, pady=2)
tk.Button(window, text="4. Save (Schengen only)", command=save_file).pack(fill='x', padx=20, pady=2)

# Launch the application
window.mainloop()