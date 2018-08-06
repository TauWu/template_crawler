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
            self.community_id_list = list()
            self.etl_ziroom()
        elif self.etl_name == "qk":
            self.etl_qk()

######################### ETL LIANJIA #########################

    def etl_lianjia(self):
        e_data = self.__e_lianjia__()
        t_data = self.__t_lianjia__(e_data)
        _      = self.__l_lianjia__(t_data)

    def __e_lianjia__(self):
        for data in self.rds_data_iter:
            data = data[1]
            yield json.loads(data)

    def __t_lianjia__(self, e_data):
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

    def __l_lianjia__(self, t_data):

        for data in t_data:
            print(data, "\n")

######################### ETL ZIROOM #########################

    def etl_ziroom(self):
        e_data = self.__e_ziroom__()
        t_data = self.__t_ziroom__(e_data)
        _      = self.__l_ziroom__(t_data)

    def __e_ziroom__(self):
        for data in self.rds_data_iter:
            data = data[1]
            yield json.loads(data)

    def __t_ziroom__(self, e_data):
        # Load data from redis to transformer.
        t_dict = dict(
            house_id        = "house_id",
            community_id    = "comm_id",
            community_name  = "",
            lat             = "lat",
            lng             = "lng",
            cw_district     = "",
            cw_busi         = "busiarea",
            house_type      = "house_type",
            orientation     = "orientation",
            price           = "price",
            floor           = "floor",
            area            = "area",

            paymentlist     = "paymentlist"
        )

        # Clean data by lamdba functions.
        t_clean_dict = dict (
            floor       = lambda f, data: ",".join(re.findall(r"楼层：(.+)层", f)[0].split('/')),
            area        = lambda a, data: int(re.findall("([0-9.]+)", a)[0]),
            cw_busi     = lambda b, data: re.findall("(.+)公寓出租", b)[0],
            orientation = lambda o, data: re.findall(r"朝向：(.+)", o)[0]
        )

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

            data_dict["source_from"] = 2
            data_dict["source_name"] = "自如"

            posi = ",".join([data_dict['lat'], data_dict['lng']])
            if posi not in self.community_id_list:
                self.community_id_list.append(posi)
                
            data_dict["community_id"] = self.community_id_list.index(posi)

            data_dict = dict(self.__bd_map__(
                data_dict["community_id"], data_dict["lat"], data_dict["lng"]
                ), **data_dict
            )

            yield data_dict

    def __l_ziroom__(self, t_data):
        for data in t_data:
            print("{}\n".format(data))

######################### ETL QINGKE #########################

    def etl_qk(self):
        e_data = self.__e_qk__()
        t_data = self.__t_qk__(e_data)
        _      = self.__l_qk__(t_data)

    def __e_qk__(self):
        for data in self.rds_data_iter:
            data = data[1]
            yield json.loads(data)
            
    def __t_qk__(self, e_data):
        t_dict = dict(
            house_id        = "house_id",
            community_id    = "comm_id",
            community_name  = "comm_name",
            lat             = "latitude",
            lng             = "longitude",
            cw_district     = "district",
            cw_busi         = "busi_name",
            house_type      = "",
            orientation     = "orientation",
            price           = "price",
            floor           = "floor",
            area            = "area"        
        )

        def hex_to_str(hex_match):
            hex_data = re.findall(r"[0-9A-Z]+", hex_match.group())[0]
            return chr(int(hex_data, 16))

        def html_to_str(html):
            cpl = re.compile(r"&#x[0-9A-Z]+;")
            html = re.sub(cpl, hex_to_str, html)
            return html

        # Clean data by lamdba functions.
        t_clean_dict = dict (
            floor           = lambda f, data: ",".join(re.findall(r"楼层：(.+)", f)[0].split('/')),
            area            = lambda a, data: int(re.findall("([0-9.]+)", a)[0]),
            orientation     = lambda o, data: re.findall(r"朝向：朝(.+)", o)[0],
            cw_busi         = lambda b, data: html_to_str(b),
            community_name  = lambda c, data: html_to_str(c)
        )

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

            data_dict["source_from"] = 3
            data_dict["source_name"] = "青客"

            data_dict = dict(self.__bd_map__(
                data_dict["community_id"], data_dict["lat"], data_dict["lng"]
                ), **data_dict
            )

            yield data_dict

    def __l_qk__(self, t_data):
        from pprint import pprint

        for data in t_data:
            pprint(data)
            a = input("DEBUG")

######################### BAIDU MAP #########################


    def __bd_map__(self, community_id, lat, lng):
        from requests import get
        
        def get_k_tree(data, k):
            k = k.split('.')
            for key in k:
                data = data[key]
            return data

        if lat is None or lng is None:
            return dict()
        
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