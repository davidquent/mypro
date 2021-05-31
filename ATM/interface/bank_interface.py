#!/usr/bin/python3
# -*- coding utf-8 -*-
'''
银行相关业务的接口
'''

from db import db_handler
from lib import common

bank_logger = common.get_logger(log_type='bank')


# 提现接口（手续费5%）
def withdraw_interface(username, money):
    # 1.先获取用户字典
    user_dic = db_handler.select(username)
    # 校验用户的钱是否足够
    balance = int(user_dic.get('balance'))
    money2 = int(money) * 1.05
    if balance >= money2:
        balance -= money2
        user_dic['balance'] = balance

        # 记录流水
        flow = f'用户[{username}]提现金额[￥{money}]成功，手续费为：[￥{money2 - float(money)}]'
        user_dic['flow'].append(flow)
        bank_logger.info(flow)
        # 保存更新数据
        db_handler.save(user_dic)

        return True, flow

    return False, '提现金额不足，请重新输入'


# 还款接口
def repay_interface(username, money):
    '''
    1.获取用户的金额
    2.给用户的金额加钱的操作
    :return:
    '''
    # 1.获取用户字典
    user_dic = db_handler.select(username)

    # 2.直接加钱操作
    # user_dic['balance'] ---> int
    user_dic['balance'] += money

    # 记录流水
    flow = f'用户：[{username}]  还款/充值：[￥{money}] 成功'
    user_dic['flow'].append(flow)

    # 3.调用数据处理层，保存修改后的数据
    db_handler.save(user_dic)
    bank_logger.info(flow)
    return True, flow


# 转账接口
def transfer_interface(login_user,to_user, money):
    '''
    :param login_user: 当前用户
    :param to_user: 目标用户
    :param money: 转账金额
    :return:
    '''
    login_user_dic = db_handler.select(login_user)
    to_user_dic = db_handler.select(to_user)
    if not to_user_dic:
        return False, 'ERROR: transfer target account does not exist'
    # 判断余额是否足够
    if login_user_dic['balance'] >= money:
        # 足够，开始转账
        # 当前用户账户减钱
        login_user_dic['balance'] -= money
        # 目标账户加钱
        to_user_dic['balance'] += money

        # 记录流水
        # 当前用户
        login_user_flow = f'用户：[{login_user}] 给 用户：[{to_user}] 转账：[￥{money}] 成功！'
        login_user_dic['flow'].append(login_user_flow)
        # 目标用户
        to_user_flow = f'用户：[{to_user}] 接收 用户：[{login_user}] 转账：[￥{money}] 成功！'
        to_user_dic['flow'].append(to_user_flow)

        # 保存用户数据
        db_handler.save(login_user_dic)
        db_handler.save(to_user_dic)

        bank_logger.info(login_user_flow)
        bank_logger.info(to_user_flow)

        return True, login_user_flow

    return False, 'Insufficient balance，the transfer was unsuccessful！'


# 查看流水接口
def check_flow_interface(login_user):
    user_dic = db_handler.select(login_user)
    return user_dic.get('flow')


# 支付接口
def pay_interface(login_user, cost):
    user_dic = db_handler.select(login_user)

    # 判断用户余额是否足够
    if user_dic.get('balance') >= cost:
        user_dic['balance'] -= cost
        flow = f'用户消费金额：[￥{cost}]'
        user_dic['flow'].append(flow)
        db_handler.save(user_dic)
        bank_logger.info(flow)
        return True
    return False
