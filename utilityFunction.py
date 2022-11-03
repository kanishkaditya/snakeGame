import random
import numpy as np

Roulette_wheel=list(range(0,int(0.2*50)))*3+list(range(int(0.2*50),int(0.5*50)))*2+list(range(int(0.5*50),50))
def crossover(parents, offspring_size):
    offspring = np.empty(offspring_size)

    for k in range(offspring_size[0]):

        parent1_id = random.choice(Roulette_wheel)
        parent2_id = random.choice(Roulette_wheel)
        while parent2_id == parent1_id: parent2_id = random.choice(Roulette_wheel)
        for j in range(offspring_size[1]):
            if random.uniform(0, 1) < 0.5:
                offspring[k, j] = parents[parent1_id, j]
            else:
                offspring[k, j] = parents[parent2_id, j]
    return offspring


def pairing(num_parents, fitness_score, weights):
    parents = np.empty((num_parents, 268))

    for parent_num in range(num_parents):
        max_fitness_idx = np.array(fitness_score).argmax()
        parents[parent_num, :] = weights[max_fitness_idx, :]
        fitness_score[max_fitness_idx] = -99999

    return parents
    # s1 = np.sum(fitness_score)
    #
    # for i in range(50):
    #     p = 0
    #     s = np.random.randint(0, int(s1))
    #     for index1, j in enumerate(fitness_score):
    #         p += j
    #         if p > s:
    #             fitness_score[index1]=-99
    #             parents[i, :] = weights[index1, :]
    #             s1-=99
    #             break
    # return parents


    # mutation()


def fitness_func(score, steps):
    fitness = (score+0.5+0.5*(score-steps/(score+1))/(score+steps/(score+1)))*1000000
    return fitness


# def crossover(index1, index2):
#     mask = np.random.randint(0, 2, size=268)
#     inv_mask = 1 - mask
#     elite = np.array(fitness_score).argsort()
#     # if (index1 in elite[490:10] and index2 in elite[490:10]) or (index1 not in elite[490:10] and index2 not in elite[490:10]):
#     weights[index1] = weights[index1] * mask + inv_mask * weights[index2]
#     weights[index2] = weights[index1] * inv_mask + mask * weights[index2]
#     # elif index1 in elite[490:10]:
#     #weights[index2] = weights[index1] * inv_mask + mask * weights[index2]
#     # else:
#     #weights[index1] = weights[index1] * mask + inv_mask * weights[index2]


# def mutation(weights):
#     for i in range(2000):
#         if random.random() < 0.4:
#             for _ in range(int(268 * 0.05)):
#                 plc = random.randint(0, 267)
#                 value = random.choice(np.arange(-0.5, 0.5, step=0.001))
#                 weights[i][plc] = weights[i][plc] + value

def mutation(offspring_crossover):
    for idx in range(offspring_crossover.shape[0]):
        for _ in range(13):
            i = random.randint(0, offspring_crossover.shape[1] - 1)
            random_value = np.random.choice(np.arange(-1, 1, step=0.001))
            offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value

    return offspring_crossover
