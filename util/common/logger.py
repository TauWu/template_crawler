# -*- coding: utf-8 -*-

# 日志文件操作模块

import logging
import sys
from .date import Time
import os
import traceback

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

        # You should check if the handler is existed to avoid repeat log records.
        if not logger.handlers:

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
                
            self.file_handler = logging.FileHandler(
                "{log_path}{date}.log".format(
                    log_path=LOG_PJT_PATH, date=Time.now_date_str()
                )
            )
            self.file_handler.setFormatter(formater)
            self.stream_handler = logging.StreamHandler(sys.stderr)
            
            logger.addHandler(self.file_handler)
            logger.addHandler(self.stream_handler)
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
        if self.logger.level == logging.INFO:
            self.logger.warning(
                "[WRN] %s %s"%(
                    msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()])
                )
            )
        elif self.logger.level == logging.DEBUG:
            tb = traceback.format_exc()
            self.logger.warning(
                "[WRN] %s %s\n%s"%(
                    msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()]), tb
                )
            )
        
    def error(self, msg, **kwargs):
        tb = traceback.format_exc()
        self.logger.error(
            "[ERR] %s %s \n%s"%(
                msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()]), tb
            )
        )

    def fatal(self, msg, **kwargs):
        tb = traceback.format_exc()
        self.logger.fatal(
            "[FTL] %s %s\n%s"%(
                msg, " ".join(["{}:{}".format(k, v) for k, v in kwargs.items()]), tb
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