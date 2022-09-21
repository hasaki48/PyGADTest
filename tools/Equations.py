#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :Equations.py
'''
!@brief :有关解线性方程的公用模块
'''
# *@author:Hasaki48
# *@date  :2022-05-28
import copy
from doctest import testsource
import numpy as np
import Initialize
from common import normalize
from sympy import Matrix

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
    common_solutions = normalize(common_solutions)
    chromosome_length = common_solutions.shape[0]


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


"""
根据成本矩阵和线性方程组的解计算当代染色体的运输成本
@param chromosome 染色体
@return EconomicCost 一个染色体花费的成本
"""


def calCost(chromosome):
    global common_solutions
    chromosome = np.array(chromosome)
    # ? 通解*不同的系数 + 特解 = 方程组的一个解
    solution = np.zeros(common_solutions[0].shape[0])
    now_cn_solution = copy.deepcopy(common_solutions)
    for i in range(chromosome_length):
        now_cn_solution[i] = now_cn_solution[i] * chromosome[i]
        solution += now_cn_solution[i]
    solution += special_solution

    # * 转换一下成本矩阵的格式以便后续计算
    EconomicVector = np.asarray(Initialize.EconomicCostMatrix).reshape(
        Initialize.ConsumpNum * (Initialize.MudNum + 1),) * solution

    # * 这里的成本计算需要使用绝对值，不然会出现极大负值的情况
    EconomicCost = 0
    for _ in range(len(EconomicVector)):
        EconomicCost += abs(EconomicVector[_])
    return EconomicCost


"""
核心算法：
1.利用最朴素的移项得齐次方程组的通解
2.lstsq()函数得最小二乘特解
3.通解*染色体 + 最小二乘特解 => 满足Ax=b的一个解
@param eps 最小容差
"""


def RandomUsingSimple(eps=1e-15):
    global A, b, special_solution, common_solutions, chromosome_length
    # * 初始化系数矩阵
    # m*n 的矩阵
    # m 为行数，n 为列数
    m = Initialize.ConsumpNum + Initialize.MudNum
    n = Initialize.ConsumpNum * (Initialize.MudNum + 1)
    A = np.zeros((m, n))
    InitializeMatrix(A)
    A_rank = np.linalg.matrix_rank(A)

    # 测试一下
    A_1, one_index_tuple = Matrix(A).rref()
    A1 = np.array(A_1.tolist()).astype(np.int32)
    # print(Matrix(A).rref())
    # print(one_index_tuple)
    unextend_index_len = len(one_index_tuple)
    one_index_list = list(one_index_tuple)
    one_index_list.append(n)

    free_vector_index_list = []
    for i in range(unextend_index_len):
        now_index = one_index_list[i]
        next_index = one_index_list[i+1]
        if (next_index - now_index) == 1:
            continue
        elif (next_index - now_index) > 1:
            free_vector_count = next_index - now_index
            for j in range(1, free_vector_count):
                free_vector_index = now_index + j
                free_vector_index_list.append(free_vector_index)
    # print(free_vector_index_list)

    # print(A1[:, one_index_tuple])
    free_var_number = n - A_rank

    Homogeneous_A = A1[:, one_index_tuple]
    common_solutions = np.zeros(shape=(free_var_number, n))

    for i in range(free_var_number):
        Homogeneous_b = np.zeros(shape=(A_rank, 1))
        for j in range(A_rank):
            Homogeneous_b[j] = -A1[j][free_vector_index_list[i]]
        one_index = np.linalg.solve(
            Homogeneous_A, Homogeneous_b).reshape(1, A_rank).tolist()[0]
        common_solutions[i][free_vector_index_list[i]] = 1
        for k in range(len(one_index)):
            common_solutions[i][one_index_tuple[k]] = one_index[k]

    chromosome_length = common_solutions.shape[0]

    # * 初始化结果向量
    MudArray = np.asarray(Initialize.Mud)
    ConsumpCapArray = np.asarray(Initialize.ConsumpCap)
    b = np.append(MudArray, ConsumpCapArray)

    # * 最小二乘特解
    special_solution = np.linalg.lstsq(
        A, b, rcond=-1)[0]
    # print(special_solution)


def rsmat(arbmat):
    """ Convert an arbitrary matrix to a simplest matrix """
    arbmat = arbmat.astype(float)
    row_number, column_number = arbmat.shape
    if row_number == 1:
        if arbmat[0, 0] != 0:
            return (arbmat/arbmat[0, 0])
        else:
            return arbmat
    else:
        rc_number = min(row_number, column_number)
        anarbmat = arbmat.copy()
        r = 0
        for n in range(rc_number):
            s_row = -1
            for i in arbmat[r:row_number, n]:
                s_row += 1
                if abs(i) > 1e-10:
                    anarbmat[r, :] = arbmat[s_row+r, :]
                    for j in range(r, row_number):
                        if j < s_row+r:
                            anarbmat[j+1, :] = arbmat[j, :]
                    arbmat = anarbmat.copy()
            if abs(anarbmat[r, n]) > 1e-10:
                anarbmat[r, :] = anarbmat[r, :] / anarbmat[r, n]
                for i in range(row_number):
                    if i != r:
                        anarbmat[i, :] -= \
                            anarbmat[i, n]*anarbmat[r, :]
            arbmat = anarbmat.copy()
            if abs(arbmat[r, n]) < 1e-10:
                r = r
            else:
                r = r + 1
        for m in range(column_number):
            if abs(arbmat[-1, m]) > 1e-10:
                arbmat[-1, :] = arbmat[-1, :]/arbmat[-1, m]
                for i in range(row_number-1):
                    arbmat[i, :] -= \
                        arbmat[i, m]*arbmat[-1, :]
                break
        return arbmat


if __name__ == '__main__':
    Initialize.initGA(5, 6, 10000, 20, 0.05)
    RandomUsingSimple()
