# -*- coding: utf-8 -*-
# Request

from util.common.tools import finder
from util.web.proxies import ProxiesRequests
from util.common.logger import LogBase

from constant.config import REQUEST_CFG

import json, re
from lxml import etree
from copy import deepcopy

class HTTPListRequest(LogBase):

    def __init__(self, crawler_conf, project_name="sample"):
        LogBase.__init__(self, project_name, "ReqList")
        self.project_name   = project_name
        self.crawler        = crawler_conf['list_crawler']
        self.sys            = crawler_conf['sys_conf']
        self.compiles       = crawler_conf['compiles']

    @property
    def list_res_iter(self):
        mutil       = int(REQUEST_CFG["mutil"])
        crawler     = self.crawler
        method      = int(crawler['method'])
        compiles    = self.compiles

        if 'childpath' in crawler.keys():
            childpath = crawler['childpath'].split(',')
        else:
            childpath = ['']

        if method == 2:
            for cpath in childpath:
                mutil_req_iter = HTTPListRequest.__mutil_req__(self.project_name, method, mutil, crawler, cpath=cpath)

                for mutil_req, cursor in mutil_req_iter:

                    total = 999999

                    if "headers" in self.sys.keys():
                        mutil_req.add_headers(json.loads(self.sys['headers']))
                        
                    res_list  = mutil_req.req_content_list

                    for res in res_list:

                        try:    
                            res = etree.HTML(res[0].decode('utf-8'))

                            if 'total' in compiles:
                                total = re.findall(compiles['total'], (etree.tostring(res.xpath(crawler['total'])[0]).decode('utf-8')))[0]
                            else:
                                total = res.xpath(crawler['total'])[0].xpath('./text()')[0]
                            self.info("Show total pages =>", total=total)
                        except IndexError:
                            self.error("Total break IndexError")
                            total = 0
                        except UnicodeDecodeError:
                            self.error("Total break UnicodeDecodeError")
                            total = 99999
                        except Exception as e:
                            self.error('Total break Error', err=e)
                        finally:                    
                            yield res

                    if cursor > int(total):
                        break

                    # break   # debug code

                    
        elif method == 1:
        
            mutil_req_iter = HTTPListRequest.__mutil_req__(self.project_name, method, mutil, crawler)

            for mutil_req, cursor in mutil_req_iter:

                total = 999999

                if "headers" in self.sys.keys():
                    mutil_req.add_headers(json.loads(self.sys['headers']))
                    res_list  = mutil_req.req_content_list

                    for res in res_list:

                        try:
                            res = etree.HTML(res[0].decode('utf-8'))
                            total = res.xpath(crawler['total'])[0].xpath('./text()')[0]
                            self.info("Show total pages =>", total=total)
                        except Exception as e:
                            self.error('Total break Error', err=e)
                        
                        yield res
                    
                    if cursor > int(total):                   
                        break
        
        else:

            mutil_req_iter = HTTPListRequest.__mutil_req__(self.project_name, method, mutil, crawler)

            for mutil_req, cursor in mutil_req_iter:

                total = 999999

                if "headers" in self.sys.keys():
                    mutil_req.add_headers(json.loads(self.sys['headers']))
                    res_list  = mutil_req.req_content_list

                    for res in res_list:

                        try:
                            res = json.loads(res[0].decode('utf-8'))
                            total = res[crawler['total']]
                            self.info("Show total pages =>", total=total)
                        except Exception as e:
                            self.error('Total break Error', err=e)
                        
                        yield res
                    
                    if cursor > int(total):                   
                        break



    @staticmethod
    def __mutil_req__(project_name, method, mutil, crawler, **kwargs):
        '''__mutil_req__
        req with different config.
        '''
        if 'cpath' in kwargs:
            cpath      = kwargs['cpath']

        if 'params' in crawler.keys():
            params     = int(crawler['params'])

        if 'list_url' in crawler.keys():
            url_tpl    = crawler['list_url']

        if 'pageshow' in crawler.keys():
            pageshow   = int(crawler['pageshow'])

        if 'data' in crawler.keys():
            data       = json.loads(crawler['data'])

        if 'data_key' in crawler.keys():
            data_key   = crawler['data_key']

        if method == 1:
            yield from HTTPListRequest.__req_get_api__(project_name, mutil, url_tpl, params)

        elif method == 2:
            yield from HTTPListRequest.__req_get_web__(project_name, mutil, url_tpl, cpath, pageshow)
        
        elif method == 3:
            yield from HTTPListRequest.__req_post_api__(project_name, mutil, url_tpl, data, data_key)

    @staticmethod
    def __req_get_api__(project_name, mutil, url_tpl, params):
        '''__req_get_api__
        method = 1
        '''
        idx         = 0
        
        while True:
            url_list = list()
            
            for idxx in range(0, mutil):
                url_list.append(url_tpl.format(idx+idxx*params))

            idx += params * mutil 
            yield ProxiesRequests(url_list, project_name), idx
            
            

    @staticmethod
    def __req_get_web__(project_name, mutil, url_tpl, cpath, pageshow):
        '''__req_get_web__
        method = 2
        '''
        # for cpath in childpath:
        idx       = 0
        while True:
            
            url_list  = list()
        
            for idxx in range(0, mutil):
                url_list.append(url_tpl.format(cpath, idx+idxx))

            idx += mutil
            yield ProxiesRequests(url_list, project_name), idx*pageshow

            

    @staticmethod
    def __req_post_api__(project_name, mutil, url_tpl, data, data_key):
        '''__req_post_api__
        method = 3
        '''
        idx         = 0
        
        while True:
            url_list    = list()
            data_list   = list()

            for idxx in range(0, mutil):
                url_list.append(url_tpl.format(idx+idxx))
                data[data_key] = idx+idxx
                data_list.append(deepcopy(data))
            idx += mutil
            yield ProxiesRequests(url_list, project_name, data_list=data_list), idx


class HTTPDetailRequest(LogBase):

    def __init__(self, rds, crawler_conf, project_name="sample"):
        LogBase.__init__(self, project_name, "ReqDetail")
        self.project_name   = project_name
        self.rds            = rds
        self.crawler_conf   = crawler_conf
        self.sys            = crawler_conf['sys_conf']

    @property
    def detail_res_iter(self):
        '''detail_res_iter
        '''
        for urls, task, idxx_list in self.__detail_task__:
            mutil_req = ProxiesRequests(urls, self.project_name)
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

    
    @property
    def detail_res_cookie_iter(self):
        '''detail_res_cookie_iter
        Detail result of request with cookies iter.
        '''
        rds_key         = self.crawler_conf['sys_conf']['redis_key']
        rds_keyx        = rds_key.split('.')
        mutil           = int(REQUEST_CFG["mutil"])
        url_tpl_dict    = dict()
        rds_kv_list     = list()
        flag            = True

        rds_data_iter = self.__show_all_in_redis__

        while flag:

            try:
                kx = next(rds_data_iter)[0]
            
                rds_idx     = kx.split('.')
                rds_kv      = dict(zip(rds_keyx, rds_idx))

                url_lists = {
                    str(idx):v["detail_url"].format_map(rds_kv)
                    for idx, v in enumerate(
                        self.crawler_conf['detail_crawlers']
                    )
                }

                rds_kv_list.append(rds_kv)
            
            except Exception:
                self.info("Iter is over, exit...")
                flag = False

            finally:
                
                for idx, url in url_lists.items():

                    if str(idx) not in url_tpl_dict.keys():
                        url_tpl_dict[str(idx)] = []

                    if len(url_tpl_dict[str(idx)]) >= mutil or flag == False:

                        req = ProxiesRequests(url_tpl_dict['0'], self.project_name, need_cookies=True)
                        if "headers" in self.sys.keys():
                            req.add_headers(json.loads(self.sys['headers']))
                        
                        ctn         = req.req_content_list
                        res_list    = ctn[0]
                        cookies     = ctn[1]
                        idxx        = 0
                        q_cookies   = dict()

                        for res, rds_kv in zip(res_list, rds_kv_list):
                            yield res[0], rds_kv, idxx

                        for k in url_tpl_dict.keys():
                            if k == '0':
                                continue
                            idxx += 1
                            extra_req = ProxiesRequests(url_tpl_dict[k], self.project_name)

                            if 'cookies_key' in self.sys.keys():
                                q_cookies[self.sys['cookies_key']] = cookies[self.sys['cookies_key']]
                                extra_req.add_cookies_dict(
                                    q_cookies
                                )

                            if "headers" in self.sys.keys():
                                extra_req.add_headers(json.loads(self.sys['headers']))

                            res_list = extra_req.req_content_list

                            for res, rds_kv in zip(res_list, rds_kv_list):
                                yield res[0], rds_kv, idxx
                            
                        url_tpl_dict    = {k:[] for k in url_tpl_dict.keys()}
                        rds_kv_list     = rds_kv_list[mutil:]
                        
                    url_tpl_dict[str(idx)].append(url)