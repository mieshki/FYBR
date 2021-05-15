from app import create_app
import folium
import gpxpy
from main import *
from flask import render_template


app = create_app()

def temp(data):
    global nodes

    i = 0
    print(f'Found {data.ways} ways')
    allWays = []
    try:
        for way in data.ways:
            nodes = way.get_nodes(resolve_missing=True)
            print(f'Nodes no.{i}: {nodes}')
            newWay = []
            for node in nodes:
                newWay.append((node.lat, node.lon))
            #plot_list(nodes, 'red')  # colour[i % 6])
            i += 1
            allWays.append(newWay)
            # print(f'lon={node.lon}, lat={node.lat}')
        # for k, v in way.tags.items():
        #    print(k, v)
    except:
        print('Exception')
    return allWays

@app.route("/")
def hello():
    """start_cords = (54.38714, 18.602002)
    start_map = folium.Map(location=start_cords, zoom_start=14, width='50%', height='50%', left='30%', top='30%')

    gps_track_points = read_gpx_file(GPX_FILE_PATH)
    result = execute_query(create_query_from_list(gps_track_points, 'way'))

    allWays = temp(result)
    for way in allWays:
        folium.vector_layers.PolyLine(locations=way, color='green', weight=5, opacity=0.8).add_to(start_map)

    with open("D:\\Python\\FYBR\\gpx\\hel.gpx", "r") as f:
        gpx1 = gpxpy.parse(f)
        points = gpx1.tracks[0].segments[0].points
        tuplePoints = []
        for point in points:
            tuplePoints.append((point.latitude, point.longitude))
    folium.vector_layers.PolyLine(locations=tuplePoints, color='red', weight=5, opacity=0.8).add_to(start_map)
    start_map.save('app/templates/map.html')"""
    return render_template("base.html")

@app.route('/maps/map.html')
def mapa():
    return render_template('maps/map.html')

@app.route('/auth/login.html')
def login():
    return render_template("auth/login.html")

if __name__ == "__main__":
    app.run(debug=True)
