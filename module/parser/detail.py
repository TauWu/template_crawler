# Parser Detail
# Parse detail page
import json, re
from lxml import etree
from util.common.tools import finder

class ParserDetail(object):

    def __init__(self, detail_res_iter, crawler_conf, rds):
        self.detail_res_iter = detail_res_iter
        self.crawler_conf    = crawler_conf
        self.rds             = rds
        self.compiles        = crawler_conf['compiles']

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
                with open("test1.html", "w") as f:
                    f.write(res.decode('utf-8'))
                xml_data = etree.HTML(res)
                for k, v in zip(parser.keys(), parser.values()):
                    try:
                        if k in self.compiles.keys():
                            # print("*****", etree.tostring(xml_data.xpath(v)[0]).decode('utf-8'))
                            rtn_data[k] = re.findall(self.compiles[k], etree.tostring(xml_data.xpath(v)[0]).decode('utf-8'))[0]
                        else:
                            rtn_data[k] = xml_data.xpath(v)[0].xpath('./text()')[0].strip()
                    except Exception as e:
                        print("Err: {}".format(e))
                self.rds.__update_dict_to_redis__(".".join(idxx), rtn_data)
                
            else:
                print("****", parser)
                find_data = parser["data_path"].split('.')            
                parser.pop('data_path')        
                res = json.loads(res.decode('utf-8'))
                try:
                    data = finder(res, find_data)
                    for k, v in zip(parser.keys(), parser.values()):
                        rtn_data[k] = data[v]
                    self.rds.__update_dict_to_redis__('.'.join(idxx), rtn_data)
                except Exception as e:
                    print("??????{} {}".format(e, res))
                finally:
                    parser['data_path'] = '.'.join(find_data)
