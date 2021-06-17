from flask import Blueprint, render_template, session, redirect, url_for, request
import folium
import gpxpy
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


@views.route('/test')
def test():
    start_cords = (54.38714, 18.602002)
    start_map = folium.Map(location=start_cords, zoom_start=14, width='100%', height='100%', tiles='OpenStreetMap')
    """track_group = folium.FeatureGroup(name='track').add_to(start_map)
    with open("D:\\Python\\FYBR\\gpx\\hel.gpx", "r") as f:
        gpx1 = gpxpy.parse(f)
        points = gpx1.tracks[0].segments[0].points
        tuplePoints = []
        for point in points:
            tuplePoints.append((point.latitude, point.longitude))
        track_group.add_child(folium.vector_layers.PolyLine(locations=tuplePoints, color='blue', weight=5, opacity=0.8))"""
    # dodawanie map
    folium.TileLayer('openstreetmap').add_to(start_map)
    folium.TileLayer('Stamen Terrain').add_to(start_map)
    folium.LayerControl().add_to(start_map)
    #start_map.save('app/templates/map.html')
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

@views.route('/upload_file', methods=["GET","POST"])
def upload_files():
    if request.method == "POST":
        if request.files and request.files["file_name"].filename.rsplit('.', 1)[1].lower() in 'gpx':
            bytea_save_file = request.files["file_name"]
            save_ride_to_database(bytea_save_file)
            #TODO  dodać else z flashem
    return redirect(url_for('views.get_rides'))

def save_ride_to_database(file_to_save):
    temp = file_to_save.read()

    map_config = calculate_map_start_point(temp)
    folium_map = folium.Map(location=map_config.center_point, zoom_start=map_config.zoom, width='100%', height='80%')
    apply_gpx_track_on_map(temp, folium_map, 'red', 8, 1.0)

    queries_list = []
    query_surfaces = OverpassQuery(temp)
    query_surfaces.set_radius(1)
    query_surfaces.add_key_value_tag(('surface', '*'))
    queries_list.append(query_surfaces)

    data = Overpass.execute_queries(queries_list)
    print(data)
    print_surfaces_no_map(data, folium_map, 10, 0.8)
    folium_map.save('mapka.html')

"""
    # parsing folium map object to plain html
    html_map = folium_map.get_root().render()
    ride = Ride(name=file_to_save.filename, gpx_file=file_to_save.read(), html_map=html_map)
    user = Users.query.filter_by(id=session['id']).first()

    db.session.add(ride)
    # adding reference to user
    user.rides.append(ride)
    db.session.commit() 
    return redirect(url_for('views.get_rides'))"""
