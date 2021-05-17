import gpxpy
import overpy


class MapConfig:
    center_point = ()
    zoom = 0

    def __init__(self, start_point_lat, start_point_lon, zoom):
        self.center_point = (start_point_lat, start_point_lon)
        self.zoom = zoom

    pass


class OverpassQuery:
    around = 10
    list_of_key_values_tags = []
    all_points = ''

    def __init__(self, gpx_file_path):
        self.read_points_from_gpx_file(gpx_file_path)

    def read_points_from_gpx_file(self, gpx_file_path):
        with open(gpx_file_path, "r") as f:
            parsed_gpx_file = gpxpy.parse(f)
            points_from_gpx_file = parsed_gpx_file.tracks[0].segments[0].points

            i = 0
            for point in points_from_gpx_file:
                i += 1
                if i % 20 == 0:
                    self.all_points += f"{point.latitude}, {point.longitude}, "

            self.all_points = self.all_points[:len(self.all_points) - 2]

    def add_key_value_tag(self, key_value_tag):
        self.list_of_key_values_tags.append(key_value_tag)

    def create_query(self, query_type):
        query = '[out:json];' + query_type + '(around:' + str(self.around) + ','

        if len(self.all_points) == 0:
            print('No gpx file loaded correctly')
            return
        query += self.all_points + ')'

        for key_value in self.list_of_key_values_tags:
            key = key_value[0]
            value = key_value[1]

            if value == '*':
                tag = f'[\"{key}\"]'
            else:
                tag = f'[\"{key}\"=\"{value}\"]'

            query += tag

        query += ';out body; >; out skel qt;'
        return query

    @staticmethod
    def execute_query(query):
        api = overpy.Overpass()
        print(f'Executing QUERY: {query}')
        output = api.query(query)
        print(f'Result: {output}')
        return output

    def create_and_execute_query(self):
        query = self.create_query('way')
        return self.execute_query(query)

    def set_radius(self, radius):
        self.around = radius
