# -*- coding: utf-8 -*-
from module.config.crawler import CrawlerConfigReader
from module.request.test import HTTPProxiesTest
from module.request.http import HTTPListRequest

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
        self.list_dat_iter      = self.__parser_list__
        self.detail_res_iter    = self.__req_detail__
        self.detail_dat_iter    = self.__parser_detail__

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
        
        req = HTTPListRequest(self.crawler_conf["list_crawler"])
        yield from req.list_res_iter

    @property
    def __parser_list__(self):
        '''__parser_list__
        Parse the data from req of list websites/APIs.
        '''
        parser = self.crawler_conf["list_parser"]
        find_data = parser["data_path"].split('.')
        parser.pop('data_path')

        for result in self.list_res_iter:
            data_list = finder(result, find_data)
            for data in data_list:
                rtn_data = dict()
                for k, v in zip(parser.keys(), parser.values()):
                    rtn_data[k] = data[v]
                self.__update_dict_to_redis__(".".join([rtn_data[k] for k in self.rds_key.split('.')]), rtn_data)

    @property
    def __parser_detail__(self):
        '''__parser_detail__
        '''
        import json 
        for res, task, idxx in self.detail_res_iter:
            crawler = self.crawler_conf['detail_crawlers'][task-1]
            parser = self.crawler_conf['detail_parsers'][task-1]

            if int(crawler['method']) == 2:
                continue

            find_data = parser["data_path"].split('.')            
            parser.pop('data_path')
            rtn_data = dict()
            res = json.loads(res.decode('utf-8'))
            data = finder(res, find_data)
            for k, v in zip(parser.keys(), parser.values()):
                rtn_data[k] = data[v]
                self.__update_dict_to_redis__('.'.join(idxx), rtn_data)
            parser['data_path'] = '.'.join(find_data)


    @property
    def __req_detail__(self):
        import json
        
        for urls, task, idxx in self.__detail_task__:
            req = ProxiesRequests(urls)
            res_list = req.req_content_list
            for res in res_list:
                yield res[0], task, idxx

    @property
    def __detail_task__(self):
        '''__detail_task__
        '''
        for idx, c in zip(range(1, 1+len(self.crawler_conf['detail_crawlers'])), self.crawler_conf['detail_crawlers']):
            yield from self.__detail__(idx, c)

    def __detail__(self, task, crawler):
        '''__detail__
        params:
            task: task No.
        '''
        mutil    = int(REQUEST_CFG["mutil"])
        task     = int(task)
        params   = crawler['params'].split('.')
        url      = crawler['detail_url']
        url_list = list()
                
        for kx, _ in self.__show_all_in_redis__:
            
            idxx = kx.split('.')[:len(params)]
            url_req = url.format(*idxx)
            url_list.append(url_req)
            if len(url_list) >= mutil:
                yield url_list, task, idxx
                url_list = list()
    
    @property
    def __show_all_in_redis__(self):
        '''__show_all_in_redis__
        '''
        yield from self.rds.rscan

    def __update_dict_to_redis__(self, k, v):
        import json
        
        if self.rds.rget(k) is not None:
            bf_val = self.rds.rget(k)
            try:
                bf_val = json.loads(bf_val)
                bf_val = dict(bf_val, **v)
                self.rds.rset(k, bf_val)
            except Exception as e:
                print("__update_dict_to_redis__ failed. {}".format(e))
                pass
        else:
            self.rds.rset(k, v)