#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :AFSATest.py
'''
!@brief :人工鱼群算法(artificial fist swarm algorithm,AFSA)
'''
# *@author:Hasaki48
# *@date  :2022-06-23


import Equations
from sko.AFSA import AFSA
import numpy as np
import Initialize
import matplotlib.pyplot as plt
import pandas as pd
import DataExport


def func(x):
    cost = Equations.calCost(x)
    return cost


def AFSASearch():
    Equations.RandomUsingSVD()
    b_norm = np.linalg.norm(Equations.b)
    afsa = AFSA(func=func, n_dim=Equations.chromosome_length,
                size_pop=200, max_iter=1000, max_try_num=100,
                step=0.5, visual=0.3, q=0.98, delta=0.5)
    best_x, best_y = afsa.run()
    print(best_x, best_y)
    DataExport.ShowData(best_x)
    plt.show()


if __name__ == '__main__':
    Initialize.initGA(5, 6, 10000, 20, 0.05)
    AFSASearch()
