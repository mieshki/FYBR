import gpxpy
import folium
from app.utilities import MapConfig, OverpassQuery, Overpass
from math import floor
import haversine


def calculate_map_start_point(gpx_file_path):
    parsed_gpx_file = gpxpy.parse(gpx_file_path)
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
    parsed_gpx_file = gpxpy.parse(gpx_file_path)
    points_from_gpx_file = parsed_gpx_file.tracks[0].segments[0].points
    lat_lon_points_tuple = []

    for point in points_from_gpx_file:
        lat_lon_points_tuple.append((point.latitude, point.longitude))

    folium.vector_layers.PolyLine(locations=lat_lon_points_tuple, color=color, weight=width, opacity=opacity).add_to(map)
    folium.Marker(lat_lon_points_tuple[0], popup="<b>start :)</b>", tooltip='Start').add_to(map)
    folium.Marker(lat_lon_points_tuple[len(lat_lon_points_tuple) - 1], popup="<b>koniec :(</b>", tooltip='Koniec').add_to(map)
    folium.TileLayer('openstreetmap').add_to(map)
    folium.TileLayer('Stamen Terrain').add_to(map)

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

def print_cycleways_on_map(data, map, width, opacity):
    highway_list = []
    available_highway = []

    for way in data.ways:
        qualified = 0
        if 'highway' in way.tags:
            nodes_list = []
            for node in way.nodes:
                nodes_list.append((node.lat, node.lon))

            highway_value = way.tags.get('highway')
            highway_list.append((highway_value, nodes_list))

            available_highway.append(highway_value)

            qualified = 1

        if qualified != 1:
            continue
        else:
            qualified = 0

    available_highway = list(dict.fromkeys(available_highway))

    for highway in available_highway:
        feature_group = folium.FeatureGroup(highway)
        for tuple in highway_list:
            if tuple[0] == highway:
                folium.PolyLine(locations=tuple[1], color=map_surface_color(highway), tooltip=highway, weight=width,
                                opacity=opacity).add_to(feature_group)
        feature_group.add_to(map)



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
    surface_list = []
    available_surfaces = []

    for way in data.ways:
        qualified = 0
        if 'surface' in way.tags:
            nodes_list = []
            for node in way.nodes:
                nodes_list.append((node.lat, node.lon))

            surface_value = way.tags.get('surface')
            surface_list.append((surface_value, nodes_list))

            available_surfaces.append(surface_value)

            qualified = 1

        if qualified != 1:
            continue
        else:
            qualified = 0


    available_surfaces = list(dict.fromkeys(available_surfaces))

    for surface in available_surfaces:
        feature_group = folium.FeatureGroup(surface)
        for tuple in surface_list:
            if tuple[0] == surface:
                folium.PolyLine(locations=tuple[1], color=map_surface_color(surface), tooltip=surface, weight=width, opacity=opacity).add_to(feature_group)
        feature_group.add_to(map)

    #folium.LayerControl().add_to(map)



def test():
    time_dif = [0]
    dist_dif_hav_2d = [0]
    dist_dif_vin_2d = [0]
    with open("gpx\\gdansk.gpx", "r") as f:
        parsed_gpx_file = gpxpy.parse(f)
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
    print('Total Time : ', floor(sum(time_dif) / 60), ' min ', int(sum(time_dif) % 60), ' sec ')
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
    print('Total distance: ', int(meters_traveled), 'meters')
    print('Speed: ', '{:.2f}'.format(average_speed / len(dist_dif_hav_2d)), 'km/h')
    #"{:.3f}".format(dist_vin[-1] / 1000)

