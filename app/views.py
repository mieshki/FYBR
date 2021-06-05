from flask import Blueprint, render_template
import folium
import gpxpy

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
