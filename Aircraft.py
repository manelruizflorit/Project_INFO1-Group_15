import os
import matplotlib.pyplot as plt

#We define a new class, aircaft:

class Aircraft:
    def __init__(self, aircraft_id, origin_airport, landing_time, airline_company):
        self.aircraft_id = aircraft_id #string of the aircraft
        self.airline_company = airline_company #3 characters with the ICAO code of the airline
        self.origin_airport = origin_airport #4 characters with the ICAO code of the airport the aircraft is coming from
        self.landing_time = landing_time # 5 characters with the format: hh:mm



def LoadArrivals(filename):
    arrivals_list = []
    linea = False
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as q:
        lines = q.readlines()

        if len(lines) <= 1:
            return []

        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) == 4:
                if len(parts[0]) != 5 or len(parts[1]) != 4 or len(parts[3]) != 3: #we need sharuk to improve our filter on time and numbers
                    linea = True

                elif linea == False:
                    aircraft_id = str(parts[0]).upper()
                    new_aircraft = Aircraft(aircraft_id, parts[1], parts[2], parts[3])
                    arrivals_list.append(new_aircraft)

                else:
                    linea = False

    return arrivals_list


def PlotArrivals(aircrafts):
    """
        Recibe una lista de objetos Aircraft y muestra un gráfico de la frecuencia
        de aterrizajes durante el día (aviones por hora).
        """
    # Check if the list is empty
    if not aircrafts:
        print("Error: The list of aircreafts is empty. The graphic cannot be made.")
        return

    # We create a list with 24 0s, one for each hour of the day
    arrivals_per_hour = [0] * 24

    # Extract the time for every hour and increase the corresponding count
    for aircraft in aircrafts:
        try:
            # Se asume que el atributo de tiempo se llama 'time' y tiene formato "hh:mm"
            if aircrafts.landing_time:
                # Separar la cadena por los dos puntos y tomar la primera parte (la hora)
                hour_str = aircraft.time.split(':')[0]
                hour = int(hour_str)

                # Asegurarse de que la hora sea válida (entre 0 y 23)
                if 0 <= hour <= 23:
                    arrivals_per_hour[hour] += 1
        except (ValueError, AttributeError, IndexError):
            # Si hay un error con el formato de la hora en algún registro, se salta
            continue

    # Eje X: Horas del día (0 a 23)
    hours_per_day = list(range(24))

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(hours_per_day, arrivals_per_hour, color='skyblue', edgecolor='black')

    # Personalizar el gráfico
    plt.title('Arrivals frequency per hour in LEBL', fontsize=14)
    plt.xlabel('Time of the day (00:00 - 23:00)', fontsize=12)
    plt.ylabel('Number of arrivals', fontsize=12)

    # Asegurar que se muestren todas las horas en el eje X
    plt.xticks(hours_per_day)

    # Añadir una cuadrícula para facilitar la lectura
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrar el gráfico
    plt.show()

PlotArrivals(LoadArrivals("Arrivals.txt"))