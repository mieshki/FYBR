from app import create_app
from app.map_helper import *
from app.utilities import *

app = create_app()


@app.route("/")
def hello():
    file_path = "gpx\\hel.gpx"

    map_config = calculate_map_start_point(file_path)

    map = folium.Map(location=map_config.center_point, zoom_start=map_config.zoom, width='100%', height='80%')

    apply_gpx_track_on_map(file_path, map, 'red', 7, 1.0)

    query = OverpassQuery(file_path)
    query.set_radius(3)
    #query.add_key_value_tag(('surface', '*'))
    query.add_key_value_tag(('highway', 'cycleway'))

    data = query.create_and_execute_query()

    apply_overpass_query_results_on_map(data, map, 'green', 6, 0.8)

    return map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)
