"""
This function is used to create the data-set
"""

import json
import random
import boxes as bx

MIN_BOXES = 10
MAX_BOXES = 36
MIN_VALUE = 50
MAX_VALUE = 500
MAX_TRUCK_LEN = 600
MIN_TRUCK_LEN = 50
MAX_TRUCK_WID = 600
MIN_TRUCK_WID = 50
MAX_TRUCK_HT = 600
MIN_TRUCK_HT = 50

truck_dim = [[random.randint(MIN_TRUCK_LEN, MAX_TRUCK_LEN), random.randint(MIN_TRUCK_WID, MAX_TRUCK_WID),
              random.randint(MIN_TRUCK_HT, MAX_TRUCK_HT)] for _ in range(5)]
NUM_BOXES = [
    [random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES),
     random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES)] for _ in range(5)]
dataset = {}
i = 0
for cont, counts in zip(truck_dim, NUM_BOXES):
    for number in counts:
        packages = bx.generateboxes([[0, 0, 0] + cont], number)
        boxes = []
        total_value = 0
        for each in packages:
            l, w, h = each[3:]
            vol = l * w * h
            value = random.randint(MIN_VALUE, MAX_VALUE)
            total_value += value
            boxes.append([l, w, h, vol, value])
        dataset[i] = {'truck dimension': cont, 'number': number, 'boxes': boxes, 'solution': packages,
                      'total value': total_value}
        i += 1

with open('input.json', 'w') as outfile:
    json.dump(dataset, outfile)
