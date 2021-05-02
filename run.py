from app import create_app
import folium
import gpxpy

app = create_app()


@app.route("/")
def hello():
    start_cords = (54.38714, 18.602002)
    start_map = folium.Map(location=start_cords, zoom_start=14, width='40%', height='40%')

    with open("D:\\Python\\FYBR\\gpx\\hel.gpx", "r") as f:
        gpx1 = gpxpy.parse(f)
        points = gpx1.tracks[0].segments[0].points
        tuplePoints = []
        for point in points:
            tuplePoints.append((point.latitude, point.longitude))
    folium.vector_layers.PolyLine(locations=tuplePoints, color='red', weight=5, opacity=0.8).add_to(start_map)
    return start_map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)
