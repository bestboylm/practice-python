#!/usr/bin/env python
# -*-encoding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:         user_management.py
# Description:  入门版用户管理系统
# Author:       Aaron
# Date:         2020/8/21 18:23
# -------------------------------------------------------------------------------

# 练习需求如下
# 1. 需要登陆认证, 认证三次失败退出程序
# 2. 有增删改查和搜索功能
#     2.1 增 add   # add Aaron 12 17575481302 aaron@qq.com
#     2.2 删 delete    # delete Aaron
#     2.3 改 update    # update Aaron set age = 18
#     2.4 查 list  # list
#     2.5 搜 find  # find monkey
#
# 3. 格式化输出


import sys


RESULT = []
USER_PROFILE = ('Aaron', '111111')
RESPONSE = {
    "code": 1000,
    "data": [],
    "message": "",
}


# 认证装饰器函数
def login(func):
    def core(*args, **kwargs):
        for n in range(1, 4):
            user_name = input("Please input your name:\t").strip()
            password = input("Please input your password:\t").strip()
            if user_name != USER_PROFILE[0] or password != USER_PROFILE[1]:
                if n == 3:
                    print("\033[31mAuthentication failure, exit\033[0m")
                    sys.exit(0)

                print("\033[35mUsername or password error, try again, please\033[0m")
            else:
                break
        print("\033[36mWelcome %s to login user management system." % user_name)
        return func(*args, **kwargs)
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


# 查询所有用户信息
def u_list(*args):
    if not RESULT:
        RESPONSE["code"] = 1004
        RESPONSE["data"] = []
        RESPONSE["message"] = "\033[33mno any user info, need to add first.\033[0m"
        return RESPONSE

    RESPONSE["code"] = 1000
    RESPONSE["data"] = RESULT
    return RESPONSE


# 搜索指定用户
def u_find(key_l):
    key = key_l[0]
    # print(key)
    if not RESULT:
        RESPONSE["code"] = 1004
        RESPONSE["data"] = []
        RESPONSE["message"] = "\033[33mno any user info, need to add first.\033[0m"
        return RESPONSE

    # print(RESULT)
    for user_info_t in RESULT:
        # print(user_info_t)
        if key == user_info_t[0]:
            RESPONSE["code"] = 1000
            RESPONSE["data"] = []
            RESPONSE["data"].append(user_info_t)
            # print(RESPONSE)
            return RESPONSE

    RESPONSE["code"] = 1004
    RESPONSE["data"] = []
    RESPONSE["message"] = "\033[31mUser %s doesn't exist.\033[0m" % key
    return RESPONSE


def u_add(data_list):
    if len(data_list) != 4:
        RESPONSE["code"] = 1001
        RESPONSE["message"] = "\033[31mdata from you is not enough, check and try again, please.\033[0m"
        return RESPONSE

    name = data_list[0].split()
    # 先查是否有重复
    if u_find(name)["data"]:
        RESPONSE["code"] = 1501
        RESPONSE["message"] = "\033[33mUser info had already existed.\033[0m"
        return RESPONSE

    RESULT.append(tuple(data_list))
    RESPONSE["code"] = 1000
    RESPONSE["data"] = RESULT
    return RESPONSE


# 更改用户信息
def u_update(data_list):
    """

    :param data_list: [key, (field_name, value)]
    :return: True or False
    """
    # field_name_l = ["name", "age", "phone", "email"]
    field_name_d = {
        "name": 0,
        "age": 1,
        "phone": 2,
        "email": 3,
    }
    # print(data_list)
    if not RESULT:
        RESPONSE["code"] = 1004
        RESPONSE["message"] = "\033[33mNo any user info, need to add first.\033[0m"
        return RESPONSE

    key = data_list[0]
    need_reset_field_l = [t[0] for t in data_list[1:]]
    for field_name in need_reset_field_l:
        if field_name not in field_name_d:
            RESPONSE["code"] = 1503
            RESPONSE["message"] = "\033[31mfield name is not true, check please.\033[0m"
            return RESPONSE

    for user_info_t in RESULT:
        if key == user_info_t[0]:
            user_index_in_result = RESULT.index(user_info_t)
            user_info_l = list(user_info_t)
            for new_info_t in data_list[1:]:
                index = field_name_d[new_info_t[0]]
                user_info_l[index] = new_info_t[1]
            new_user_info_t = tuple(user_info_l)
            RESULT.pop(user_index_in_result)
            RESULT.insert(0, new_user_info_t)
            RESPONSE["code"] = 1000
            RESPONSE["data"] = []
            return RESPONSE

    RESPONSE["code"] = 1004
    RESPONSE["message"] = "\033[31mUser %s doesn't exist.\033[0m" % key
    return RESPONSE


# 有bug
def u_delete(key_l):
    key = key_l[0]
    # print(key)
    if not RESULT:
        RESPONSE["code"] = 1004
        RESPONSE["message"] = "\033[33mNo any user info, need to add first.\033[0m"
        return RESPONSE

    for user_info_t in RESULT:
        if key == user_info_t[0]:
            user_index_in_result = RESULT.index(user_info_t)
            RESULT.pop(user_index_in_result)
            RESPONSE["code"] = 1000
            RESPONSE["data"] = []
            return RESPONSE

    RESPONSE["code"] = 1004
    RESPONSE["message"] = "\033[31mUser %s doesn't exist.\033[0m" % key
    return RESPONSE


def u_show():
    if RESPONSE["code"] == 1000:
        print("\033[36mSuccess.\n\033[0m")

    if RESPONSE["code"] == 1000 and RESPONSE["data"]:
        print("{:^10}{:^9}{:^17}{:^27}".format("name", "age", "phone", "email"))
        # print(type(RESPONSE["data"]))
        for user_info_t in RESPONSE["data"]:
            print("| {:^8} | {:^7} | {:^15} | {:^25} |".format(
                user_info_t[0], user_info_t[1], user_info_t[2], user_info_t[3], ))

    if RESPONSE["code"] != 1000:
        print(RESPONSE["message"])


@login
def main():
    method_dict = {
        "add": u_add,
        "delete": u_delete,
        "update": u_update,
        "list": u_list,
        "find": u_find,
    }
    while True:
        user_input = input("INPUT >>:\t").strip()
        if not user_input:
            continue

        user_input_list = user_input.split()
        # import re
        # regex = re.compile("set|=")
        # user_input_list = regex.split(user_input)
        operator_symbol = user_input_list[0]
        data_list = user_input_list[1:]
        if operator_symbol == "update":
            data_list.pop(1)
            data_list.pop(2)
            new_data_t = (data_list[1], data_list[2])
            data_list.append(new_data_t)
            data_list.pop(1)
            data_list.pop(1)

        if operator_symbol == 'help':
            help_info()

        if operator_symbol == 'q':
            sys.exit(0)

        if operator_symbol not in method_dict:
            print("\033[36mno this operator symbol, u can use help to check.\033[0m")
            continue

        # 调用不同功能函数
        method_dict[operator_symbol](data_list)
        u_show()


if __name__ == "__main__":
    main()
    pass



