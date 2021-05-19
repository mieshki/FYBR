import gpxpy
import overpy


class MapConfig:
    center_point = ()
    zoom = 0

    def __init__(self, start_point_lat, start_point_lon, zoom):
        self.center_point = (start_point_lat, start_point_lon)
        self.zoom = zoom

    pass

class Overpass:
    @staticmethod
    def execute_queries(queries):
        api = overpy.Overpass()

        all_queries = '[out:json];('
        for query in queries:
            all_queries += query.create_query('way')

        all_queries += '); out body; >; out skel qt;'

        print(f'Executing QUERY: {all_queries}')
        output = api.query(all_queries)
        print(f'Result: {output}')

        return output
    pass

class OverpassQuery:

    def __init__(self, gpx_file_path):
        self.around = 10
        self.list_of_key_values_tags = []
        self.all_points = ''
        self.read_points_from_gpx_file(gpx_file_path)

    def read_points_from_gpx_file(self, gpx_file_path):
        with open(gpx_file_path, "r") as f:
            parsed_gpx_file = gpxpy.parse(f)
            points_from_gpx_file = parsed_gpx_file.tracks[0].segments[0].points

            i = 0
            for point in points_from_gpx_file:
                i += 1
                if i % 200 == 0:
                    self.all_points += f"{point.latitude}, {point.longitude}, "

            self.all_points = self.all_points[:len(self.all_points) - 2]

    def add_key_value_tag(self, key_value_tag):
        self.list_of_key_values_tags.append(key_value_tag)

    def create_query(self, query_type):
        if len(self.all_points) == 0:
            print('No gpx file loaded correctly')
            return

        query = query_type + '('

        query += f'around:' + str(self.around) + ','
        query += self.all_points + ')'

        for key_value in self.list_of_key_values_tags:
            key = key_value[0]
            value = key_value[1]

            if value == '*':
                tag = f'[\"{key}\"]'
            else:
                tag = f'[\"{key}\"=\"{value}\"]'

            query += tag

        query += ';'
        return query

    def set_radius(self, radius):
        self.around = radius
