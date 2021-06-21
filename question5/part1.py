import random
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
poly = Polygon([ (0, 0), (500, 0), (0, 500), (500,500) ])
x_points = []
y_points = []

def distribute_targets(poly, targets=17):
    target_points = []
    min_x, min_y, max_x, max_y = poly.bounds

    while(len(target_points)<targets):
        position = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if(position.within(poly)):
            if position not in target_points:
                target_points.append(position)
    return target_points

def get_target_points():
    list_points = distribute_targets(poly)
    final_points = []
    for point in list_points:
        x_points.append(int(point.x))
        y_points.append(int(point.y))
        tup = (int(point.x), int(point.y))
        final_points.append(tup)
    return final_points


# get_target_points()
# print(x_points)
# print(y_points)
# plt.xlim(0,500)
# plt.ylim(0,500)
# plt.plot(x_points,y_points, 'o', color= 'red')
# plt.show()