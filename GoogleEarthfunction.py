def MapAirports(airports):
    # Esta funcion nos permite mostrar en Google Earth lso diferentes
    # aeropuertos de la lista, distinguiendolos por colores entre
    # shengen y no shengen
    if not airports:
        return -1
    try:
    # We create a KML file to edit it.
        with open(filename, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            file.write('<Document>\n')
    # We differentiate from Shengen to non shengen airports with red and blue colors
            i = 0
            while i < len(airports):
                if airports[i].schengen:
                    pin_color = "ff0000ff"
                else:
                    pin_color = "ffff0000"
    # It generates a Placemark for every airport defining it for google Earth
                airport = airports[i]
                file.write('  <Placemark>\n')
                file.write('    <name>' + airport.code + '</name>\n')
                file.write('    <Style>')
                file.write('      <IconStyle>\n')
                file.write('        <color>' + pin_color + '</color>\n')
                file.write('      </IconStyle>\n')
                file.write('    </Style>')
                file.write('    <Point>\n')

                coords = str(airport.lon) + "," + str(airport.lat)
                file.write('      <coordinates>' + coords + '</coordinates>\n')
                file.write('    </Point>\n')
                file.write('  </Placemark>\n')
                i += 1
            file.write('</Document>\n')
            file.write('</kml>\n')
        return 0
    except IOError:
        return -1

from airport import *
filename = 'airports.kml'
airports = [Airport("LEBL", 41.2974, 2.0833), Airport("KJFK", 40.6413, -73.7781)]
result = MapAirports(airports)
if result == 0:
    print("Archivo KML creado correctamente")
else:
    print("Error al crear el archivo")



