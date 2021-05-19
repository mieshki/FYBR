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

def print_overpass_query_results_on_map(data, map, color, width, opacity):
    temp_list_of_nodes = []
    for way in data.ways:
        for node in way.nodes:
            temp_list_of_nodes.append((node.lat, node.lon))
        folium.vector_layers.PolyLine(locations=temp_list_of_nodes, color=color, weight=width, opacity=opacity).add_to(map)
        temp_list_of_nodes = []
        print(f'way:{way}\n')

def generate_tooltip(way):
    tooltip = ''
    for key in way.tags.keys():
        tooltip += f'\"{key}\"=\"{way.tags[key]}\"<br>'
    return tooltip

def print_cycleways_on_map(data, map, color, width, opacity):
    temp_list_of_nodes = []
    for way in data.ways:
        qualified = 0
        if 'highway' in way.tags:
            if way.tags['highway'] == 'cycleway':
                qualified = 1

        if qualified != 1:
            continue
        else:
            qualified = 0

        for node in way.nodes:
            temp_list_of_nodes.append((node.lat, node.lon))
        folium.vector_layers.PolyLine(locations=temp_list_of_nodes, color=color, weight=width, opacity=opacity, tooltip=generate_tooltip(way)).add_to(map)
        temp_list_of_nodes = []

        tags_tooltip = ''
        print(f'way:{way}\n')
    pass

def map_surface_color(value):
    color = 'darkpurple'
    if value == 'asphalt':
        color = 'black'
    elif value == 'unpaved':
        color = 'darkred'
    elif value == 'paved':
        color = 'orange'
    elif value == 'ground':
        color = 'lightgray'
    elif value == 'concrete':
        color = 'gray'
    elif value == 'gravel':
        color = 'darkblue'
    elif value == 'cobblestone':
        color = 'beige'

    return color

def print_surfaces_no_map(data, map, width, opacity):
    temp_list_of_nodes = []

    for way in data.ways:
        qualified = 0
        if 'surface' in way.tags:
            qualified = 1

        if qualified != 1:
            continue
        else:
            qualified = 0

        for node in way.nodes:
            temp_list_of_nodes.append((node.lat, node.lon))
        folium.vector_layers.PolyLine(locations=temp_list_of_nodes, color=map_surface_color(way.tags['surface']), weight=width, opacity=opacity, tooltip=generate_tooltip(way)).add_to(map)
        temp_list_of_nodes = []
        print(f'way:{way}\n')
