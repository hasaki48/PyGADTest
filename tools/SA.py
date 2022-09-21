#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :SATest.py
'''
!@brief :模拟退火算法(SA,Simulated Annealing)
'''
# *@author:Hasaki48
# *@date  :2022-06-23


import Equations
from sko.SA import SA
import numpy as np
import Initialize
import matplotlib.pyplot as plt
import pandas as pd
import DataExport


def fitness_func(x):
    cost = Equations.calCost(x)
    fitness = cost
    return fitness


def SASearch():
    Equations.RandomUsingSimple()
    b_norm = np.linalg.norm(Equations.b)

    initial_x = np.random.randint(-b_norm, b_norm,
                                  size=(Equations.chromosome_length,))
    sa = SA(func=fitness_func, x0=initial_x, T_max=300,
            T_min=1e-9, L=2000, max_stay_counter=300)
    best_x, best_y = sa.run()
    print('best_x', best_x, "min_cost", best_y)
    plt.plot(pd.DataFrame(sa.best_y_history).cummin(axis=0))
    DataExport.ShowData(best_x)
    plt.show()


if __name__ == '__main__':
    Initialize.initGA(5, 6, 10000, 20, 0.05)
    SASearch()
