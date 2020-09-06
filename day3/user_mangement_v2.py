#!/usr/bin/env python
# -*-encoding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:         user_mangement_v2.py
# Description:  用户管理系用-v2
# Author:       Aaron
# Date:         2020/8/24 19:35
# -------------------------------------------------------------------------------

# 练习需求如下
# 1. 需要登陆认证, 认证三次失败退出程序
# 2. 有增删改查和搜索功能
#     2.1 增 add   # add Aaron 12 17575481302 aaron@qq.com
#     2.2 删 delete    # delete Aaron
#     2.3 改 update    # update Aaron set age = 18, [ other_field_name = new_value ]
#     2.4 查 list  # list
#     2.5 搜 find  # find monkey
#
# 3. 格式化输出(Ptable)
# 4. 数据展示具有分页功能
# 5. 数据更新时自动持久化(json)
# 6. 异常处理
# 7. 优雅的格式输出
# 8. 提供导出csv功能(csv)
# 提示: 数据结构可用字典


import re
import os
import sys
import csv
import json
import time
from prettytable import PrettyTable


# 核心全局变量
RESULT = {}
FIELD_NAME_L = ["name", "age", "phone", "email"]
# USER_PROFILE = ('Aaron', '111111')
RESPONSE = {
    "code": 1000,
    "data": {},
    "message": "",
}
USER_PROFILE_PATH = "./user.db"
USER_DETAIL_FILE_PATH = "./user_info.json"


# 其它全局变量
TIME_FORMAT = '%Y-%m-%d  %X'


# 计算运行时间的装饰器
def time_cal(func):
    def core(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        time_consumption = time.time() - start_time
        print("\033[33m耗时: %s sec" % time_consumption)
        return res

    return core


# 用户验证
def user_verification(func):
    def core(*args, **kwargs):
        n = 0
        while n < 3:
            print("默认用户: aaron\t密码: 111")
            user_name = input("\033[36mEnter your account name, please:>>\t\033[0m").strip()
            password = input("\033[36mEnter your password, please:>>\t\033[0m").strip()
            if os.path.isfile(USER_PROFILE_PATH):
                with open(USER_PROFILE_PATH) as fd:
                    for line in fd:
                        name, pwd = line.strip().split(":")
                        if user_name == name and password == pwd:
                            print("\033[36mWelcome [%s] logining UM\n\033[0m" % name)
                            return func(*args, **kwargs)
            else:
                print("\033[33mCreate file '{}' first, \n"
                      "then use 'username:password' format to create new user.\t\033[0m".format(USER_PROFILE_PATH))
            n += 1

        print("\033[31mAccount name or password error, more than three failure, exit.\033[0m")
        return False

    return core


# 帮助信息
def help_info():
    print("""
    \tadd: add new_user_name age phone email
    \tdelete: delete old_user_name
    \tupdate: update old_user_name set field_name = new_value
    \tlist: list (it will list all of users.)
    \tfind: find old_user_name
    \tq: process exit
    """)


# 列出所有用户信息
def user_list(*args, **kwargs):
    if not RESULT:
        RESPONSE["code"] = 1004
        RESPONSE["message"] = "\033[33mno any user info, need to add first.\033[0m"
        RESPONSE["data"] = {}
        return user_show()

    RESPONSE["code"] = 1000
    RESPONSE["data"] = RESULT
    return user_show()


# 列出单个用户信息
def user_find(key):
    if key not in RESULT:
        RESPONSE["code"] = 1004
        RESPONSE["message"] = "\033[33m{} is not existed, add first.\033[0m".format(key)
        RESPONSE["data"] = {}
        return user_show()

    user_detail_d = {key: RESULT.get(key)}
    RESPONSE["code"] = 1000
    RESPONSE["data"] = user_detail_d
    user_show()


# 添加新用户
def user_add(data):
    data_length = len(data)
    if data_length < 4:
        RESPONSE["code"] = 1001
        RESPONSE["message"] = "\033[33mdata from user is not enough, try again, please.\033[0m"
        RESPONSE["data"] = {}
        return user_show()

    username = data[0]
    if username in RESULT:
        RESPONSE["code"] = 1003
        RESPONSE["message"] = "\033[33mUser [{}] has already existed\033[0m".format(username)
        RESPONSE["data"] = {}
        return user_show()

    RESULT[username] = {}
    RESULT[username]["age"] = data[1]
    RESULT[username]["phone"] = data[2]
    RESULT[username]["email"] = data[3]
    save_data()
    user_list()


# 更新用户信息
def user_update(data):
    """

    :param data: {name: "username", new_value: {"field_name": "value", ...}}
    :return:
    """
    key = data.get("name")
    field_value_d = data.get("new_value")
    if key not in RESULT:
        RESPONSE["code"] = 1004
        RESPONSE["message"] = "\033[33m{} is not existed, cannot update, add first.\033[0m".format(key)
        RESPONSE["data"] = {}
        return user_show()

    if not field_value_d:
        RESPONSE["code"] = 1001
        RESPONSE["message"] = "\033[33m{} update failure, try again please.\033[0m".format(key)
        RESPONSE["data"] = {}
        return user_show()

    for field, value in field_value_d.items():
        print(field)
        if field == "name" and value not in RESULT:
            user_detail_d = RESULT[key]
            RESULT.pop(key)
            RESULT[value] = user_detail_d
            key = value
            continue

        if field in FIELD_NAME_L:
            RESULT[key][field] = value

    user_detail_d = {key: RESULT.get(key)}
    save_data()
    RESPONSE["code"] = 1000
    RESPONSE["data"] = user_detail_d
    user_show()


# 删除用户信息
def user_delete(key):
    if key not in RESULT:
        RESPONSE["code"] = 1004
        RESPONSE["message"] = "\033[33m{} is not existed, cannot delete.\033[0m".format(key)
        RESPONSE["data"] = {}
        return user_show()

    RESULT.pop(key)
    save_data()
    RESPONSE["code"] = 1000
    RESPONSE["data"] = {}
    user_show()


# 导出用户数据(未完成)
def data_export():
    pass


# 持久化数据到磁盘
def save_data():
    try:
        with open(USER_DETAIL_FILE_PATH, "w") as fd:
            json.dump(RESULT, fd)
    except Exception as e:
        print("\033[31m{} - Error: Data persistence failure. - {} - {} - {}\n\033[0m".format(
            time.strftime(TIME_FORMAT), __file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno))
        print(e)
        return False
    return True


# 加载用户数据到内存
def load_data():
    if os.path.isfile(USER_DETAIL_FILE_PATH):
        with open(USER_DETAIL_FILE_PATH) as fd:
            user_data_d = json.load(fp=fd)
        RESULT.clear()
        RESULT.update(user_data_d)


# 格式化输出
def user_show(server_response=RESPONSE):
    code = server_response["code"]
    user_info_d = server_response["data"]
    user_info_d_length = len(user_info_d)

    if user_info_d:
        x = PrettyTable()
        x.field_names = FIELD_NAME_L
        for name, other_info_d in user_info_d.items():
            age, phone, email = other_info_d["age"], other_info_d["phone"], other_info_d["email"]
            x.add_row([name, age, phone, email])
        print("\033[33m\n{}\033[0m".format(x))
        print("\033[33m{} row in set.\033[0m".format(user_info_d_length))

    if code == 1000:
        print("\033[36mSuccess.\033[0m")
    else:
        print("\033[31mError, %s\033[0m"% code)
        print("\033[31m%s\033[0m" % server_response["message"])


# 处理用户输入
def get_change_data(data):
    result = {}
    data_l = data.split()
    if data_l[2] != "set":
        return False

    regex = re.compile('\s*update\s*|\s*set\s*|\s*=\s*|\s*,\s*|\s*and\s*')
    user_data_l = regex.split(data)
    user_data_l.pop(user_data_l.index(''))
    user_data_length = len(user_data_l)
    if user_data_length % 2 == 0:
        return False

    username = user_data_l[0]
    result["name"] = username
    result["new_value"] = {}

    field_index_l = list(range(user_data_length))[1::2]
    for id in field_index_l:
        value_id = id +1
        field_name = user_data_l[id]
        value = user_data_l[value_id]
        result["new_value"][field_name] = value

    return result


@time_cal
@user_verification
def main():
    # 加载已存在的用户数据
    load_data()

    method_dict = {
        "add": user_add,
        "delete": user_delete,
        "update": user_update,
        "list": user_list,
        "find": user_find,
    }
    while True:
        user_input = input("INPUT >>:\t").strip()
        if not user_input:
            continue

        user_input_list = user_input.split()
        operator_symbol = user_input_list[0]
        data_list = user_input_list[1:]
        if operator_symbol == "update":
            change_information_l = get_change_data(user_input)
            if not change_information_l:
                continue
            data_list = change_information_l

        if operator_symbol == 'help':
            help_info()

        if operator_symbol == 'q':
            sys.exit(0)

        if operator_symbol not in method_dict:
            print("\033[36mno this operator symbol, u can use help to check.\033[0m")
            continue

        # 调用不同功能函数
        method_dict[operator_symbol](data_list)


if __name__ == "__main__":
    main()



