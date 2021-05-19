import copy

from app import create_app
from app.map_helper import *
from app.utilities import *

app = create_app()


@app.route("/")
def hello():
    file_path = "gpx\\hel.gpx"

    map_config = calculate_map_start_point(file_path)

    map = folium.Map(location=map_config.center_point, zoom_start=map_config.zoom, width='100%', height='80%')

    apply_gpx_track_on_map(file_path, map, 'red', 8, 1.0)

    queries_list = []

    # Query na ścieżki rowerowe
    query_cycleways = OverpassQuery(file_path)
    query_cycleways.set_radius(3)
    query_cycleways.add_key_value_tag(('highway', 'cycleway'))
    queries_list.append(query_cycleways)

    # Query na wyciągnięcie informacji o drodze
    query_surfaces = OverpassQuery(file_path)
    query_surfaces.set_radius(3)
    query_surfaces.add_key_value_tag(('surface', '*'))
    queries_list.append(query_surfaces)

    data = Overpass.execute_queries(queries_list)

    print_cycleways_on_map(data, map, 'black', 10, 0.8)
    print_surfaces_no_map(data, map, 10, 0.8)
    # print_overpass_query_results_on_map(data, map, 'green', 6, 0.8)

    return map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)
