import gpxpy
import pandas as pd
#import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import overpy
import plotly.express as px


def create_query_from_list(list, type):
    query_fist = "[out:json];" + type + "[\"surface\"][\"highway\"=\"path\"](around:5,"

    iter = 0
    for element in list:
        iter += 1
        if iter % 50 == 1:
            query_fist += f"{element.latitude}, {element.longitude}, "

    #query_fist += f"{list[0].latitude}, {list[0].longitude}, "

    query_fist = query_fist[:len(query_fist) - 2]
    query_fist += ");"

    query = query_fist + "out body geom;"
    return query


def execute_query(query):
    api = overpy.Overpass()
    print(f'Executing QUERY: {query}')
    output = api.query(query)
    print(f'Result: {output}')
    return output


def read_gpx_file(path_to_file):
    gpx_file = open(
        path_to_file,
        'r')
    gpx = gpxpy.parse(gpx_file)
    #list = pd.DataFrame(columns=['lon', 'lat'])
    points = gpx.tracks[0].segments[0].points

    #for point in points:
    #    list = list.append({'lon': point.longitude, 'lat': point.latitude}, ignore_index=True)

    return points


def plot_list(list, colour):
    table = pd.DataFrame(columns=['longitude', 'latitude'])

    for element in list:
        try:
            table = table.append({'lon': element.longitude, 'lat': element.latitude}, ignore_index=True)
        except:
            table = table.append({'lon': element.lon, 'lat': element.lat}, ignore_index=True)

    # https://www.youtube.com/watch?v=5G-1k4CNChI
    #table_geo = gpd.GeoDataFrame(table, geometry=gpd.points_from_xy(
    #    table.lon,
    #    table.lat))
    #
    #world_data = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #axis = world_data[world_data.continent == 'Africa'].plot(
    #    color = 'lightblue', edgecolor = 'black'
    #)

    #table_geo.plot(ax = axis, color = 'black')
    #plt.title('majne tajtle')

    plt.plot(table['lon'], table['lat'], color=colour)


def hgw(data):
    global nodes

    colour = ['red', 'green', 'yellow', 'orange', 'purple']
    i = 0
    print(f'Found {data.ways} ways')
    try:
        for way in data.ways:
            #nodes = way.get_nodes(resolve_missing=True)
            print(f'Nodes no.{i}: {nodes}')
            plot_list(nodes, 'red')#colour[i % 6])
            i += 1
            #print(f'lon={node.lon}, lat={node.lat}')
        #for k, v in way.tags.items():
        #    print(k, v)
    except:
        print('Exception')

    pass

############### End of declarations ###############

#GPX_FILE_PATH = "C:\\Users\\mieshki\\PycharmProjects\\osm-research\\gpx\\hel.gpx"
GPX_FILE_PATH = "D:\\Python\\FYBR\\gpx\\hel.gpx"

gps_track_points = read_gpx_file(GPX_FILE_PATH)
#result = execute_query(create_query_from_list(gps_track_points, 'way'))
#plot_list(gps_track_points, 'black')


#hgw(result)

#plt.plot(gpxTable['lon'], gpxTable['lat'], color="red")
plt.show()
i = 999


