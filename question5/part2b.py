import random
from shapely.geometry import Polygon, Point

poly = Polygon([ (0, 0), (500, 0), (0, 500), (500,500)])
no_of_sensors = 40
def distribute_sensors(poly, sensors=no_of_sensors):
    sensor_points = []
    min_x, min_y, max_x, max_y = poly.bounds

    while(len(sensor_points)<sensors):
        position = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if(position.within(poly)):
            if position not in sensor_points:
                sensor_points.append(position)
    return sensor_points

def get_sensor_points():
    list_points = distribute_sensors(poly)
    final_points = []
    for point in list_points:
        tup = (int(point.x), int(point.y))
        final_points.append(tup)
    return final_points
