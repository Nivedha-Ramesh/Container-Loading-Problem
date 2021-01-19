import random


def mutate(offsprings, pm1, pm2,rotation=6):
    """
    This function mutates the offsprings produced by recombination
    :param offsprings: dictionary of the offsprings
    :param pm1: mutation probability constant 1
    :param pm2: mutation probability constant 1
    :param rotation: degrees of allowed rotations
    :return: dictionary of mutated offsprings
    """
    for child in offsprings.values():
        order = child['order']
        rotate = child['rotate']
        if random.uniform(0, 1) <= pm1:
            i = random.randint(1, int(len(order) / 2) + 1)
            j = random.randint(i + 1, int(len(order) - 1))
            order[i:j + 1] = order[j:i - 1:-1]
            rotate[i:j + 1] = rotate[j:i - 1:-1]

        # Second level of mutation
        for i in range(len(rotate)):
            if random.uniform(0, 1) <= pm2:
                rotate[i] = random.randint(0, rotation)

    return offsprings
