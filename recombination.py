import random
from copy import deepcopy
import matplotlib.pyplot as plt


def recombine(parents):
    offsprings = {}
    keys = list(parents.keys())
    random.shuffle(keys)
    for x in range(0, len(parents), 2):
        k1 = random.choice(keys)
        o1 = deepcopy(parents[k1]['order'])
        r1 = deepcopy(parents[k1]['rotate'])
        keys.remove(k1)
        k2 = random.choice(keys)
        o2 = deepcopy(parents[k2]['order'])
        r2 = deepcopy(parents[k2]['rotate'])
        keys.remove(k2)

        i = random.randint(1, int(len(o1) / 2) + 1)
        j = random.randint(i + 1, int(len(o1) - 1))
        # print("Values of i is {} and j is {}".format(i, j))
        co1 = [-1] * len(o1)
        co2 = [-1] * len(o2)
        cr1 = [-1] * len(r1)
        cr2 = [-1] * len(r2)

        co1[i:j + 1] = o1[i:j + 1]
        co2[i:j + 1] = o2[i:j + 1]
        cr1[i:j + 1] = r1[i:j + 1]
        cr2[i:j + 1] = r2[i:j + 1]
        pos = (j + 1) % len(o2)
        for k in range(len(o2)):
            if o2[k] not in co1 and co1[pos] == -1:
                co1[pos] = o2[k]
                pos = (pos + 1) % len(o2)
        pos = (j + 1) % len(o2)
        for k in range(len(o1)):
            if o1[k] not in co2 and co2[pos] == -1:
                co2[pos] = o1[k]
                pos = (pos + 1) % len(o1)
        pos = (j + 1) % len(o2)
        for k in range(len(r2)):
            if cr1[pos] == -1:
                cr1[pos] = r2[k]
                pos = (pos + 1) % len(r2)
        pos = (j + 1) % len(o2)
        for k in range(len(r1)):
            if cr2[pos] == -1:
                cr2[pos] = r1[k]
                pos = (pos + 1) % len(r1)
        offsprings[x] = {'order': deepcopy(co1), 'rotate': deepcopy(cr1)}
        offsprings[x + 1] = {'order': deepcopy(co2), 'rotate': deepcopy(cr2)}
    return offsprings


def select_parents(individuals, num, k):
    parents = {}
    for each in range(num):
        pool = random.sample(individuals, k)
        if pool[0]['Rank'] > pool[1]['Rank']:
            parents[each] = pool[0]
            individuals.remove(pool[0])
        elif pool[0]['Rank'] < pool[1]['Rank']:
            parents[each] = pool[1]
            individuals.remove(pool[1])
        elif pool[0]['CD'] > pool[1]['CD']:
            parents[each] = pool[0]
            individuals.remove(pool[0])
        else:
            parents[each] = pool[1]
            individuals.remove(pool[1])
    return parents


def crossover(population, pc, k=3):
    p = select_parents(list(population.values()), pc, k)
    child = recombine(p)
    return child
