#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :DataExport.py
'''
!@brief :
'''
# *@author:Hasaki48
# *@date  :2022-06-21

import numpy as np
import Equations
import copy
import Initialize
import pandas as pd

"""
数据展示
@param chromosome 各个系数K组成的单条染色体
"""


def ShowData(chromosome):
    # 满足线性方程组的解
    solution = np.zeros(Equations.common_solutions[0].shape[0])
    # 通解 => 全局变量
    now_cn_solution = copy.deepcopy(Equations.common_solutions)
    # * 解的形式类似 x = solution[0]*k0 + solution[1]*k1
    for j in range(Equations.common_solutions.shape[0]):
        now_cn_solution[j] = now_cn_solution[j] * chromosome[j]
        solution += now_cn_solution[j]
    solution += Equations.special_solution
    # 将解转换成矩阵形式以便显示
    solution = solution.reshape((Initialize.MudNum + 1, Initialize.ConsumpNum))
    # numpy设置数字的显示格式
    np.set_printoptions(formatter={'float': '{:.2f}'.format})
    ArrayToExcel(solution)
    print(solution)


"""
将数据写入Excel文件
@param data numpy数组
"""


def ArrayToExcel(data):
    row_names = ['渣场1', '渣场2', '渣场3', '渣场4', '渣场5', '受纳场结余']
    column_names = ['受纳场1', '受纳场2', '受纳场3', '受纳场4', '受纳场5', '受纳场6']
    deploy_matrix = pd.DataFrame(data, index=row_names, columns=column_names)
    deploy_matrix.loc['受纳场承受能力'] = Initialize.ConsumpCap
    deploy_matrix['渣场产渣量'] = Initialize.Mud + [''] * 2

    cost_matrix = pd.DataFrame(
        Initialize.EconomicCostMatrix, index=row_names, columns=column_names)

    writer = pd.ExcelWriter("调配结果.xlsx")
    deploy_matrix.to_excel(excel_writer=writer, sheet_name='调配矩阵',
                           float_format='%.5f')
    cost_matrix.to_excel(excel_writer=writer, sheet_name='成本矩阵',
                         float_format='%.5f')

    writer.save()
