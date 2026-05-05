class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []

class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = [] # List of ICAO codes

class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type # 'Schengen' or 'non-Schengen'
        self.gates = []

class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""
