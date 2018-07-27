# -*- coding: utf-8 -*-
# Request

from util.common.tools import finder
from util.web.proxies import ProxiesRequests

from constant.config import REQUEST_CFG

import json
from lxml import etree

class HTTPListRequest(object):

    def __init__(self, crawler_conf):
        self.crawler = crawler_conf['list_crawler']
        self.sys     = crawler_conf['sys_conf']

    @property
    def list_res_iter(self):
        mutil       = int(REQUEST_CFG["mutil"])
        crawler     = self.crawler
        method      = int(crawler['method'])
        params      = crawler["params"]
        url_tpl     = crawler["list_url"]
        find_total  = crawler["total"].split('.')

        # Result set.
        url_list    = list()
        data_list   = list()
        end_flag    = True

        try:
            params = int(params)
        except Exception:
            print("Here is another method.")
            # if `params` is not an integer, you may get data from redis.
            raise

        idx = 0
        while end_flag:

            url_list = list()

            for idxx in range(0, mutil):
                url_list.append(url_tpl.format(idx+idxx*params))
                if method == 3:
                    data = json.loads(self.crawler['data'])
                    data[self.crawler['data_key']] = idx+idxx*params
                    data_list.append(data)
                    
            if method == 1:
                mutil_req = ProxiesRequests(url_list)
            elif method == 2:
                mutil_req = ProxiesRequests(url_list)
            elif method == 3:
                mutil_req = ProxiesRequests(url_list, data_list=data_list)

            if "headers" in self.sys.keys():
                mutil_req.add_headers(json.loads(self.sys['headers']))

            res_list  = mutil_req.req_content_list
            
            for res in res_list:
                if method == 1 or method == 3:
                    res = json.loads(res[0].decode('utf-8'))
                    try:
                        total = finder(res, find_total)
                        print("totaldebug:{}".format(total))
                        if idx > int(total) and end_flag:
                            end_flag = False
                    except Exception:
                        total = 999
                else:
                    try:
                        res = etree.HTML(res[0].decode('utf-8'))
                        total = res.xpath(crawler['total'])[0].xpath('./text()')[0]
                        print("totaldebug:{}".format(total))
                    except Exception as e:
                        total = 999
                        print('ERR: total {}'.format(e))
                    if idx > int(total) and end_flag:                        
                        end_flag = False
                yield res
                                
            idx += params*mutil
            print("idxdebug {}".format(idx))

            # Here is a debugger.
            # if idx > 0:
            #     break

class HTTPDetailRequest(object):

    def __init__(self, rds, crawler_conf):
        self.rds = rds
        self.crawler_conf = crawler_conf
        self.sys          = crawler_conf['sys_conf']

    @property
    def detail_res_iter(self):
        '''detail_res_iter
        '''
        for urls, task, idxx_list in self.__detail_task__:
            mutil_req = ProxiesRequests(urls)
            if "headers" in self.sys.keys():
                mutil_req.add_headers(json.loads(self.sys['headers']))
            res_list = mutil_req.req_content_list
            for res, idxx in zip(res_list, idxx_list):
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
        mutil           = int(REQUEST_CFG["mutil"])
        task            = int(task)
        params          = crawler['params'].split('.')
        url             = crawler['detail_url']
        url_list        = list()
        rds_idx_list    = list()
                
        for kx, _ in self.__show_all_in_redis__:
            
            rds_idx = kx.split('.')
            idxx = rds_idx[:len(params)]
            url_req = url.format(*idxx)
            url_list.append(url_req)
            rds_idx_list.append(rds_idx)
            if len(url_list) >= mutil:
                yield url_list, task, rds_idx_list
                url_list = list()
                rds_idx_list= list()
    
    @property
    def __show_all_in_redis__(self):
        '''__show_all_in_redis__
        '''
        yield from self.rds.rscan