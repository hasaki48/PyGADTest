#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :test.py
'''
!@brief :用pygad模块尝试一下
'''
# *@author:Hasaki48
# *@date  :2022-06-21

from DataExport import ShowData
import Equations
import pygad
import numpy as np
import Initialize


def fitness_func(solution, solution_idx):
    cost = Equations.calCost(solution)
    fitness = 100000.0 / cost
    return fitness


def GASearch():
    Equations.RandomUsingSVD()
    sol_per_pop = 200
    num_genes = Equations.chromosome_length

    init_range_low = -np.linalg.norm(Equations.b)
    init_range_high = np.linalg.norm(Equations.b)

    # mutation_percent_genes =

    ga_instance = pygad.GA(num_generations=10000,
                           num_parents_mating=20,
                           fitness_func=fitness_func,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           mutation_probability=0.1
                           )

    ga_instance.run()
    ga_instance.plot_fitness()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(
        solution=solution))
    print("Cost of the best solution = {solution_fitness}".format(
        solution_fitness=100000.0 / solution_fitness))
    print("Index of the best solution : {solution_idx}".format(
        solution_idx=solution_idx))
    ShowData(solution)


if __name__ == '__main__':
    Initialize.initGA(5, 6, 10000, 20, 0.05)
    GASearch()
