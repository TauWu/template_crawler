# Parser.list
# Parse list info

from util.common.tools import finder

class ParserList(object):

    def __init__(self, list_res_iter, crawler_conf, rds, rds_key):
        self.list_res_iter   = list_res_iter
        self.crawler_conf    = crawler_conf
        self.rds             = rds
        self.rds_key         = rds_key

    @property
    def save(self):
        parser = self.crawler_conf["list_parser"]
        find_data = parser["data_path"].split('.')
        parser.pop('data_path')

        for result in self.list_res_iter:
            data_list = finder(result, find_data)
            for data in data_list:
                rtn_data = dict()
                for k, v in zip(parser.keys(), parser.values()):
                    rtn_data[k] = data[v]
                if len(self.rds_key.split('.')) > 1:
                    self.rds.__update_dict_to_redis__(".".join([rtn_data[k] for k in self.rds_key.split('.')]), rtn_data)
                else:
                    self.rds.__update_dict_to_redis__(rtn_data[self.rds_key], rtn_data)
