from flask import Blueprint, render_template, session, redirect, url_for, request
import folium
import gpxpy
from . import db
from app.models import Ride, Users

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
    start_map = folium.Map(location=start_cords, zoom_start=14, width='100%', height='100%')
    track_group = folium.FeatureGroup(name='track').add_to(start_map)
    with open("D:\\Python\\FYBR\\gpx\\hel.gpx", "r") as f:
        gpx1 = gpxpy.parse(f)
        points = gpx1.tracks[0].segments[0].points
        tuplePoints = []
        for point in points:
            tuplePoints.append((point.latitude, point.longitude))
        track_group.add_child(folium.vector_layers.PolyLine(locations=tuplePoints, color='red', weight=5, opacity=0.8))
    folium.LayerControl().add_to(start_map)
    start_map.save('app/templates/map.html')
    return render_template('maps/index.html')

@views.route('/rides')
def get_rides():
    # Check if user is loggedin
    if 'loggedin' in session:
        rides = Ride.query.filter_by(user_id=session['id']).all()
        return render_template('rides.html', rides=rides)
    # User is not loggedin redirect to login page
    return redirect(url_for('auth.login'))

@views.route('/upload_file', methods=["POST"])
def upload_files():
    if request.method == "POST":
        if request.files and request.files["file_name"].filename.rsplit('.',1)[1].lower() in 'gpx':
            bytea_save_file = request.files["file_name"]
            save_ride_to_database(bytea_save_file)
    return redirect(url_for('views.get_rides'))

def save_ride_to_database(file_to_save):
    ride = Ride(bike_id=1, name=file_to_save.filename, gpx_file=file_to_save.read())
    user = Users.query.filter_by(id=session['id']).first()
    db.session.add(ride)
    # adding reference to user
    user.rides.append(ride)
    db.session.commit()
    return redirect(url_for('views.get_rides'))
