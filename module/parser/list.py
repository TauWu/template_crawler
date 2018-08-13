# Parser.list
# Parse list info

from util.common.tools import finder
from util.common.logger import LogBase
import lxml

class ParserList(LogBase):

    def __init__(self, project_name, list_res_iter, crawler_conf, rds, rds_key):
        LogBase.__init__(self, project_name, "ParserList")
        self.project_name    = project_name
        self.list_res_iter   = list_res_iter
        self.crawler_conf    = crawler_conf
        self.rds             = rds
        self.rds_key         = rds_key

    @property
    def save(self):
        from lxml import etree
        import re

        parser      = self.crawler_conf["list_parser"]
        crawler     = self.crawler_conf["list_crawler"]
        compiles    = self.crawler_conf['compiles']
        
        if crawler['method'] == '1' or crawler['method'] == '3':
            find_data = parser["data_path"].split('.')
            parser.pop('data_path')

            for result in self.list_res_iter:
                try:
                    data_list = finder(result, find_data)
                    for data in data_list:
                        rtn_data = dict()
                        for k, v in zip(parser.keys(), parser.values()):
                            rtn_data[k] = data[v]
                        self.__update_redis__(rtn_data)
                except Exception as e:
                    self.err("Parser by json failed", err=e)
                    
        else:
            for result in self.list_res_iter:
                rtn_datas = list()

                with open("test.html", "w") as f:
                    f.write(etree.tostring(result).decode('utf-8'))
                
                for k, v in parser.items():
                    rtn_data_list   = list()
   
                    for data in result.xpath(v):
                        rtn_data = dict()

                        try:
                            if k in compiles.keys():
                                rtn_data[k] = re.findall(compiles[k], etree.tostring(data).decode('utf-8'))[0]
                            else:
                                rtn_data[k] = data.xpath('./text()')[0].replace('\xa0\xa0', '')
                        except Exception as e:
                            self.error("Parser by lxml failed.", key=k, err=e)

                        rtn_data_list.append(rtn_data)

                    rtn_datas.append(rtn_data_list)
                
                for rtn in zip(*rtn_datas):
                    for items in rtn:
                        rtn_data = dict(rtn_data, **items)

                    if len(rtn_data.items()) > 0:
                        self.__update_redis__(rtn_data)

    
    def __update_redis__(self, rtn_data):
        if len(self.rds_key.split('.')) > 1:
            self.rds.__update_dict_to_redis__(".".join([str(rtn_data[k]) for k in self.rds_key.split('.')]), rtn_data)
        else:
            self.rds.__update_dict_to_redis__(rtn_data[self.rds_key], rtn_data)

                
