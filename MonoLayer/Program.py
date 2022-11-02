#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :Program.py
'''
!@brief :单层遗传网络处理流程
'''
# *@author:Hasaki48
# *@date  :2022-09-21


import os
import sys
"""
python import模块
"""

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from tools.GA import GASearch  # NOQA:E402
import InputPara  # NOQA:E402
import tools.Parameters  # NOQA:E402
import tools.Initialize  # NOQA:E402


tools.Parameters.MudList = InputPara.MudList
tools.Parameters.ConsumpCapList = InputPara.ConsumpCapList
tools.Parameters.EconomicCostMatrix = InputPara.EconomicCostMatrix
tools.Initialize.initGA(5, 6, 10000, 20, 0.05)
GASearch()
