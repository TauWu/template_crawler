# -*- coding: utf-8 -*-
from module.config.crawler import CrawlerConfigReader
from module.request.test import HTTPProxiesTest
from module.request.http import HTTPListRequest, HTTPDetailRequest
from module.parser.detail import ParserDetail
from module.parser.list import ParserList

from util.common.tools import finder
from util.redis import RedisController
from util.web.proxies import ProxiesRequests
from constant.config import REQUEST_CFG


class Do(object):

    @staticmethod
    def test(self):
        '''test
        Request IP test URL to ensure the proxies is enabled.
        '''
        HTTPProxiesTest.test()

    def __init__(self, crawler_name):
        '''Do object
            You may get much info from appointed crawler files.
            It may include request's type, parser's type and
            so on.
        params:
            crawler_name: Crawler's name, which turns to config
            files in ./config folders.
        '''
        # var
        self.crawler_name = crawler_name
        self.req_order    = list()
        self.crawler_conf = dict()
        
        # init
        self.__load__

        self.do()       # debug code

    def do(self):
        '''do
        Start Process from here.
        '''
        self.list_res_iter      = self.__req_list__
        self.__parser_list__
        
        self.detail_res_iter    = self.__req_detail__
        self.__parser_detail__

    @property
    def __load__(self):
        '''__load__
        Load crawler config detail info from config files.
        '''
        self.crawler_conf = CrawlerConfigReader.crawler_config(self.crawler_name)
        self.rds          = RedisController(int(self.crawler_conf['sys_conf']['redis_db']))
        self.rds_key      = self.crawler_conf['sys_conf']['redis_key']
        # Here is a log about read crawler config info succeed.

    @property
    def __req_list__(self):
        '''__req_list__
        Start a request to get list info from list websites/APIs.
        '''
        # You are supposed to create a child process to do this.
        
        req = HTTPListRequest(self.crawler_conf)
        yield from req.list_res_iter

    @property
    def __req_detail__(self):
        '''__req_detail__
        Start a request to get detail info from web page.
        '''
        # You are supposed to create a child process to do this.

        req = HTTPDetailRequest(self.rds, self.crawler_conf)
        yield from req.detail_res_iter

    @property
    def __parser_list__(self):
        '''__parser_list__
        Parse the data from req of list websites/APIs.
        '''
        parser = ParserList(self.list_res_iter, self.crawler_conf, self.rds, self.rds_key)
        parser.save

    @property
    def __parser_detail__(self):
        '''__parser_detail__
        Parse the data from req of detail websites/APIs
        '''
        parser = ParserDetail(self.detail_res_iter, self.crawler_conf, self.rds)
        parser.save