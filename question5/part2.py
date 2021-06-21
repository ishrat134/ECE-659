from question5.part1 import get_target_points
from question5.part2b import get_sensor_points
import random
import numpy as np
import question5.part2b as sensor_dist

cost = (300, 170, 65)
types = (100, 70, 30)

dict_cost_types = {300: 100, 170: 70, 65: 30}

# this dictionary contains the sensor no as the key. Its state(0 depicts that the sensor is not active/is removed and
# state 1 depicts that is being used for monitoring, its cost and range.
dict = {}
targets_covered_coord = []

#no of sensors to be thrown
no_of_sensors = sensor_dist.no_of_sensors

def random_distribution_sensor_parameters():
    random_list_cost = []
    for i in range(1, no_of_sensors+1):
        n = random.choice(cost)
        random_list_cost.append(n)
    j = 1
    while j <= len(random_list_cost):
        type = ""
        if random_list_cost[j - 1] == 300:
            type = types.__getitem__(0)
        elif random_list_cost[j - 1] == 170:
            type = types.__getitem__(1)
        elif random_list_cost[j - 1] == 65:
            type = types.__getitem__(2)
        else:
            print("invalid cost")
        ll = [1, random_list_cost[j - 1], type]
        dict[j] = list(ll)
        j = j + 1


def function_to_minimize_cost(dict):
    total_cost = 0
    for i in range(1, len(dict) + 1):
        total_cost = total_cost + (dict[i][0] * dict[i][1])
    return total_cost


def random_neighbor():
    num = np.random.randint(1, no_of_sensors)
    random_sensor = final_sensor_points[num]
    index = final_sensor_points.index(random_sensor)
    return random_sensor, index

#function to check coverage
def coverage(random_sensor, index):
    range_random_sensor = dict[index][2]
    cost_random_sensor = dict[index][1]
    point1 = np.array(random_sensor)
    target_covered = calculate_distance_sensor_to_target(point1, range_random_sensor)

    if target_covered < 1:
        dict[index][0] = 0
        new_cost = function_to_minimize_cost(dict)
        return new_cost

    if target_covered >= 1 and cost_random_sensor == 300:
        range_random_sensor_170 = 170
        target_covered_170 = calculate_distance_sensor_to_target(point1, range_random_sensor_170)
        if (target_covered == target_covered_170):
            dict[index][1] = range_random_sensor
            dict[index][2] = dict_cost_types[170]
            range_random_sensor_65 = 65
            target_covered_65 = calculate_distance_sensor_to_target(point1, range_random_sensor_65)
            if target_covered_65 == target_covered_170:
                dict[index][1] = range_random_sensor
                dict[index][2] = dict_cost_types[65]

    new_cost = function_to_minimize_cost(dict)
    return new_cost


def calculate_distance_sensor_to_target(point1, range_random_sensor):
    target_covered = 0
    for i in targets:
        point2 = np.array(i)
        dist = np.linalg.norm(point1 - point2)
        if (dist <= range_random_sensor):
            target_covered = target_covered + 1
            if i not in targets_covered_coord:
                targets_covered_coord.append(i)
    return target_covered



def control_parameter(fraction):
    return max(0.01, min(1, 1 - fraction))

def acceptance_probability(cost, new_cost, T):
    if new_cost < cost:
        return 1
    else:
        p = np.exp(- (new_cost - cost) / T)
        return p

if __name__ == '__main__':
    maxsteps = 2000
    #distribute targets randomly
    targets = get_target_points()

    #distribute sensors randomly
    final_sensor_points = get_sensor_points()

    print("Total number of sensors thrown: ", no_of_sensors)

    random_distribution_sensor_parameters()
    cost = function_to_minimize_cost(dict)
    print("total initial cost of the sensors after throwing them randomly(this needs to be minimized):", cost, " units")
    states, costs = [], [cost]

    for step in range(maxsteps):
        fraction = step / float(maxsteps)
        T = control_parameter(fraction)
        new_state, index = random_neighbor()
        states.append(new_state)
        new_cost = coverage(new_state, index)
        if acceptance_probability(cost, new_cost, T) > np.random.random():
            cost = new_cost
            state = new_state
            states.append(state)
            costs.append(cost)

    print("Reduced cost after optimization: ", costs[-1], " units")
    ctr_removed_sensors = 0
    for key, value in dict.items():
        if value[0] == 0:
            ctr_removed_sensors = ctr_removed_sensors+1

    print("Number of sensors removed during optimization: ", ctr_removed_sensors)
    print("Number of sensors remaining in the fields after optimization: ",(no_of_sensors-ctr_removed_sensors))

    coverage_given_by_sensors_in_the_network_after_optimization = len(targets_covered_coord)/len(targets)*100
    print("Coverage given by sensors in the network after optimization: ", coverage_given_by_sensors_in_the_network_after_optimization)




