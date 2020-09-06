#!/usr/bin/env python
# -*-encoding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:         t1.py
# Description:  
# Author:       Aaron
# Date:         2020/9/6 19:06
# -------------------------------------------------------------------------------
import sys
import traceback
import os

RESPONSE = {
    "code": 1000,
    "data": [],
    "message": "",
}

def m1():
    # 当前文件名
    print(__file__)

    # 模块名
    print(sys._getframe().f_code.co_name)

    # 行号
    print(sys._getframe().f_lineno)


def m2():
    try:
        RESPONSE["data"] = 2
        raise NameError
    except Exception as e:
        m1()
        print(e)


m2()
print(RESPONSE)