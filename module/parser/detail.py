# Parser Detail
# Parse detail page
import json
from lxml import etree
from util.common.tools import finder

class ParserDetail(object):

    def __init__(self, detail_res_iter, crawler_conf, rds):
        self.detail_res_iter = detail_res_iter
        self.crawler_conf    = crawler_conf
        self.rds             = rds

    @property
    def save(self):
        '''save
        Save parsed data into redis.
        '''
        
        for res, task, idxx in self.detail_res_iter:
            crawler = self.crawler_conf['detail_crawlers'][task-1]
            parser = self.crawler_conf['detail_parsers'][task-1]
            
            rtn_data = dict()
            if int(crawler['method']) == 2:
                xml_data = etree.HTML(res)
                for k, v in zip(parser.keys(), parser.values()):
                    rtn_data[k] = xml_data.xpath(v)[0].xpath('./text()')[0].strip()
                self.rds.__update_dict_to_redis__(".".join(idxx), rtn_data)
                
            else:
                find_data = parser["data_path"].split('.')            
                parser.pop('data_path')        
                res = json.loads(res.decode('utf-8'))
                data = finder(res, find_data)
                for k, v in zip(parser.keys(), parser.values()):
                    rtn_data[k] = data[v]
                self.rds.__update_dict_to_redis__('.'.join(idxx), rtn_data)
                parser['data_path'] = '.'.join(find_data)