#!/usr/bin/python3
# -*- coding utf-8 -*-
"""
用户视图层
"""

from interface import user_interface
from interface import bank_interface
from interface import shop_interface
from lib import common

login_user = None

# 1. 注册功能

# 面条版
'''
def register():
    while True:

        # 1）让用户输入用户名和密码进行校验
        username = input('请输入用户名: ').strip()
        password = input('请输入密码: ').strip()
        re_password = input('请确认密码: ').strip()

        # 小的逻辑处理：比如两次密码是否一致
        if password == re_password:
            import json
            import os
            from conf import settings

            # 拼接用户的json文件路径
            user_path = os.path.join(
                settings.USER_DATA_PATH, f'{username}.json'
            )
            # 2）查看用户是否存在
            # 2.1) 若存在，提示用户重新输入
            if os.path.exists(user_path):
                print('用户已存在，请重新输入！')
                continue

            # 4) 若不存在，则保存用户数据
            # 4.1) 组织用户的数据的字典信息
            user_dic = {
                'username': username,
                'password': password,
                'balance': 15000,
                # 用于记录用户流水的列表
                'flow': [],
                # 购物车
                'shop_cart': {},
                # locked:用于记录用户是否被冻结
                # False: 未冻结   True: 被冻结
                'locked': False
            }

            # 用户数据， 如tank.json 以用户名创建json文件
            # 4.2)
            # user_path = os.path.join(
            #     settings.USER_DATA_PATH, f'{username}.json'
            # )
            with open(user_path, 'w', encoding='utf-8') as f:
                # ensure_ascii=False 是让中文显示更美观
                json.dump(user_dic, f, ensure_ascii=False)
'''


# 分层版
def register():
    while True:

        # 1）让用户输入用户名和密码进行校验
        username = input('请输入用户名: ').strip()
        password = input('请输入密码: ').strip()
        re_password = input('请确认密码: ').strip()

        if password == re_password:
            # 2）调用接口层的注册接口，讲用户名和密码交给接口层来处理,并获得返回值

            # 返回值为元组，解包赋值：flag, msg ---> (False，‘用户名已存在‘) 或 （True，‘注册成功’）
            flag, msg = user_interface.register_interface(
                username, password
            )

            # 3）根据flag判断用户注册是否成功, flag控制是否break返回前调用函数
            if flag:
                print(msg)
                break
            else:
                print(msg)


# 2. 登录功能
def login():
    # 登录视图
    while True:
        username = input('请输入用户名： ').strip()
        password = input('请输入密码： ').strip()

        # 调用接口层，将数据传给登录接口
        flag, msg = user_interface.login_interface(username, password)
        if flag:
            print(msg)
            global login_user
            login_user = username
            break
        else:
            print(msg)


# 3. 查看余额
@common.login_auth
def check_balance():
    # 直接调用查看余额接口，获取返回值，得到用户余额
    balance = user_interface.check_bal_interface(
        login_user
    )
    print(f'用户{login_user} 账户余额为：{balance}')


# 4. 提现功能
@common.login_auth
def withdraw():
    while True:
        input_money = input('请输入提现金额： ').strip()
        if not input_money.isdigit():
            print('请重新输入')
            continue
        input_money = int(input_money)
        flag, msg = bank_interface.withdraw_interface(
            login_user, input_money
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 5. 还款功能
@common.login_auth
def repay():
    """
    银行卡还款，即充值功能
    :return:
    """
    while True:
        input_money = input('请输入需要还款/充值的金额： ').strip()

        if not input_money.isdigit():
            print('请输入正确的金额')
            continue
        input_money = int(input_money)

        if input_money > 0:
            flag, msg = bank_interface.repay_interface(
                login_user, input_money
            )

            if flag:
                print(msg)
                break
            else:
                print('还款/充值的金额不能小于零！')


# 6. 转账功能
@common.login_auth
def transfer():
    """
    1. 接收用户输入的 转账金额
    2. 接收用户输入的 转账目标用户
    :return:
    """
    while True:
        # 1.让用户输入金额和目标账户
        to_user = input('请输入转账目标用户： ').strip()
        money = input('请输入转账金额： ').strip()
        # 2.判断金额是否是数字 或 > 0
        if not money.isdigit():
            print('please enter correct transfer amount: ')
            continue
        money = int(money)
        if money > 0:
            flag, msg = bank_interface.transfer_interface(
                # 当前用户， 目标用户， 转账金额
                login_user, to_user, money
            )
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('please enter correct transfer amount: ')


# 7. 查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(
        login_user
    )
    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print('没有流水')


# 8. 购物功能
@common.login_auth
def shopping():
    # 本例不从文件中读取商品数据
    # good_list = {
    #     '0':{'name':'上海灌汤包','price':30}
    # }
    good_list = [
        ['上海灌汤包', 30],
        ['抱枕', 330],
        ['凤爪', 28],
        ['鱼丸', 18],
        ['坦克', 818228],
        ['macbook', 28228]
    ]

    # 初始化当前购物车
    shopping_car = {}  # {'商品名称'：['单价','数量']}

    while True:
        # 1.打印商品信息，让客户选择
        # 枚举，enumerate(可迭代对象) ---->(可迭代对象的索引，索引对于的值)
        # 即：---->(0,['上海灌汤包'，30])
        for index, goods in enumerate(good_list):
            goods_name, goods_price = goods[0], goods[1]
            print(f'商品编号为：{index}',
                  f'商品名称：{goods_name}',
                  f'商品价格：{goods_price}')

        # 2.让客户输入选择的商品编号
        choice = input('请输入商品编号(是否结账输入 y or n): ').strip()

        # 2.1 输入 y 进入支付结算功能
        if choice == 'y':
            if not shopping_car:
                print('购物车为空，不能支付，请重新输入！')
                continue
            # 6.调用支付接口进行支付
            flag, msg = shop_interface.shopping_interface(
                login_user, shopping_car
            )
            if flag:
                print(msg)
                break
            else:
                print(msg)

        # 2.2 输入 n 添加购物车
        elif choice == 'n':
            # 判断当前用户是否添加过购物车
            if not shopping_car:
                print('购物车为空，不能添加，请重新输入！')
                continue
            # 7.调用添加购物车接口
            flag, msg = shop_interface.add_shop_car_interface(
                login_user, shopping_car
            )
            if flag:
                print(msg)
                break
            else:
                print(msg)

        if not choice.isdigit():
            continue
        choice = int(choice)

        # 3.判断choice是否存在
        if choice not in range(len(good_list)):
            print('请输入正确的编号！')
            continue

        # 4.获取商品名称和价格
        shop_name, shop_price = good_list[choice]

        # 5.加入购物车
        # 5.1 判断用户选择的商品是否重复，重复则数量+1
        if shop_name in shopping_car:
            # [shop_price,1][1] ----> 1+=1
            shopping_car[shop_name][1] += 1
        else:
            # {'商品名称'：['单价','数量']}
            shopping_car[shop_name] = [shop_price, 1]

        print('当前购物车：', shopping_car)


# 清空购物车功能
#TODO
    pass


# 9. 查看购物车
@common.login_auth
def check_shop_cart():
    shop_cart = shop_interface.check_shop_cart_interface(login_user)
    print(shop_cart)


# 10 管理员功能
@common.login_auth
def admin():
    from core import admin
    admin.admin_run()


# 创建函数功能字典

func_dic = {
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_cart,
    '10': admin,
}


# 视图层主程序


def run():
    while True:
        print('''
        =====ATM + 购物车=====
            1.注册功能
            2.登录功能
            3.查看余额
            4.提现功能
            5.还款功能
            6.转账功能
            7.查看流水
            8.购物功能
            9.购物车
            10.管理员功能 
        ======= E N D ======= 
        ''')

        choice = input('请输入功能编号： ').strip()

        if choice not in func_dic:
            print('请输入正确的功能编号！')
            continue

        func_dic.get(choice)()  # func_dic.get('1')() ---> register()
