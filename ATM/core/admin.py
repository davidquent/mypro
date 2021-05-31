#!/usr/bin/python3
# -*- coding utf-8 -*-

from core import src
from interface import admin_interface


def add_user():
    src.register()


def change_balance():
    while True:
        # 1.输入需要修改的用户名
        change_user = input('请输入需要修改额度的用户： ').strip()
        # 2.修改的用户额度
        money = input('请输入需要修改的用户额度： ').strip()
        if not money.isdigit():
            continue
        # 3.调用修改额度的接口
        flag, msg = admin_interface.change_balance_interface(
            change_user, money
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)


def lock_user():
    while True:
        # 1.输入需要修改的用户名
        change_user = input('请输入需要冻结的用户： ').strip()

        flag, msg = admin_interface.lock_user_interface(change_user)
        if flag:
            print(msg)
            break
        else:
            print(msg)

admin_func = {
    '1': add_user,
    '2': change_balance,
    '3': lock_user,
}


def admin_run():
    while True:
        print(
            '''
        1.添加账户
        2.修改额度
        3.冻结账户
        '''
        )
        choice = input('请输入管理员功能编号： ').strip()

        if choice not in admin_func:
            print('请输入正确的功能编号！')
            continue
        admin_func.get(choice)()
