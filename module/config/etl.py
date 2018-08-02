# -*- coding: utf-8 -*-
# ETL config reader

from constant.config import conf_kv_func

class ETLConfigReader(object):

    @staticmethod
    def etl_config(etl_name):
        
        etl_name = "etl_%s"%etl_name
        
        # Get system config.
        sys_conf = conf_kv_func("%s.sys_config"%etl_name, all=True)

        return dict(
            sys_conf        = sys_conf
        )