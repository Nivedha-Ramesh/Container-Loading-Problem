"""
This module ranks the population into different fronts and also calculates the crowding distance according to NSGA 2
"""


def calc_crowding_dis(solutions):
    obj = len(solutions[0]) - 1
    ranks = {val[3] for val in solutions.values()}
    dict1 = {}
    for rank in ranks:
        group = {k: v for k, v in solutions.items() if v[3] == rank}
        for value in group.values():
            value.append(0)
        for i in range(obj):
            sorted_group = dict(sorted(group.items(), key=lambda x: x[1][i]))
            list1 = list(sorted_group.values())
            list1[0][4] = 5000
            list1[-1][4] = 5000
            for j in range(1, len(list1) - 1):
                list1[j][4] += (list1[j + 1][i] - list1[j - 1][i]) / 100
        dict1.update(group)
    return dict1


def get_dominant_solution(p, q):
    obj = len(p)
    dominance = []
    for i in range(obj):
        if p[i] >= q[i]:
            dominance.append(True)
        else:
            dominance.append(False)

    if True in dominance and False not in dominance:
        return p
    elif True not in dominance and False in dominance:
        return q
    else:
        return None


def rank(population, individuals):
    ranked_solutions = {}
    frontal = set()
    for key, current_solution in individuals.items():
        ranked_solutions[key] = {'Sp': set(), 'Np': 0}

        for index, solution in individuals.items():
            if current_solution[0:3] != solution[0:3]:
                dominant = get_dominant_solution(current_solution[0:3], solution[0:3])
                if dominant is None:
                    continue
                if dominant == current_solution[0:3]:
                    ranked_solutions[key]['Sp'].add(index)
                elif dominant == solution[0:3]:
                    ranked_solutions[key]['Np'] += 1

        if ranked_solutions[key]['Np'] == 0:
            ranked_solutions[key]['Rank'] = 1
            individuals[key].append(1)
            frontal.add(key)

    i = 1
    while len(frontal) != 0:
        sub = set()
        for sol in frontal:
            for dominated_solution in ranked_solutions[sol]['Sp']:
                ranked_solutions[dominated_solution]['Np'] -= 1
                if ranked_solutions[dominated_solution]['Np'] == 0:
                    ranked_solutions[dominated_solution]['Rank'] = i + 1
                    individuals[dominated_solution].append(i + 1)
                    sub.add(dominated_solution)
        i += 1
        frontal = sub

    result = calc_crowding_dis(individuals)

    for key, value in result.items():
        population[key]['Rank'] = value[3]
        population[key]['CD'] = value[4]

    return population
