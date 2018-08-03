# Parser Detail
# Parse detail page
import json, re
from lxml import etree
from util.common.tools import finder
import module.parser.extra as extra

class ParserDetail(object):

    def __init__(self, crawler_name, detail_res_iter, crawler_conf, rds):
        self.detail_res_iter = detail_res_iter
        self.crawler_conf    = crawler_conf
        self.crawler_name    = crawler_name
        self.rds             = rds
        self.compiles        = crawler_conf['compiles']

    @property
    def save(self):
        '''save
        Save parsed data into redis.
        '''
        from xml.sax.saxutils import unescape

        for res, rds_kv, idx in self.detail_res_iter:

            # print(self.crawler_conf["detail_crawlers"], idx)

            crawler     = self.crawler_conf['detail_crawlers'][idx]
            parser      = self.crawler_conf['detail_parsers'][idx]
            
            rtn_data = dict()
            
            if int(crawler['method']) == 2:
                with open("test1.html", "w") as f:
                    f.write(res.decode('utf-8'))
                xml_data = etree.HTML(res)
                for k, v in zip(parser.keys(), parser.values()):
                    try:
                        if k in self.compiles.keys():
                            rtn_data[k] = re.findall(self.compiles[k], etree.tostring(xml_data.xpath(v)[0]).decode('utf-8'))[0]
                        else:
                            rtn_data[k] = xml_data.xpath(v)[0].xpath('./text()')[0].strip()
                    except Exception as e:
                        print("Err: {}".format(e))
                self.rds.__update_dict_to_redis__(".".join([rds_kv[k] for k in self.crawler_conf['sys_conf']['redis_key'].split('.')]), rtn_data)
                
            else:
                find_data = parser["data_path"].split('.')            
                parser.pop('data_path')        
                res = json.loads(res.decode('utf-8'))
                try:
                    data = finder(res, find_data)
                    for k, v in zip(parser.keys(), parser.values()):
                        rtn_data[k] = data[v]
                    try:
                        rtn_data = eval("extra.{}_extra({})".format(self.crawler_name, rtn_data))
                    except Exception:
                        pass
                    self.rds.__update_dict_to_redis__(".".join([rds_kv[k] for k in self.crawler_conf['sys_conf']['redis_key'].split('.')]), rtn_data)
                except Exception as e:
                    print("Parse Detail Error! Err:{} Result:{}".format(e, res))
                finally:
                    parser['data_path'] = '.'.join(find_data)
