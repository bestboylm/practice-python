#!/usr/bin/env python
# -*-encoding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:         hw_1.py
# Description:  
# Author:       Aaron
# Date:         2020/8/21 10:49
# -------------------------------------------------------------------------------


# 输入6次, 求和计算
def summation():
    res = 0
    for n in range(1, 6):
        while True:
            try:
                user_input = int(input("\033[37m Please input number {}:\t\033[0m".format(n)))
                break
            except Exception as e:
                continue
        res += user_input
    print("\033[36mThe result of six numbers add up to [{}].\n\033[0m".format(res))
    return res


def summation_2(n=1, res=0):
    if n >= 6:
        print("\033[36mThe result of six numbers add up to [{}].\n\033[0m".format(res))
        return res
    user_input = int(input("\033[37m Please input number {}:\t\033[0m".format(n)))
    res += user_input
    n += 1
    return summation_2(n, res)


# 计算1到100的和
def summation_one_to_hundred():
    res = 0
    for n in range(1, 101):
        res += n
    print("The sum from one to one hundred is [{}].\n".format(res))


# 输入数字,输入0结束输入, 求和,求最大值
def summation_and_max_number():
    temp_list = []
    while True:
        try:
            user_input = int(input("Please input a number:\t"))
            temp_list.append(user_input)
        except Exception as e:
            continue

        if user_input == 0:
            break

    sum_from_user_input = sum(temp_list)
    max_number = max(temp_list)
    print("%s = %s\nThe largest number among them is [%s]\n" % (
        "+".join([str(n) for n in temp_list]), sum_from_user_input, max_number))
    return sum_from_user_input, max_number


# 打印乘法口诀
def multiplication_table(second_number=1):
    if second_number > 9:
        return

    for first_number in range(1, second_number + 1):
        equation_s = "%s x %s = %s " % (first_number, second_number, first_number*second_number)
        print("{:<12}".format(equation_s), end="")
    print()
    return multiplication_table(second_number+1)


# 猜100以内数字游戏, 6次机会, 每次提示(正确, 小了, 大了)
def guess_right_number():
    import random
    luck_number = random.randint(0, 100)
    # print("%s tell you answer quiet!!" % luck_number)
    while True:
        user_input = input("Please guess a  number in 0-100:\t")
        if not user_input.isdigit():
            print("\033[31mmust input number!!! try again, please.\033[0m")

        user_number = int(user_input)
        if user_number == luck_number:
            print("\033[36mcongratulations, u win~\033[0m")
            return luck_number

        if user_number < luck_number:
            print("\033[31mThe number from u is too small...\033[0m")
            pass

        if user_number > luck_number:
            print("\033[31mThe number from u is too big...\033[0m")


if __name__ == "__main__":
    summation()
    # summation_2()
    summation_one_to_hundred()
    summation_and_max_number()
    multiplication_table()
    guess_right_number()
