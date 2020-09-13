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


def wrapper1(fn):
    def inner(*args, **kwargs):
        print("wrapper1-start")
        ret = fn(*args, **kwargs)
        print("wrapper1-end")
        return ret

    return inner


def wrapper2(fn):
    def inner(*args, **kwargs):
        print("wrapper2-start")
        ret = fn(*args, **kwargs)
        print("wrapper2-end")
        return ret

    return inner


def wrapper3(fn):
    def inner(*args, **kwargs):
        print("wrapper3 - start")
        ret = fn(*args, **kwargs)
        print("wrapper3 - end")
        return ret

    return inner


# 就近原则
@wrapper1
@wrapper2
@wrapper3
def func():
    print("我是可怜的func")


if __name__ == "__main__":
    # m2()
    # print(RESPONSE)

    func()