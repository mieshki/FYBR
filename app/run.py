import copy
from app import create_app
import folium
import gpxpy
from main import *
from flask import render_template

from app import create_app
from app.map_helper import *
from app.utilities import *

##

import gpxpy
from geopy import distance
from math import sqrt, floor
import haversine

##

app = create_app()

def test():
    time_dif = [0]
    dist_dif_hav_2d = [0]

    with open("gpx\\gdansk.gpx", "r") as f:
        parsed_gpx_file = gpxpy.parse(f)
        data = parsed_gpx_file.tracks[0].segments[0].points

    for index in range(len(data)):
        if index == 0:
            pass
        else:
            start = data[index - 1]
            stop = data[index]
            distance_hav_2d = haversine.haversine((start.latitude, start.longitude), (stop.latitude, stop.longitude)) * 1000
            dist_dif_hav_2d.append(distance_hav_2d)
            time_delta = (stop.time - start.time).total_seconds()
            time_dif.append(time_delta)

    print('Total Time : ', floor(sum(time_dif) / 60), ' min ', int(sum(time_dif) % 60), ' sec ')
    average_speed = 0
    meters_traveled = 0
    dist_dif_per_sec = []

    for i in range(0, len(dist_dif_hav_2d)):
        if time_dif[i] != 0:
            meters_traveled += dist_dif_hav_2d[i]
            average_speed += (dist_dif_hav_2d[i] / time_dif[i]) * 3.6
            dist_dif_per_sec.append(dist_dif_hav_2d[i] / time_dif[i])

    #https://towardsdatascience.com/how-tracking-apps-analyse-your-gps-data-a-hands-on-tutorial-in-python-756d4db6715d
    print('Total distance: ', int(meters_traveled), 'meters')
    print('Speed: ', '{:.2f}'.format(average_speed / len(dist_dif_hav_2d)), 'km/h')

@app.route("/")
def hello():
    test()
    file_path = "gpx\\hel.gpx"

    map_config = calculate_map_start_point(file_path)

    map = folium.Map(location=map_config.center_point, zoom_start=map_config.zoom, width='100%', height='80%')

    apply_gpx_track_on_map(file_path, map, 'red', 8, 1.0)

    queries_list = []

    # Query na ścieżki rowerowe
    query_cycleways = OverpassQuery(file_path)
    query_cycleways.set_radius(1)
    query_cycleways.add_key_value_tag(('highway', 'cycleway'))
    queries_list.append(query_cycleways)

    # Query na wyciągnięcie informacji o drodze
    query_surfaces = OverpassQuery(file_path)
    query_surfaces.set_radius(1)
    query_surfaces.add_key_value_tag(('surface', '*'))
    queries_list.append(query_surfaces)

    ##data = Overpass.execute_queries(queries_list)

    ##print_cycleways_on_map(data, map, 'black', 10, 0.8)
    ##print_surfaces_no_map(data, map, 10, 0.8)
    # print_overpass_query_results_on_map(data, map, 'green', 6, 0.8)

    #return map._repr_html_()
    map.save('app/templates/maps/map.html')
    return render_template("base.html")

@app.route('/maps/index.html')
def mapa():
    return render_template('maps/index.html')

@app.route('/auth/login.html')
def login():
    return render_template("auth/login.html")

if __name__ == "__main__":
    app.run(debug=True)
