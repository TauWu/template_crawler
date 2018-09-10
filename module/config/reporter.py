# -*- coding: utf-8 -*-
# Reporter config reader

from constant.config import conf_kv_func

class RPTerConfigReader(object):

    @staticmethod
    def rpter_config(rpter_name):
        
        rpter_name = "rpt_%s"%rpter_name

        # Get Xlsx File Config
        xlsx_conf = conf_kv_func("%s.xlsx"%rpter_name, all=True)

        # Get Recver Config
        recv_conf = conf_kv_func("%s.recv"%rpter_name, all=True)
        recv_conf['recv_mail'] = recv_conf['recv_mail'].split(',')

        return dict(
            xlsx = xlsx_conf,
            recv = recv_conf
        )