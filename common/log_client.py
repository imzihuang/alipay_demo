#coding:utf-8

import logging
from logging.handlers import TimedRotatingFileHandler
import os
from os import path


def init_logger(log_path):
    """initialize log
    @param log_path: generated log path
    """
    root = path.dirname(log_path)
    if not path.isdir(root):
        os.makedirs(root)

    log = logging.getLogger()
    log.setLevel(logging.NOTSET)

    hdlr = TimedRotatingFileHandler(log_path, when='D', backupCount=10, encoding='utf-8')
    hdlr.setFormatter(logging.Formatter('%(asctime)-15s [%(levelname)s] [%(process)d] [%(threadName)s] %(message)s'))

    log.addHandler(hdlr)

    return log


gen_log = init_logger('./logs/alipay.log')