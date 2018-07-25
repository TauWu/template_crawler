# -*- coding: utf-8 -*-
# Request HTTP APIs

from util.common.tools import finder
from util.web.proxies import ProxiesRequests

from constant.config import REQUEST_CFG

import json

class HTTPListRequest(object):

    def __init__(self, crawler_conf):
        self.crawler = crawler_conf

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
        end_flag    = True

        try:
            params = int(params)
        except Exception:
            print("Here is another method.")
            # if `params` is not an integer, you may get data from redis.
            raise

        idx = 0
        while end_flag:

            for idxx in range(0, mutil):
                url_list.append(url_tpl.format(idx+idxx*params))
            
            mutil_req = ProxiesRequests(url_list)
            res_list  = mutil_req.req_content_list
            
            for res in res_list:
                res = json.loads(res[0].decode('utf-8'))
                total = finder(res, find_total)
                if idx > total and end_flag:
                    end_flag = False
                yield res
            
            idx += params*mutil

            # Here is a debugger.
            if idx > 0:
                break

class HTTPDetailRequest(object):

    def __init__(self, crawler_conf):
        self.crawler = crawler_conf

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
        end_flag    = True

        try:
            params = int(params)
        except Exception:
            print("Here is another method.")
            # if `params` is not an integer, you may get data from redis.
            raise

        idx = 0
        while end_flag:

            for idxx in range(0, mutil):
                url_list.append(url_tpl.format(idx+idxx*params))
            
            mutil_req = ProxiesRequests(url_list)
            res_list  = mutil_req.req_content_list
            
            for res in res_list:
                res = json.loads(res[0].decode('utf-8'))
                total = finder(res, find_total)
                if idx > total and end_flag:
                    end_flag = False
                yield res
            
            idx += params*mutil

            # Here is a debugger.
            if idx > 0:
                break

