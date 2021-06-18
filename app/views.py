from flask import Blueprint, render_template, session, redirect, url_for, request
from app.map_helper import *
from app.utilities import *

from . import db
from app.models import Ride, Users
from .map_helper import calculate_map_start_point, apply_gpx_track_on_map, print_surfaces_no_map
from .utilities import OverpassQuery

views = Blueprint('views', __name__)


@views.route('/maps/index')
def mapa():
    return render_template('maps/index.html')

@views.route('/map')
def get_map():
    return render_template('map.html')

@views.route('/test')
def test():
    start_cords = (54.38714, 18.602002)
    start_map = folium.Map(location=start_cords, zoom_start=14, width='100%', height='100%', tiles='OpenStreetMap')
    # dodawanie map
    folium.TileLayer('openstreetmap').add_to(start_map)
    folium.TileLayer('Stamen Terrain').add_to(start_map)
    folium.LayerControl().add_to(start_map)
    mapka = start_map._repr_html_()

    return render_template('maps/new.html', mapa=mapka)


@views.route('/rides')
def get_rides():
    # Check if user is loggedin
    if 'loggedin' in session:
        rides = Ride.query.filter_by(user_id=session['id']).all()
        return render_template('rides.html', rides=rides)
    # User is not loggedin redirect to login page
    return redirect(url_for('auth.login'))


@views.route('/upload_file', methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        if request.files and request.files["file_name"].filename.rsplit('.', 1)[1].lower() in 'gpx':
            bytea_save_file = request.files["file_name"]
            save_ride_to_database(bytea_save_file)
    return redirect(url_for('views.get_rides'))


@views.route('/view/<ride_id>', methods=['POST', 'GET'])
def map_generator(ride_id):
    ride = Ride.query.filter_by(id=ride_id).first()
    mapka = ride.html_map
    time, speed, distance = stats_from_gpx(ride.gpx_file)
    return render_template('maps/new.html', mapa=mapka, time=time, speed=speed, distance=distance)

def stats_from_gpx(gpx_file):
    time_dif = [0]
    dist_dif_hav_2d = [0]
    dist_dif_vin_2d = [0]
    parsed_gpx_file = gpxpy.parse(gpx_file)
    data = parsed_gpx_file.tracks[0].segments[0].points
    for index in range(len(data)):
        if index == 0:
            pass
        else:
            start = data[index - 1]
            stop = data[index]
            distance_hav_2d = haversine.haversine((start.latitude, start.longitude),
                                                  (stop.latitude, stop.longitude)) * 1000
            dist_dif_hav_2d.append(distance_hav_2d)
            time_delta = (stop.time - start.time).total_seconds()
            time_dif.append(time_delta)
    print()
    time = f'Total Time : {floor(sum(time_dif) / 60)} min {int(sum(time_dif) % 60)} sec'
    average_speed = 0
    meters_traveled = 0
    dist_dif_per_sec = []
    #dist_dif_with_timeout = dist_dif_hav_2d > 0.9
    for i in range(0, len(dist_dif_hav_2d)):
        if time_dif[i] != 0:
            meters_traveled += dist_dif_hav_2d[i]
            average_speed += (dist_dif_hav_2d[i] / time_dif[i]) * 3.6
            dist_dif_per_sec.append(dist_dif_hav_2d[i] / time_dif[i])
    #https://towardsdatascience.com/how-tracking-apps-analyse-your-gps-data-a-hands-on-tutorial-in-python-756d4db6715d
    distance = f'Total distance: {int(meters_traveled)} meters'
    speed = f'Speed: ' + '{:.2f}'.format(average_speed / len(dist_dif_hav_2d)) + ' km/h'
    return time, speed, distance


def save_ride_to_database(file_to_save):
    temp = file_to_save.read()

    queries_list = []
    query_surfaces = OverpassQuery(temp)
    query_surfaces.set_radius(1)
    query_surfaces.add_key_value_tag(('surface', '*'))
    queries_list.append(query_surfaces)

    data = Overpass.execute_queries(queries_list)

    map_config = calculate_map_start_point(temp)
    folium_map = folium.Map(location=map_config.center_point, zoom_start=map_config.zoom, width='100%', height='100%')
    apply_gpx_track_on_map(temp, folium_map, 'red', 8, 1.0)

    print_surfaces_no_map(data, folium_map, 10, 0.6)
    print_cycleways_on_map(data, folium_map, 10, 0.6)
    folium.LayerControl().add_to(folium_map)
    html_map = folium_map._repr_html_()
    time, speed, distance = stats_from_gpx(temp)

    ride = Ride(name=file_to_save.filename, gpx_file=temp, html_map=html_map, map_png=map_png, time=time, speed=speed, distance=distance)
    user = Users.query.filter_by(id=session['id']).first()

    db.session.add(ride)
    # adding reference to user
    user.rides.append(ride)
    db.session.commit()
    return redirect(url_for('views.get_rides'))
