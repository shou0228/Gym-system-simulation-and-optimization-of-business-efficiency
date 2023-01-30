import random as rd
import numpy as np
from copy import deepcopy
from multiprocessing.pool import Pool
import matplotlib.pyplot as plt

# parameters
CLIENT_ARRIVAL_RATES = 0.8  # Poisson rate per min. /10  0.8
TIME = 60*18  # how many hours
NO_MENU_RATE = 0.3  # no menu
INITIAL_SOL = {'benchpress': 4, 'dumbbell': 15, 'butterfly': 3, 'cable': 5 * 4, 'squat': 5, 'bent_row': 2,
               'dy_row': 5, 'triangle_row': 4, 'leg_press': 5, 'glut_m': 5, 'hip_thrust': 2, 'leg_stretch': 3,
               'shoulder_press': 3, 'incline_chest': 3,  'down_pull': 3, 'biceps_curl': 2}
MAX_COST = 7_500_000
# List of equipment available
PARAMETER_EQUIPMENT = {
    'benchpress':     {'No.': 8, 'Using': [], 'Waiting': [], 'cost': 48_000, 'total_wait': 0, 'total_use': 0},   # 臥推架
    'dumbbell':       {'No.': 30, 'Using': [], 'Waiting': [], 'cost': 53_000, 'total_wait': 0, 'total_use': 0},  # 啞鈴區
    'butterfly':      {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 45_000, 'total_wait': 0, 'total_use': 0},  # 蝴蝶機
    'cable':          {'No.': 5 * 4, 'Using': [], 'Waiting': [], 'cost': 75_000, 'total_wait': 0, 'total_use': 0},  # cable機  cost:300_000 / 4
    'squat':          {'No.': 10, 'Using': [], 'Waiting': [], 'cost': 99_111, 'total_wait': 0, 'total_use': 0},  # 深蹲架
    'bent_row':       {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 45_000, 'total_wait': 0, 'total_use': 0},  # 俯身划船機
    'dy_row':         {'No.': 10, 'Using': [], 'Waiting': [], 'cost': 121_970, 'total_wait': 0, 'total_use': 0},  # DY-ROW
    'triangle_row':   {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 80_970, 'total_wait': 0, 'total_use': 0},  # 後三角划船機
    'leg_press':      {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 156_970, 'total_wait': 0, 'total_use': 0},  # 腿推機
    'glut_m':         {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 90_000, 'total_wait': 0, 'total_use': 0},  # 腿後彎舉機
    'hip_thrust':     {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 57_851, 'total_wait': 0, 'total_use': 0},  # 臀推機
    'leg_stretch':    {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 85_102, 'total_wait': 0, 'total_use': 0},  # 腿伸展機
    'shoulder_press': {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 90_000, 'total_wait': 0, 'total_use': 0},  # 肩推機
    'incline_chest':  {'No.': 3, 'Using': [], 'Waiting': [], 'cost': 39_582, 'total_wait': 0, 'total_use': 0},  # 上斜胸推機
    'down_pull':      {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 80_970, 'total_wait': 0, 'total_use': 0},  # 滑輪下拉機
    'biceps_curl':    {'No.': 5, 'Using': [], 'Waiting': [], 'cost': 80_970, 'total_wait': 0, 'total_use': 0}}  # 二頭彎舉機
SETS_WORKOUT = {'push':  ['ps-1', 'ps-2', 'ps-3', 'ps-4', 'ps-5', 'ps-6', 'ps-7', 'ps-8'],
                'pull':  ['pl-1', 'pl-2', 'pl-3', 'pl-4', 'pl-5', 'pl-6', 'pl-7'],
                'leg':   ['lg-1', 'lg-2', 'lg-3', 'lg-4', 'lg-5'],
                'push2': ['ps2-1', 'ps2-2', 'ps2-3', 'ps2-4', 'ps2-5', 'ps2-6', 'ps2-7', 'ps2-8'],
                'pull2': ['pl2-1', 'pl2-2', 'pl2-3', 'pl2-4', 'pl2-5']}
SETS_WORKOUT_LIST = ['pull', 'push', 'leg', 'pull2', 'push2']
ALL_ACTIONS = ['ps-1', 'ps-2', 'ps-3', 'ps-4', 'ps-5', 'ps-6', 'ps-7', 'ps-8',
               'pl-1', 'pl-2', 'pl-3', 'pl-4', 'pl-5', 'pl-6', 'pl-7',
               'lg-1', 'lg-2', 'lg-3', 'lg-4', 'lg-5',
               'ps2-1', 'ps2-2', 'ps2-3', 'ps2-4', 'ps2-5', 'ps2-6', 'ps2-7', 'ps2-8',
               'pl2-1', 'pl2-2', 'pl2-3', 'pl2-4', 'pl2-5']
EQUIPMENT_USE = {
    'ps-1':  'benchpress', 'ps-2': 'squat', 'ps-3': 'dumbbell', 'ps-4': 'dumbbell',
    'ps-5':  'butterfly', 'ps-6': 'cable', 'ps-7': 'dumbbell', 'ps-8': 'cable',
    'pl-1':  'squat', 'pl-2': 'bent_row', 'pl-3': 'dy_row', 'pl-4': 'triangle_row',
    'pl-5':  'butterfly', 'pl-6': 'dumbbell', 'pl-7': 'cable',
    'lg-1':  'leg_press', 'lg-2': 'glut_m', 'lg-3': 'hip_thrust', 'lg-4': 'glut_m', 'lg-5': 'leg_stretch',
    'ps2-1': 'shoulder_press', 'ps2-2': 'dumbbell', 'ps2-3': 'incline_chest', 'ps2-4': 'cable',
    'ps2-5': 'cable', 'ps2-6': 'cable', 'ps2-7': 'cable', 'ps2-8': 'cable',
    'pl2-1': 'down_pull', 'pl2-2': 'dy_row', 'pl2-3': 'dumbbell', 'pl2-4': 'biceps_curl', 'pl2-5': 'dumbbell'
}
TIME_USE = {
    'ps-1':  (14, 2), 'ps-2': (8, 1.2), 'ps-3': (11, 0.5), 'ps-4': (6, 0.5),
    'ps-5':  (5, 0.5), 'ps-6': (7, 0.5), 'ps-7': (11, 0.5), 'ps-8': (8, 0.5),
    'pl-1':  (13, 0.5), 'pl-2': (7, 2), 'pl-3': (11, 1), 'pl-4': (8, 0.5),
    'pl-5': (9, 0.5), 'pl-6': (7, 0.5), 'pl-7': (5, 0.5),
    'lg-1':  (15, 0.5), 'lg-2': (8, 0.5), 'lg-3': (8, 0.5), 'lg-4': (12, 0.5), 'lg-5': (7, 0.5),
    'ps2-1': (9, 0.8), 'ps2-2': (7, 1.9), 'ps2-3': (6, 1.7), 'ps2-4': (6, 0.8),
    'ps2-5': (6, 0.5), 'ps2-6': (6, 0.5), 'ps2-7': (9, 0.5), 'ps2-8': (6, 0.5),
    'pl2-1': (10, 0.9), 'pl2-2': (7, 2.1), 'pl2-3': (12, 0.5), 'pl2-4': (10, 2.4), 'pl2-5': (9, 1)
}
PERSON = {'No.': 0, 'set': '', 'menu': [], 'time_remaining': [], 'wait': 0, 'workout_time': 0}


def simulation(sol, rate=0.8):
    time = 0
    num = 0
    in_gym = []
    record = []
    total_wait = 0
    total_use = 0
    EQUIPMENT = deepcopy(PARAMETER_EQUIPMENT)
    for i in EQUIPMENT:
        EQUIPMENT[i]['No.'] = sol[i]

    while time < TIME:
        inside = 0

        # generate arrivals
        arrivals = np.random.poisson(rate)
        arrivals = [deepcopy(PERSON) for _ in range(arrivals)]
        for i in arrivals:
            num += 1
            i['No.'] = num
            if rd.uniform(0,1) < NO_MENU_RATE:
                i['set'] = 'No menu'
                actions = rd.choice([5, 6, 7, 8])
                i['menu'] = rd.sample(ALL_ACTIONS, actions)
            else:
                i['set'] = rd.choice(SETS_WORKOUT_LIST)
                i['menu'] = deepcopy(SETS_WORKOUT[i['set']])
            i['time_remaining'] = [max(1, int(np.random.normal(loc=TIME_USE[j][0], scale=TIME_USE[j][1])))
                                   for j in i['menu']]
            n = 1
            while True:
                if rd.uniform(0, 1) > 1 - min(1, max(0, EQUIPMENT[EQUIPMENT_USE[i['menu'][0]]]['No.'] / \
    ((len(EQUIPMENT[EQUIPMENT_USE[i['menu'][0]]]['Waiting']) + 1)**(1/n)))) or n > 10:
                    EQUIPMENT[EQUIPMENT_USE[i['menu'][0]]]['Waiting'].append(i)
                    break
                else:
                    i['menu'].append(i['menu'][0])
                    i['menu'].pop(0)
                    i['time_remaining'].append(i['time_remaining'][0])
                    i['time_remaining'].pop(0)
                    n += 1

        # workout
        for i in EQUIPMENT:
            while len(EQUIPMENT[i]['Using']) < EQUIPMENT[i]['No.']:  # if there are empty slots on equipment
                if not EQUIPMENT[i]['Waiting']:
                    break
                EQUIPMENT[i]['Using'].append(EQUIPMENT[i]['Waiting'][0])
                EQUIPMENT[i]['Waiting'].pop(0)

            # using the equipment
            for j in EQUIPMENT[i]['Using']:
                j['time_remaining'][0] -= 1
                j['workout_time'] += 1
                if j['time_remaining'][0] <= 0:  # done with equipment
                    j['menu'].pop(0)
                    j['time_remaining'].pop(0)
                    if j['menu']:  # if there are any actions remaining, then to next equipment
                        n = 1
                        while True:
                            if rd.uniform(0, 1) > 1 - min(1, max(0, EQUIPMENT[EQUIPMENT_USE[j['menu'][0]]]['No.'] / \
    ((len(EQUIPMENT[EQUIPMENT_USE[j['menu'][0]]]['Waiting']) + 1) ** (1 / n)))) or n > 10:
                                if len(EQUIPMENT[EQUIPMENT_USE[j['menu'][0]]]['Using']) <= EQUIPMENT[EQUIPMENT_USE[j['menu'][0]]]['No.']:
                                    EQUIPMENT[EQUIPMENT_USE[j['menu'][0]]]['Using'].append(j)
                                else:
                                    EQUIPMENT[EQUIPMENT_USE[j['menu'][0]]]['Waiting'].append(j)
                                break
                            else:
                                j['menu'].append(j['menu'][0])
                                j['menu'].pop(0)
                                j['time_remaining'].append(j['time_remaining'][0])
                                j['time_remaining'].pop(0)
                                n += 1
                    else:
                        wait_ratio = j['wait'] / (j['wait'] + j['workout_time'])
                        record.append(wait_ratio)
                        total_wait += j['wait']
                        total_use += j['workout_time']
                    EQUIPMENT[i]['Using'].remove(j)
            EQUIPMENT[i]['total_use'] += len(EQUIPMENT[i]['Using'])
            inside += len(EQUIPMENT[i]['Using'])

            # waiting time
            for j in EQUIPMENT[i]['Waiting']:
                j['wait'] += 1
            EQUIPMENT[i]['total_wait'] += len(EQUIPMENT[i]['Waiting'])
            inside += len(EQUIPMENT[i]['Waiting'])

        in_gym.append(inside)
        time += 1
        # print(f'{time} ', end='')

    # gym closes
    else:
        for i in EQUIPMENT:
            for j in EQUIPMENT[i]['Using']:
                wait_ratio = j['wait'] / (j['wait'] + j['workout_time'] + 1)
                record.append(wait_ratio)
                total_wait += j['wait']
                total_use += j['workout_time']
            for j in EQUIPMENT[i]['Waiting']:
                wait_ratio = j['wait'] / (j['wait'] + j['workout_time'] + 1)
                record.append(wait_ratio)
                total_wait += j['wait']
                total_use += j['workout_time']
        # print('* ', end='')
    # return record, total_wait, total_use, in_gym, EQUIPMENT
    return sum(record) / len(record)


def cal_cost(sol):
    cost = 126_303
    for i in sol:
        cost += sol[i] * PARAMETER_EQUIPMENT[i]['cost']
    if cost <= MAX_COST:
        return 0
    return cost - MAX_COST

def local_search():
    sol = deepcopy(INITIAL_SOL)
    results, tries, best = [], 1, simulation(sol)

    def generate_sol(sol):
        while True:
            n = 1
            r = deepcopy(sol)
            for i in sol:
                if i == 'cable':
                    change = rd.choice([-4, 0, 4])
                    r[i] = max(0, sol[i] + change)
                    continue

                change = rd.choice([-1, 0, 1])
                r[i] = max(0, sol[i] + change)
            if cal_cost(r) == 0 or n > 100:
                if n > 100:
                    print(f'fail:{n}')
                break
        return r

    while tries <= 500:
        new = generate_sol(sol)
        ratio = simulation(new)
        cost = cal_cost(new)
        response = ratio + cost / 1_000

        if response < best:
            best = response
            sol = new
            print(f'observations: {tries} ratio:{ratio:.5f} cost:{cost:,}')
        results.append(best)

        if tries % 10 == 0:
            print(f'observations: {tries} best:{best:.5f} ratio:{ratio:.5f} cost:{cost:,}')

        tries += 1
    return sol, results, cal_cost(sol)

# Main Function
def main():
    # print(f'{simulation(INITIAL_SOL)}')
    # print(cal_cost(INITIAL_SOL))

    solution, results, cost = local_search()
    print(f'solution:{solution} \nratio:{results} \ncost:{cost}')

    xaxis = [i for i in range(500)]
    plt.plot(xaxis, results)
    plt.ylim(0, 0.04)
    plt.xlabel('Observations')
    plt.ylabel('Waiting Time Ratio')
    plt.suptitle('Local Search')
    plt.show()

    return


if __name__ == '__main__':
    main()



