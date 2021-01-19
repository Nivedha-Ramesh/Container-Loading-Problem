from operator import itemgetter
from copy import deepcopy


def evaluate(population, truck_dimension, boxes, total_value):
    """
    This function uses the S-DBLF algorithm to pack the boxes in the container and calculates the utilization space, the
    number of boxes packed and the total value of the boxes packed onto the container as the fitness values
    :param population: A dictionary of individuals, with order, rotate and values for each box
    :param truck_dimension: The [l, w, h] of the container
    :param boxes: A dictionary of the box number as the key and a list of [l, w, h, vol, value] of the boxes as values
    :return: The population dictionary adn list of fitness values for every individual
    """
    container_vol = truck_dimension[0] * truck_dimension[1] * truck_dimension[2]
    ft = {}
    for key, individual in population.items():
        dblf = [[0, 0, 0] + truck_dimension]
        occupied_vol = 0
        number_boxes = 0
        value = 0
        result = []
        for box_number, r in zip(individual['order'], individual['rotate']):
            dblf = sorted(dblf, key=itemgetter(3))
            dblf = sorted(dblf, key=itemgetter(5))
            dblf = sorted(dblf, key=itemgetter(4))
            for pos in dblf:
                current = deepcopy(pos)
                space_vol = pos[3] * pos[4] * pos[5]
                box_vol = boxes[box_number][3]
                box_value = boxes[box_number][4]
                if r == 0:
                    l, w, h = boxes[box_number][0:3]
                elif r == 1:
                    w, l, h = boxes[box_number][0:3]
                elif r == 2:
                    l, h, w = boxes[box_number][0:3]
                elif r == 3:
                    h, l, w = boxes[box_number][0:3]
                elif r == 4:
                    h, w, l = boxes[box_number][0:3]
                else:
                    w, h, l = boxes[box_number][0:3]
                if space_vol >= box_vol and pos[3] >= l and pos[4] >= w and pos[5] >= h:
                    result.append(pos[0:3] + [l, w, h])
                    occupied_vol += box_vol
                    number_boxes += 1
                    value += box_value
                    top_space = [pos[0], pos[1], pos[2] + h, l, w, pos[5] - h]
                    beside_space = [pos[0], pos[1] + w, pos[2], l, pos[4] - w, pos[5]]
                    front_space = [pos[0] + l, pos[1], pos[2], pos[3] - l, pos[4], pos[5]]
                    dblf.remove(current)
                    dblf.append(top_space)
                    dblf.append(beside_space)
                    dblf.append(front_space)
                    break
        fitness = [round((occupied_vol / container_vol * 100), 2), round((number_boxes / len(list(boxes.keys())) * 100), 2),
                   round((value / total_value * 100), 2)]
        ft[key] = fitness
        population[key]['fitness'] = deepcopy(fitness)
        population[key]['result'] = result
    return population, ft
