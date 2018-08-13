# Parser Detail
# Parse detail page

from util.common.tools import finder
from module.parser.extra import *
from constant.config import REQUEST_CFG

import asyncio
import json
import re
from os import remove, walk
from lxml import etree

class ParserDetail(object):

    def __init__(self, crawler_name, detail_res_iter, crawler_conf, rds):
        self.detail_res_iter = detail_res_iter
        self.crawler_conf    = crawler_conf
        self.crawler_name    = crawler_name
        self.rds             = rds
        self.compiles        = crawler_conf['compiles']
        self.mutil           = int(REQUEST_CFG['mutil'])
        self.task_dict       = dict()
        self.task_dict_dtl   = dict()

    @property
    def save(self):
        '''save
        Save parsed data into redis.
        '''
        flag = True
        while flag:

            try:
                res, rds_kv, idx = next(self.detail_res_iter)

                crawler     = self.crawler_conf['detail_crawlers'][idx]
                parser      = self.crawler_conf['detail_parsers'][idx]
                
                rtn_key  = ".".join([rds_kv[k] for k in self.crawler_conf['sys_conf']['redis_key'].split('.')])
                rtn_data = dict()
                
                # Request by HTML Web page.
                if int(crawler['method']) == 2:

                    xml_data = etree.HTML(res)
                    for k, v in zip(parser.keys(), parser.values()):
                        try:
                            if k in self.compiles.keys():
                                rtn_data[k] = re.findall(self.compiles[k], etree.tostring(xml_data.xpath(v)[0]).decode('utf-8'))[0]
                            else:
                                rtn_data[k] = xml_data.xpath(v)[0].xpath('./text()')[0].strip()
                        except Exception as e:
                            print("Err: {}".format(e))

                    try:
                        self.task_dict = dict(
                            {rtn_key:rtn_data}, **self.task_dict
                        )
                    except Exception as e:
                        print(e)
                    self.rds.__update_dict_to_redis__(rtn_key, rtn_data)
                    
                # Request by HTTP Api.
                else:
                    find_data = parser["data_path"].split('.')            
                    parser.pop('data_path')        
                    res = json.loads(res.decode('utf-8'))
                    try:
                        data = finder(res, find_data)
                        for k, v in zip(parser.keys(), parser.values()):
                            v_data = finder(data, v.split('.'))
                            rtn_data[k] = v_data
                        try:
                            self.task_dict = dict(
                                {rtn_key:rtn_data}, **self.task_dict
                            )
                        except Exception as e:
                            print(e)
                            
                        if len(self.task_dict.items()) == 0:
                            self.rds.__update_dict_to_redis__(rtn_key, rtn_data)
                            
                    except Exception as e:
                        print("Parse Detail Error! Err:{} Result:{}".format(e, res))
                    finally:
                        parser['data_path'] = '.'.join(find_data)
                        rtn_data = dict()

            except Exception:
                flag = False
            
            if len(self.task_dict.items()) >= self.mutil or not flag:
                loop = asyncio.get_event_loop()
                data = loop.run_until_complete(self.aextra(loop))
                if data:
                    for k, p in data.items():
                        self.rds.__update_dict_to_redis__(k, p)
                    self.task_dict = dict()

    async def aextra(self, loop):
        '''aextra
        Mutil io about extra func.
        '''
        
        try:
            eval("{}_extra".format(self.crawler_name))
        except Exception:
            return False

        task_dict = self.task_dict
        k_list = list()     # Key List
        v_list = list()     # Val List
        t_list = list()     # Tsk List

        for k, v in zip(task_dict.keys(), task_dict.values()):
            k_list.append(k)
            v_list.append(v)

        # Create task list.
        for k, v in zip(k_list, v_list):
                        
            t_list.append(
                loop.run_in_executor(
                    None, eval, *("{}_extra({}, {})".format(
                        # Use inner func eval to call function with string.
                        self.crawler_name, k, v
                    ), globals())
                )
            )

        # Await execute funcs.
        for k, t in zip(k_list, t_list):
            task_dict[k] = await t

        # delete useless temp files after all threads finished.
        for _, _, files in walk("_output"):
            for file in files:
                if file.endswith("png"):
                    remove("_output/%s"%file)
        
        return task_dict