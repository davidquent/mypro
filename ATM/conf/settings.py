#!/usr/bin/python3
# -*- coding utf-8 -*-
"""
存放配置信息
"""
import os

# 获取项目根目录路径
BASE_PATH = os.path.dirname(
    os.path.dirname(__file__)
)

# 获取user_data文件夹目录路径

USER_DATA_PATH = os.path.join(
    BASE_PATH, 'db', 'user_data'
)

# print(USER_DATA_PATH)

# logging的配置信息
"""
logging配置
"""

# 定义三种日志的输出格式 开始
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'  # name为getlogger指定的名字
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s]%(message)s'

# 定义三种日志的输出格式 结束
# **********注意1：log文件的目录

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
logfile_dir = os.path.join(BASE_PATH, 'log')

# **********注意2： log文件名
logfile_name = 'ATM.log'

if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

LOGGING_DIC = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": standard_format
        },
        "simple": {
            "format": simple_format
        }
    },
    "filters": {},
    "handlers": {
        # 打印到终端的日志
        "console": {
            "class": "logging.StreamHandler",  # 打印到终端屏幕
            "level": "DEBUG",
            "formatter": "simple"
            # "stream": "ext://sys.stdout"
        },
        # 打印到文件的日志，收集info及以上的日志
        "default": {
            "class": "logging.handlers.RotatingFileHandler",  # 保存到文件
            "level": "INFO",
            "formatter": "standard",
            "filename": logfile_path,  # 日志文件
            "maxBytes": 10485760,  # 日志大小 10M
            "backupCount": 10,
            "encoding": "utf-8"  # 日志文件的编码，防止中文log乱码
        },
    },
    "loggers": {
        # logging.getLogger(__name__)拿到的logger配置
        "": {
            "handlers": ["default"],   # 这里可以把上面定义的两个handler都加上，即log数据既写入文件也打印到终端
            "level": "DEBUG",
            "propagate": True,  # 向上(更高level的logger)传递
        },
    },
}
