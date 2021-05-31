#!/usr/bin/python3
# -*- coding utf-8 -*-
from db import db_handler
from lib import common

admin_logger = common.get_logger(log_type='admin')


def change_balance_interface(username, money):
    user_dic = db_handler.select(username)
    if user_dic:
        user_dic['balance'] = int(money)
        # 保存修改后的用户数据
        db_handler.save(user_dic)

        msg = f'管理员修改用户：[{username}]额度成功'
        admin_logger.info(msg)
        return True, '额度修改成功'
    return False, '用户不存在，未修改数据'


def lock_user_interface(username):
    user_dic = db_handler.select(username)
    if user_dic:
        user_dic['locked'] = True
        db_handler.save(user_dic)
        msg = f'用户{username}账户冻结成功'
        admin_logger.info(msg)
        return True, msg

    msg = f'用户{username}不存在'
    return False, msg
