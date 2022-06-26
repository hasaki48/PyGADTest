#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :PSOTest.py
'''
!@brief :粒子群算法(Particle swarm optimization)
'''
# *@author:Hasaki48
# *@date  :2022-06-23


import numpy as np
import Equations
from sko.PSO import PSO
import matplotlib.pyplot as plt
import DataExport
import Initialize


def fitness_func(x):
    cost = Equations.calCost(x)
    fitness = cost
    return fitness


def PAOSearch():
    Equations.RandomUsingSimple()
    b_norm = np.linalg.norm(Equations.b)
    lb = [-b_norm] * Equations.chromosome_length
    ub = [b_norm] * Equations.chromosome_length
    pso = PSO(func=fitness_func, n_dim=Equations.chromosome_length,
              lb=lb, ub=ub, pop=200, max_iter=1000)
    pso.run()
    print("best_x is ", pso.gbest_x, 'best_y is', pso.gbest_y)
    plt.plot(pso.gbest_y_hist)
    plt.show()
    DataExport.ShowData(pso.gbest_x)
    plt.show()


if __name__ == '__main__':
    Initialize.initGA(5, 6, 10000, 20, 0.05)
    PAOSearch()
