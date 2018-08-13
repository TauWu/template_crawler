# -*- coding: utf-8 -*-

# 日志文件操作模块

import logging
import sys
from .date import Time
import os

class LogBase(object):
    """Log base service

    """
    def __init__(self, project_name, logger_name):
        '''class log_base
        params:
            project_name
            logger_name
        '''
        logger = logging.getLogger(logger_name)
        formater = logging.Formatter(
            'P:%(process)-5s T:%(threadName)s %(asctime)s [%(name)s] \t%(message)s',
            r'%Y/%m/%d %H:%M:%S'
        )

        LOG_BASE_PATH = "./log"
        LOG_PJT_PATH  = "./log/%s/"%project_name

        if not os.path.exists(LOG_BASE_PATH):
            os.mkdir(LOG_BASE_PATH)
            
        if not os.path.exists(LOG_PJT_PATH):
            os.mkdir(LOG_PJT_PATH)
            
        file_handler = logging.FileHandler(
            "{log_path}{date}.log".format(
                log_path=LOG_PJT_PATH, date=Time.now_date_str()
            )
        )
        file_handler.setFormatter(formater)
        stream_handler = logging.StreamHandler(sys.stderr)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(logging.INFO)
    
        self.logger = logger

    def debug(self, msg, **kwargs):
        self.logger.debug(
            "[DBG] %s %s"%(
                msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()])
            )
        )
        
    def info(self, msg, **kwargs):
        self.logger.info(
            "[INF] %s %s"%(
                msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()])
            )
        )

    def warning(self, msg, **kwargs):
        self.logger.warning(
            "[WRN] %s %s"%(
                msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()])
            )
        )
    def error(self, msg, **kwargs):
        self.logger.err(
            "[ERR] %s %s"%(
                msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()])
            )
        )
    def fatal(self, msg, **kwargs):
        self.logger.fatal(
            "[FTL] %s %s"%(
                msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()])
            )
        )

    def dbg(self, msg, **kwargs):
        "rename debug"
        self.debug(msg, **kwargs)

    def inf(self, msg, **kwargs):
        "rename info"
        self.info(msg, **kwargs)

    def wrn(self, msg, **kwargs):
        "rename warning"
        self.warning(msg, **kwargs)

    def warn(self, msg, **kwargs):
        "rename warning"
        self.warning(msg, **kwargs)

    def err(self, msg, **kwargs):
        "rename error"
        self.error(msg, **kwargs)

    def ftl(self, msg, **kwargs):
        "rename fatal"
        self.fatal(msg, **kwargs)