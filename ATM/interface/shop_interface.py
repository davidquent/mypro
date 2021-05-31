#!/usr/bin/python3
# -*- coding utf-8 -*-
'''
购物商城接口
'''

from db import db_handler
from lib import common

shop_logger = common.get_logger(log_type='shop')


# 商品准备结算接口
def shopping_interface(login_user, shopping_car):
    # 1 计算消费总额
    #      key ：value
    # {‘商品名称’：[]}
    cost = 0
    for price_number in shopping_car.values():
        price, number = price_number
        cost += (price * number)

    # 导入银行接口
    from interface import bank_interface
    flag = bank_interface.pay_interface(login_user, cost)
    if flag:
        msg = '支付成功，准备发货'
        shop_logger.info(msg)
        return True, msg

    msg = '支付失败，金额不足'
    shop_logger.info(msg)
    return False, msg


# 添加购物车接口
def add_shop_car_interface(login_user, shopping_car):
    # 1.获取当前用户的购物车
    user_dic = db_handler.select(login_user)
    # 获取用户文件中的商品数据
    shop_cart = user_dic.get('shop_cart')

    # 2.添加购物车
    # 2.1 判断当前用户选择的商品是否已经存在
    # shopping_car -----> {'商品名':[]}
    for good_name, price_number in shopping_car.items():
        # 每个商品的数量
        number = price_number[1]
        # 2.2 若商品存在，则累加商品数量
        if good_name in shop_cart:
            user_dic['shop_cart'][good_name][1] += number
        else:
            user_dic['shop_cart'].update(
                {good_name: price_number}
            )
        db_handler.save(user_dic)

    return True, '添加购物车成功'


# 查看购物车接口
def check_shop_cart_interface(username):
    user_dic = db_handler.select(username)
    return user_dic.get('shop_cart')
