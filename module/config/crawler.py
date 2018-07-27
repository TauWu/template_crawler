# -*- coding: utf-8 -*-
# crawler config reader

from constant.config import conf_kv_func

class CrawlerConfigReader(object):

    @staticmethod
    def crawler_config(crawler_name):
        # Get system config.
        sys_conf = conf_kv_func("%s.sys_config"%crawler_name, all=True)
        
        # Get list crawler config.
        list_crawler = conf_kv_func("%s.list_crawler"%crawler_name, all=True)
        list_parser  = conf_kv_func("%s.list_parser"%crawler_name, all=True)

        # Get compile config for `re` module.
        compiles     = conf_kv_func("%s.compiles"%crawler_name, all=True)
        
        # Get detail crawler config list. You may have many different configure to get detail infos.
        idx = 0
        detail_crawlers = list()
        detail_parsers  = list()
        while True:
            try:
                idx += 1
                detail_crawler = conf_kv_func("%s.detail_crawler%d"%(crawler_name, idx), all=True)
                detail_parser  = conf_kv_func("%s.detail_parser%d"%(crawler_name, idx), all=True)
            except KeyError:
                print("Load all detail crawler config succeed.")
                break
            else:
                detail_crawlers.append(detail_crawler)
                detail_parsers.append(detail_parser)

        return dict(
            sys_conf        = sys_conf,
            list_crawler    = list_crawler, 
            list_parser     = list_parser,
            detail_crawlers = detail_crawlers,
            detail_parsers  = detail_parsers,
            compiles        = compiles
        )