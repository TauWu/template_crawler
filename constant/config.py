# -*- coding: utf-8 -*-
import os
from util.config import ConfigReader

# Lambda Functions about conf_path
# Return path lead to appointed config file.
conf_path_func = lambda config : '{}/config/{}.cfg'.format(os.getcwd(), config)
conf_kv_func   = lambda load, *k, **kwargs: ConfigReader.read_section_key(conf_path_func(load.split('.')[0]), load.split('.')[1], *k, **kwargs)

# Basic Config Value.
REDIS_CFG   = conf_kv_func("sys.redis", all=True)
MYSQL_CFG   = conf_kv_func("sys.database", all=True)
PROXY_CFG   = conf_kv_func("sys.proxy", all=True)
REQUEST_CFG = conf_kv_func("sys.request", all=True)
BD_MAP_CFG  = conf_kv_func("sys.bd_map", all=True)
EMAIL_CFG    = conf_kv_func("sys.email", all=True)