#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :Equations.py
'''
!@brief :有关解线性方程的公用模块
'''
# *@author:Hasaki48
# *@date  :2022-05-28
import numpy as np
import Initialize

# 当前层的系数矩阵
A = 0

# 当前层求解向量
b = 0

# 当前层线性方程的特解与通解
special_solution = 0
common_solutions = 0

# 染色体的长度
chromosome_length = 0

"""
核心算法：
1.利用SVD分解得齐次方程组的通解
2.lstsq()函数得最小二乘特解
3.通解*染色体 + 最小二乘特解 => 满足Ax=b的一个解
@param eps 最小容差
@return common_solutions.shape[0] 通解含有的向量个数
"""


def RandomUsingSVD(eps=1e-15):
    global A, b, special_solution, common_solutions, chromosome_length
    # * 初始化系数矩阵
    A = np.zeros((Initialize.ConsumpNum + Initialize.MudNum,
                  Initialize.ConsumpNum * (Initialize.MudNum + 1)))
    InitializeMatrix(A)

    # * 初始化结果向量
    MudArray = np.asarray(Initialize.Mud)
    ConsumpCapArray = np.asarray(Initialize.ConsumpCap)
    b = np.append(MudArray, ConsumpCapArray)

    # * 最小二乘特解
    special_solution = np.linalg.lstsq(
        A, b, rcond=-1)[0]
    # print(special_solution)

    # * SVD分解得到通解
    u, s, vt = np.linalg.svd(A)
    condition_array = []
    for i in range(vt.shape[0]):
        if i < s.shape[0]:
            if s[i] <= eps:
                condition_array.append(1)
            else:
                condition_array.append(0)
        else:
            condition_array.append(1)
    # print(condition_array)
    common_solutions = np.compress(condition_array, vt, axis=0)
    return common_solutions.shape[0]


"""
初始化系数矩阵
@param Matrix 系数矩阵
即系数矩阵要使
1.分配矩阵中的各行加起来 = 渣场的产渣量
2.分配矩阵中的各列加起来 <= 受纳场的承受能力
"""


def InitializeMatrix(Matrix):
    # * 需要分两种情况

    # *1.渣场有关的前几个需要填的系数紧贴在一起
    for i in range(Initialize.MudNum):
        Jump(Matrix[i], Initialize.ConsumpNum*i, Initialize.ConsumpNum, 1)

    # * 2.受纳场有关的系数在矩阵中分开了一段距离
    for i in range(Initialize.ConsumpNum):
        Jump(Matrix[Initialize.MudNum + i], i,
             Initialize.MudNum+1, Initialize.ConsumpNum)


"""
系数矩阵行向量初始化技巧函数
@param Row 系数矩阵的第几行
@param Start 从第{Row}行的第几个开始
@param Num 初始化多少个
@param Step 系数彼此的间隔为多少
"""


def Jump(Row, Start, Num, Step=1):
    for i in range(Num):
        Row[Start + i * Step] = 1
