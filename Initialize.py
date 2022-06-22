#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :Initialize.py
'''
!@brief :数据初始化模块
'''
# *@author:Hasaki48
# *@date  :2022-05-28


from math import isnan, nan
from random import Random

import numpy as np

from common import initRandomArray, initRandomMatrix

# 渣土集合(Mud[i]表示第i个渣场产生的渣土量)
Mud = [50, 60, 30, 40, 70]  # 设定为特殊值[50,60,30,40,70]
# 渣场数量
MudNum = 5

# 中转场、受纳场处理能力集合(ConsumpCap[i]表示第i个中转场或处理场的消纳能力)
ConsumpCap = []
# 中转场、受纳场数量
ConsumpNum = 5
# 中转场、受纳场时间成本矩阵
# (TimeCost[i,j]表示将单位量i渣场产生的渣土运输至j处理场并处理的时间成本)
TimeCostMatrix = []
# 中转场、受纳场经济成本矩阵
# (EconomicCost[i,j]表示将单位量i渣场产生的渣土运输至j处理场并处理的经济成本)
EconomicCostMatrix = []

# 渣土量取值范围
MudRange = [30, 100]

# 受纳场处理能力取值范围
ConsumpCapRange = [200, 400]
# 受纳场处理能力最大值
ConsumpCapMax = max(ConsumpCapRange)
# 受纳场处理能力平均值
ConsumpCapAvg = sum(ConsumpCapRange)/len(ConsumpCapRange)

# 受纳场时间成本取值范围
TimeRange = [10, 20]
# 受纳场经济成本取值范围
EconomicRange = [300, 800]
# 受纳场经济成本最大值
EconomicMax = max(EconomicRange)
# 受纳场经济成本平均值
EconomicAvg = sum(EconomicRange)/len(EconomicRange)


# 目标函数平均值
Fit_avg = EconomicAvg * ConsumpCapAvg
# 目标函数最大值
Fit_max = EconomicMax * ConsumpCapMax
# 适应度函数中的常数C
C = 1.5
# 适应度函数系数阿尔法
Alpha = (C - 1) * Fit_avg / (Fit_max - Fit_avg)
# 适应度函数系数贝塔
Beta = (Fit_max - C * Fit_avg) * Fit_avg / (Fit_max - Fit_avg)


# 染色体初始随机数选择范围最大值
RandomMax = 100

# 迭代次数
iteratorNum = 10000

# 染色体数量
chromosomeNum = 10

# 适应度矩阵(下标：染色体编号、值：该染色体的适应度)
adaptability = []
# 自然选择的概率矩阵(下标：染色体编号、值：该染色体被选择的概率)
selectionProbability = []

# 染色体复制的比例(每代中保留适应度较高的染色体直接成为下一代)
copyproportion = 0.2
# 参与交叉变异的染色体数量
crossoverMutationNum = 0

# 调配规划结果集([迭代次数][染色体编号])
resultData = []

"""
初始化遗传算法
@param _MudNum 渣场数量
@param _ConsumpNum 受纳场数量
@param _iteratorNum 迭代次数
@param _chromosomeNum 染色体数量
@param _copyproportion 染色体复制的比例
"""


def initGA(_MudNum, _ConsumpNum, _iteratorNum, _chromosomeNum, _copyproportion):
    # * 参数检验
    if checkParam(_MudNum, _ConsumpNum, _iteratorNum, _chromosomeNum, _copyproportion) == False:
        return

    # * 初始化渣场集合
    global Mud, MudNum
    MudList = initRandomArray(MudNum, MudRange)
    # Mud = [x / 100 for x in MudList]  # 归一化处理
    Mud = MudList

    # * 初始化中转场、受纳场集合
    global ConsumpCap, ConsumpNum
    ConsumpCapList = initRandomArray(ConsumpNum, ConsumpCapRange)
    # ConsumpCap = [x / 100 for x in ConsumpCapList]  # 归一化处理
    ConsumpCap = ConsumpCapList

    # * 时间、经济成本矩阵初始化
    global TimeCostMatrix, EconomicCostMatrix
    TimeCostMatrix = initRandomMatrix(MudNum, ConsumpNum, TimeRange)
    TimeCostMatrix.append([0 for _ in range(ConsumpNum)])
    EconomicCostMatrix = initRandomMatrix(MudNum, ConsumpNum, EconomicRange)
    EconomicCostMatrix.append([0 for _ in range(ConsumpNum)])


"""
参数校验
@param _MudNum 渣场数量
@param _ConsumpNum 受纳场数量
@param _iteratorNum 迭代次数
@param _chromosomeNum 染色体数量
@param _copyproportion 染色体复制的比例
"""


def checkParam(_MudNum, _ConsumpNum, _iteratorNum, _chromosomeNum, _copyproportion):
    def checkIsNaN(parameter):
        if isnan(parameter[0]):
            print("{}必须是数字!".format(parameter[1]))
            return False
        return True
    parameters = [(_MudNum, "渣场数量"), (_ConsumpNum, "受纳场数量"),
                  (_iteratorNum, "迭代次数"), (_chromosomeNum, "染色体数量")]
    result = all(map(checkIsNaN, parameters))
    if result == False:
        return False
    if isnan(_copyproportion or _copyproportion < 0 or _copyproportion > 1):
        print("染色体复制的比例必须为数字！并且在0~1之间！")
        return False

    global MudNum, ConsumpNum, iteratorNum, chromosomeNum, copyproportion, crossoverMutationNum
    MudNum = _MudNum
    ConsumpNum = _ConsumpNum
    iteratorNum = _iteratorNum
    chromosomeNum = _chromosomeNum
    copyproportion = _copyproportion
    crossoverMutationNum = int(chromosomeNum - chromosomeNum * _copyproportion)
    return True


if __name__ == '__main__':
    initGA(5, 5, 100, 20, 0.5)
