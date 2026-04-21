from Aircraft import *

def MapFlights(aircrafts):
    aircrafts = LoadArrivals(aircrafts)
    if not aircrafts:
        return -1
    filename = "flights.kml"
    try:
    f = open(filename, "w")

    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write("<Document>\n")

    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        origin = aircraft.origin_airport
        SetSchengen(origin)
        if airports[i].schengen:
            color = "ff00ffff"
        else:
            color = "ffff0000"

            f.write("   <Placemark>\n")
            f.write("   <name>" + str(ac.aircraft_id) + "</name>\n")
            f.write("   <Style><LineStyle><color>" + color + "</color><width>2</width></LineStyle></Style>\n")
            f.write("   <LineString>\n")
            f.write("   <coordinates>\n")

            f.write("   " + str(lon_orig) + "," + str(lat_orig) + ",0 ")
            f.write(str(lon_dest) + "," + str(lat_dest) + ",0\n")
            f.write("   </coordinates>\n")
            f.write("   </LineString>\n")
            f.write("   </Placemark>\n")

        i = i + 1
    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()

    return 0