# -*- coding: utf-8 -*-
from constant.config import conf_kv_func
from util.web.proxies import ProxiesVaild

class Do(object):

    def __init__(self, crawler_name):
        '''Do object
            You may get much info from appointed crawler files.
            It may include request's type, parser's type and
            so on.
        params:
            crawler_name: Crawler's name, which turns to config
            files in ./config folders.
        '''
        self.crawler_name = crawler_name

    def test_req(self):
        vld = ProxiesVaild(num=10)
        print(vld.vaild_proxies_a)