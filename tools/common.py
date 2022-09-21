#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *file  :common.py
'''
!@brief :算法中各个模块都需要用到的共有模块
'''
# *author:Hasaki48
# *date  :2022-02-17

import random
from typing import List

import numpy as np

"""
向量归一化
@param vector 需要归一化的向量
@return normalized_vector 归一化后的向量
"""


def normalize(vector):
    normalized_vector = vector / np.linalg.norm(vector)
    return normalized_vector


"""
创建随机数组
@param length 数组长度
@param range 数组取值范围
"""


def initRandomArray(length: int, ranges: List[int]) -> List[int]:
    randomArray = []
    for i in range(length):
        randomArray.append(random.randint(ranges[0], ranges[1]))
    return randomArray


"""
创建随机矩阵
@param m 矩阵行数
@param n 矩阵列数
@param range 取值范围
"""


def initRandomMatrix(m: int, n: int, ranges: List[int]) -> List[List[int]]:
    randomMatrix = []
    for i in range(m):
        randomMatrix.append(initRandomArray(n, ranges))
    return randomMatrix


"""
根据数组创建其数值大小序列的新数组
*例如：数组[70,50,90,60,40]经过处理后应该得到[4,1,3,0,2](从小到大的顺序，顺序)或者[2,0,3,1,4](从大到小的顺序，逆序)
@param array 需要得到大小序列的数组
@param type 顺序还是逆序
@return {array} 大小序列数组
"""


def getOrderArray(array: List[float], type):
    arraycopy = array[:]
    orderArray = []
    for i in range(len(arraycopy)):
        minindex = array.index(min(arraycopy))
        orderArray.append(minindex)
        arraycopy[minindex] = float('inf')
    if type == "Reverse":
        orderArray.reverse()
    return orderArray


"""
Sigmoid函数
@param number 自变量x
@return number 因变量y
"""


def Sigmoid(x):
    return 1.0/(1 + np.exp(-x))


"""
从数组中寻找最大的n个元素
@param array
@param n
"""


def maxN(array, n):
    # * 将一切数组升级成二维数组，二维数组的每一行都有两个元素构成[原一维数组的下标，值]
    matrix = []
    for index in range(len(array)):
        matrix.append([index, array[index]])

    # * 对二维数组排序（因为只需要寻找最大的n个，故这里采用冒泡排序）
    for i in range(int(n)):
        for j in range(1, len(matrix)):
            if matrix[j-1][1] > matrix[j][1]:
                temp = matrix[j-1]
                matrix[j-1] = matrix[j]
                matrix[j] = temp

    # * 取最大的n个元素
    maxIndexArray = []
    for i in range(len(matrix) - 1, len(matrix) - int(n) - 1, -1):
        maxIndexArray.append(matrix[i][0])

    return maxIndexArray


if __name__ == '__main__':
    print(getOrderArray([70, 50, 90, 60, 40], "Reverse"))
