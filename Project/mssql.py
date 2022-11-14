#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :mssql.py
'''
!@brief :python连接SQL Server数据库
'''
# *@author:Hasaki48
# *@date  :2022-11-09

import PeriodConfig
import pyodbc
import datetime


TimeConfig = {"BeginChar": '\'2021-06-01\'', "EndChar": '\'2021-08-01\'',
              "Begin": '2021-06-01', "End": '2021-08-01'}


def ServerConnection():
    Driver = "SQL Server"
    Server = "localhost"
    Database = "Transport"
    UID = "sa"
    PWD = "@whu6408"
    ConnectionStr = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format(
        Driver, Server, Database, UID, PWD)

    Connection = pyodbc.connect(ConnectionStr)
    return Connection

# row = cursor.fetchone()


def program():
    Connection = ServerConnection()
    cursor = Connection.cursor()
    cursor.execute(PeriodConfig.CheckExists)  # 检查WeekPlan表是否存在，存在即删除
    Connection.commit()
    cursor.execute(PeriodConfig.SelInto.format(
        **TimeConfig))  # Select into WeekPlan表
    Connection.commit()

    BeginDate = datetime.datetime.strptime(TimeConfig["Begin"], '%Y-%m-%d')
    EndDate = datetime.datetime.strptime(TimeConfig["End"], '%Y-%m-%d')
    StartWeek = BeginDate.isocalendar()[1]
    StartWeekDay = BeginDate.isocalendar()[2]
    EndWeek = EndDate.isocalendar()[1]
    EndWeekDay = EndDate.isocalendar()[2]

    LoopSum = EndWeek - StartWeek  # 有多少周就循环多少次
    LoopCount = 0
    while LoopCount <= LoopSum:
        if(LoopCount == 0):  # 如果是第一周
            StartDateOfWeek = BeginDate.strftime(
                "\'%Y-%m-%d\'")  # 这周的开始时间取区间开始日期
            EndDateOfWeek = (BeginDate +
                             datetime.timedelta(
                                 7-StartWeekDay)).strftime("\'%Y-%m-%d\'")  # 这周的结束时间取周末
            LoopCount += 1  # 计数器加一

            rows = cursor.execute(PeriodConfig.SQL.format(
                StartDateOfWeek=StartDateOfWeek, EndDateOfWeek=EndDateOfWeek)).fetchall()
            print(rows)
            continue
        if(LoopCount == LoopSum):  # 如果是最后一周
            StartDateOfWeek = (BeginDate +
                               datetime.timedelta(
                                   LoopCount*7 - StartWeekDay - 1)).strftime("\'%Y-%m-%d\'")  # 这周的开始时间正常的取周一
            EndDateOfWeek = EndDate.strftime("\'%Y-%m-%d\'")  # 这周的结束时间取区间最后日期
            LoopCount += 1
            rows = cursor.execute(PeriodConfig.SQL.format(
                StartDateOfWeek=StartDateOfWeek, EndDateOfWeek=EndDateOfWeek)).fetchall()
            print(rows)
            continue
        # 其余无特殊情况
        StartDateOfWeek = (BeginDate +
                           datetime.timedelta(LoopCount*7-StartWeekDay -
                                              1)).strftime("\'%Y-%m-%d\'")  # 通过一点小小的计算，取周一
        EndDateOfWeek = (BeginDate +
                         datetime.timedelta((LoopCount+1)*7 -
                                            StartWeekDay)).strftime("\'%Y-%m-%d\'")  # 取周末
        LoopCount += 1
        rows = cursor.execute(PeriodConfig.SQL.format(
            StartDateOfWeek=StartDateOfWeek, EndDateOfWeek=EndDateOfWeek)).fetchall()
        print(rows)


if __name__ == '__main__':
    program()
