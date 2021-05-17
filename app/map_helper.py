import gpxpy
import folium
from app.utilities import MapConfig


def calculate_map_start_point(gpx_file_path):
    with open(gpx_file_path, "r") as f:
        parsed_gpx_file = gpxpy.parse(f)
        points_from_gpx_file = parsed_gpx_file.tracks[0].segments[0].points
        lat_list = []
        lon_list = []

        for point in points_from_gpx_file:
            lat_list.append(point.latitude)
            lon_list.append(point.longitude)

        #latitude = --
        #longitude = |

        west_wall = min(lat_list)
        east_wall = max(lat_list)
        north_wall = max(lon_list)
        south_wall = min(lon_list)

        middle_lat = ((east_wall + west_wall) / 2)
        middle_lon = ((north_wall + south_wall) / 2)

        zoom_start = 11

        return MapConfig(middle_lat, middle_lon, zoom_start)


def apply_gpx_track_on_map(gpx_file_path, map, color, width, opacity):
    with open(gpx_file_path, "r") as f:
        parsed_gpx_file = gpxpy.parse(f)
        points_from_gpx_file = parsed_gpx_file.tracks[0].segments[0].points
        lat_lon_points_tuple = []

        for point in points_from_gpx_file:
            lat_lon_points_tuple.append((point.latitude, point.longitude))

    folium.vector_layers.PolyLine(locations=lat_lon_points_tuple, color=color, weight=width, opacity=opacity).add_to(map)
    folium.Marker(lat_lon_points_tuple[0], popup="<b>start :)</b>", tooltip='Start').add_to(map)
    folium.Marker(lat_lon_points_tuple[len(lat_lon_points_tuple) - 1], popup="<b>koniec :(</b>", tooltip='Koniec').add_to(map)

def apply_overpass_query_results_on_map(data, map, color, width, opacity):
    temp_list_of_nodes = []
    for way in data.ways:
        for node in way.nodes:
            temp_list_of_nodes.append((node.lat, node.lon))
        folium.vector_layers.PolyLine(locations=temp_list_of_nodes, color=color, weight=width, opacity=opacity).add_to(map)
        temp_list_of_nodes = []
        print(f'way:{way}\n')