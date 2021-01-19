import fitnesscalc as ft
import nsga2 as ns


def select(population, offsprings, truck, boxes, total_value, count):
    survivors = {}
    offspring, fitness = ft.evaluate(offsprings, truck, boxes, total_value)
    offspring = ns.rank(offspring, fitness)
    pool = list(population.values()) + list(offspring.values())
    i = 1
    while len(survivors) < count:
        group = [values for values in pool if values['Rank'] == i]

        # If length of the group is lesser append the whole group
        if len(group) <= count - len(survivors):
            j = 0
            for index in range(len(survivors), len(survivors)+len(group)):
                survivors[index] = group[j]
                j += 1

        # If length of the group is bigger than needed, sort according to CD
        else:
            group = sorted(group, key=lambda x: x['CD'], reverse=True)
            j = 0
            for index in range(len(survivors), count):
                survivors[index] = group[j]
                j += 1
        i += 1

    return survivors
