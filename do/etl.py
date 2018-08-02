# -*- coding: utf-8 -*-
# ETL project main function
from module.config.etl import ETLConfigReader
from module.redis.scan import RedisScanner
from constant.config import BD_MAP_CFG

import json
import re

class Do(object):

    def __init__(self, etl_name):
        self.etl_name       = etl_name
        self.etl_conf       = ETLConfigReader.etl_config(etl_name)
        self.rds_data_iter  = RedisScanner.rds_data_iter(self.etl_conf["sys_conf"]["redis_db"])
        self.community_dict = dict()

    def do(self):
        print(self.etl_conf)

        if self.etl_name == "lianjia":
            self.etl_lianjia()
        elif self.etl_name == "ziroom":
            self.etl_ziroom()
        elif self.etl_name == "qk":
            self.etl_qk()

##################################################

    def etl_lianjia(self):
        e_data = self.__e_lianjia__()
        t_data = self.__t__lianjia__(e_data)
        _      = self.__l__lianjia__(t_data)

    def __e_lianjia__(self):
        for data in self.rds_data_iter:
            data = data[1]
            yield json.loads(data)

    def __t__lianjia__(self, e_data):
        '''__t_lianjia__
        Lianjia ETL project Transformer.
        '''
        # Load data from redis to transformer.
        t_dict = dict(
            house_id        = "house_id",
            community_id    = "comm_id",
            community_name  = "comm_name",
            lat             = "lat_lng",
            lng             = "lat_lng",
            cw_district     = "district",
            cw_busi         = "busiarea",
            house_type_new  = "house_type",
            orientation     = "orientation",
            house_price     = "price_dtl",
            house_floor     = "floor",
            area            = "area"
        )

        # Clean data by lamdba functions.
        t_clean_dict = dict (
            lat             = lambda ll, data: ll.split(',')[1],
            lng             = lambda ll, data: ll.split(',')[0],
            house_price     = lambda p, data: int(clean_price(p, data)),
            house_floor     = lambda f, data: ",".join(re.findall("(.+)楼层 \(共([0-9]+)层\)", f)[0]),
            area            = lambda a, data: int(re.findall("([0-9]+)", a)[0])
        )

        def clean_price(p, data):
            if p is not None:
                return p
            return data["price"]
        
        for data in e_data:
            data_dict = dict()

            for t in t_dict.items():
                try:
                    data_dict[t[0]] = data[t[1]]
                except Exception:
                    data_dict[t[0]] = None

            for t in t_clean_dict.items():
                try:
                    data_dict[t[0]] = t[1](data_dict[t[0]], data)
                except Exception:
                    pass
            
            data_dict = dict(self.__bd_map__(
                data_dict["community_id"], data_dict["lat"], data_dict["lng"]
                ), **data_dict
            )

            data_dict["source_from"] = 1
            data_dict["source_name"] = "链家"

            yield data_dict

    def __l__lianjia__(self, t_data):
        for data in t_data:
            print(data, "\n")

##################################################

    def etl_ziroom(self):
        pass

    def __e_ziroom__(self):
        pass

    def __t__ziroom__(self):
        pass

    def __l__ziroom__(self):
        pass

##################################################

    def etl_qk(self):
        pass

    @property
    def __e_qk__(self):
        pass

    @property
    def __t__qk__(self):
        pass

    @property
    def __l__qk__(self):
        pass

##################################################

    def __bd_map__(self, community_id, lat, lng):
        from requests import get

        def get_k_tree(data, k):
            k = k.split('.')
            for key in k:
                data = data[key]
            return data
        
        try:
            return self.community_dict[community_id]
        except Exception:
            url_tpl = "http://api.map.baidu.com/geocoder/v2/?location={lat},{lng}&output=json&pois=1&ak={ak}"
            url = url_tpl.format(lat=lat, lng=lng, ak=BD_MAP_CFG["ak"])
            bd_kv = dict(
                bd_province = "addressComponent.province",
                bd_city     = "addressComponent.city",
                bd_district = "addressComponent.district",
                bd_busi     = "business",
                bd_street   = "addressComponent.street",
                bd_detail   = "formatted_address",
                bd_adcode   = "addressComponent.adcode"
            )

            bd_data = json.loads(get(url).content.decode('utf-8'))
            bd_data_dict = dict()

            if bd_data["status"] == 0:
                bd_data = bd_data["result"]
                for kv in bd_kv.items():
                    bd_data_dict[kv[0]] = get_k_tree(bd_data, kv[1])
            
            self.community_dict[community_id] = bd_data_dict
            return bd_data_dict