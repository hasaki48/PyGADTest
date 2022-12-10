#!/usr/bin/env python3
# ?-*- coding:utf-8 -*-
# *@file  :CalcualateDis.py
'''
!@brief :Python连接SQL Server数据库通过T-SQL计算距离得到成本
'''
# *@author:Hasaki48
# *@date  :2022-12-01


import pyodbc
import GetMudData
from pyodbc import *
import CommonSQL
import Distance


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


def Calculate(Connection: Connection):
    cursor = Connection.cursor()
    cursor.execute(CommonSQL.CheckExists.format(TableName="Distance"))
    Connection.commit()
    cursor.execute(Distance.SelInto)
    Connection.commit()


if __name__ == '__main__':
    connection = ServerConnection()
    Calculate(connection)
