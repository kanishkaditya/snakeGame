from Snake_Game import main
import numpy as np
import os
import random
import matplotlib.pyplot as  plt

import utilityFunction

no_of_agents = 50
generation = 150
mutation_rate = 0.4
fitness_score = []
high_scores = []
avg_fitness = []
num_parents = 50
offspring_size = 450
parents = []
gens = []
file_name = 'weights.npz'

if file_name not in os.listdir(os.getcwd()):
    weights = np.random.uniform(size=(500, 268))
    i = 0
else:
    ip = np.load(file_name)
    weights = ip['population']
    high_scores = ip['score'].tolist()
    gens = [i for i in ip['generation']]
    avg_fitness=ip['avg'].tolist()
    i = gens[-1] + 1

while True:

    print('generation', i)
    for j in range(500):
        apple, step = main.run_game(weights[j])
        fitness_score.append(utilityFunction.fitness_func(apple, step))
        print(
            "Chromosome " + str(j) + ":- " + "score :- " + str(apple) + " steps :- " + str(step) + " fitness :- " + str(
                fitness_score[-1]))
    high_scores.append(np.array(fitness_score).max())
    avg_fitness.append(np.mean(fitness_score))
    parents = utilityFunction.pairing(num_parents, fitness_score, weights)
    offspring = utilityFunction.crossover(parents, (450, 268))
    offspring_mutation = utilityFunction.mutation(offspring)

    weights[0:parents.shape[0], :] = parents
    weights[parents.shape[0]:, :] = offspring_mutation

    gens.append(i)

    plt.ion()
    plt.plot(gens, high_scores,label='highest',color='red')
    plt.plot(gens, avg_fitness, label='highest', color='orange')
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.show(block=False)
    plt.pause(2)
    plt.close('all')
    np.savez(file_name, population=weights, score=high_scores, generation=gens,avg=avg_fitness)
    i += 1

    fitness_score = []
