# -*- coding: utf-8 -*-
# ETL project main function
from module.config.etl import ETLConfigReader
from module.redis.scan import RedisScanner
from module.database.db_opter import DBOpter
from constant.config import BD_MAP_CFG
from util.common.logger import LogBase
from module.mail.mail import Mail
from util.common.date import Time

import json
import re

class Do(LogBase):

    def __init__(self, etl_name):
        project_name            = "etl_%s"%etl_name
        self.project_name       = project_name
        LogBase.__init__(self, project_name, "main")

        self.etl_name           = etl_name
        self.etl_conf           = ETLConfigReader.etl_config(etl_name)
        self.rds_data_iter      = RedisScanner.rds_data_iter(self.etl_conf["sys_conf"]["redis_db"], project_name)
        self.community_tbname   = "community_info"
        self.community_tbkeys   = [
            'community_id', 'source_from', 'source_name', 'community_name',
            'lat', 'lng', 'cw_district', 'cw_busi', 'cw_detail', 'bd_province',
            'bd_city', 'bd_district', 'bd_busi', 'bd_street', 'bd_detail', 'bd_adcode'
        ]
        self.community_dict     = dict()
        self.db                 = DBOpter(project_name)
        

    def do(self):
        
        self.info("ETL Project start.")
        self.debug("Here is the conf.", **self.etl_conf["sys_conf"])
        p1s = Time.ISO_time_str()

        if self.etl_name == "lianjia":
            self.base_tbname = "house_base_infolj"
            self.base_tbkeys = [
                'house_id', 'community_id', 'orientation', 'house_area',
                'house_price', 'house_floor', 'house_type_new',
                'sale_date', 'sale_date_new', 'see_count', 'see_stat_total',
                'see_stat_weekly', 'house_title'
            ]

            self.etl_lianjia()

        elif self.etl_name == "ziroom":
            self.community_id_list  = list()
            self.base_tbname        = "house_base_infozr"
            self.base_tbkeys        = [
                'house_id', 'community_id', 'price', 'area',
                'house_type', 'floor', 'status', 'house_code'
            ]
            
            self.etl_ziroom()
        
        elif self.etl_name == "qk":
            self.base_tbname = "house_base_infoqk"
            self.base_tbkeys = [
                'house_id', 'community_id', 'orientation', 'floor', 'area',
                'origin_price', 'price'
            ]
            self.etl_qk()

        elif self.etl_name == "danke":
            self.community_id_list  = list()
            self.base_tbname = "house_base_infodk"
            self.base_tbkeys = [
                'house_id', 'area', 'house_type', 'house_code',
                'de_fee_1', 'de_fee_6', 'de_fee_12', 'ser_fee_1', 'ser_fee_6', 'ser_fee_12',
                'price', 'community_id', 'floor', 'orientation'
            ]
            self.etl_danke()

        msg = None
        sub = "Report for {} => {}".format(self.project_name, Time.ISO_date_str())
        
        p1e = Time.ISO_time_str()
        
        with open("./constant/etl_report.tpl") as r:
            msg = r.read()
        msg = msg.format(
            sub=sub, p1s=p1s, p1e=p1e        
        )

        attachment = {
            "{}.log".format(
                self.project_name
            ):"./log/{}/{}.log".format(
                self.project_name, Time.now_date_str()
            )
        }

        Mail.send(msg, sub, attachment)

    @property
    def __e_data_iter__(self):
        '''Extract Data iter.
        Get data from redis one by one.
        '''

        for data in self.rds_data_iter:

            if self.etl_name == "ziroom":
                house_id = data[0]
                house_data = json.loads(data[1])
                if 'house_id' not in house_data.keys():
                    self.warning("'house_id' not in house_data", house_id=house_id)
                    house_data = dict(house_data, **({"house_id":house_id}))
                yield house_data
            else:
                data = data[1]
                yield json.loads(data)

    def __transformer__(self, data, t_dict, t_clean_dict):
        '''__transformer__
        Transform Data by ordered methods.
        '''
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

        return data_dict

    def __bd_mapper__(self, data_dict):
        '''__bd_mapper__
        Add Bd Map info into data_dict.
        '''
        return dict(self.__bd_map__(
            data_dict["community_id"], data_dict["lat"], data_dict["lng"]
            ), **data_dict
        )
        
######################### ETL LIANJIA #########################

    def etl_lianjia(self):
        '''etl_lianjia
        ETL project for lianjia.
        '''

        e_data = self.__e_data_iter__
        t_data = self.__t_lianjia__(e_data)
        _      = self.__l_lianjia__(t_data)

    def __t_lianjia__(self, e_data):
        '''__t_lianjia__
        Lianjia ETL project Transformer.
        '''
        # Load data from redis to transformer.
        t_dict = dict(
            house_id        = "house_id",
            community_id    = "comm_id",
            community_name  = "comm_name",
            house_area      = "area",
            lat             = "lat_lng",
            lng             = "lat_lng",
            cw_district     = "district",
            cw_busi         = "busiarea",
            house_type_new  = "house_type",
            orientation     = "orientation",
            house_price     = "price_dtl",
            house_floor     = "floor",
            area            = "area",
            see_count       = "see",
            sale_date       = "sale_date",
            sale_date_new   = "sale_date_new",
            see_stat_total  = "see_tl",
            see_stat_weekly = "see_wk",
            house_title     = "title"
        )

        # Clean data by lamdba functions.
        t_clean_dict = dict (
            lat             = lambda ll, data: ll.split(',')[1],
            lng             = lambda ll, data: ll.split(',')[0],
            house_price     = lambda p,  data: int(clean_price(p, data)),
            house_floor     = lambda f,  data: ",".join(re.findall("(.+)楼层 \(共([0-9]+)层\)", f)[0]),
            area            = lambda a,  data: int(re.findall("([0-9]+)", a)[0]),
            see_count       = lambda c,  data: int(c),
            sale_date       = lambda sd, date: re.findall(r"([0-9.]+)", sd)[0],
            sale_date_new   = lambda sd, date: re.findall(r"([0-9]+)", sd)[0],
            house_area      = lambda a,  date: re.findall(r"([0-9]+)", a)[0],
        )

        def clean_price(p, data):
            '''clean_price'''
            return p if p is not None else data["price"]
        
        for data in e_data:
            data_dict = self.__transformer__(data, t_dict, t_clean_dict)
            
            data_dict["source_from"] = 1
            data_dict["source_name"] = "链家"

            data_dict = self.__bd_mapper__(data_dict)

            yield data_dict

    def __l_lianjia__(self, t_data):

        for data in t_data:
            self.db.update_data(self.community_tbname, data, self.community_tbkeys, community_id=data['community_id'])
            self.db.update_data(self.base_tbname, data, self.base_tbkeys, house_id=data['house_id'])


######################### ETL ZIROOM #########################

    def etl_ziroom(self):
        '''etl_ziroom
        ETL project for ziroom.
        '''

        e_data = self.__e_data_iter__
        t_data = self.__t_ziroom__(e_data)
        _      = self.__l_ziroom__(t_data)

    def __t_ziroom__(self, e_data):
        '''__t_ziroom__
        Ziroom transformer.
        '''

        self.db.execute(
            "select max(cast(community_id as unsigned integer)) as max from community_info where source_from = 2 and enabled = 1"
        )
        data = self.db.cur.fetchone()
        max_id = 0 if data["max"] is None else data["max"]
            
        self.info("The max_id in community table for ziroom =>", max=max_id)

        def get_community(data_dict):
            '''get_community
            Get new community id if it's not exists.
            '''

            try:

                self.db.execute(
                    "select community_id from community_info where source_from = 2 and lat = {lat} and lng = {lng} and enabled = 1".format(
                        lat=data_dict['lat'], lng=data_dict['lng']
                    )
                )

                data = self.db.cur.fetchone()
                community_id = data["community_id"]
                self.debug("Find community_id for ziroom in table SECCEED.",community_id=community_id, lat=data_dict['lat'], lng=data_dict['lng'])

            except Exception:
                self.warning("No community_id for ziroom in table equals this lat and lng.", lat=data_dict['lat'], lng=data_dict['lng'])

                try:

                    posi = ",".join([data_dict['lat'], data_dict['lng']])
                    if posi not in self.community_id_list:
                        self.community_id_list.append(posi)    
                    community_id = max_id + 1 + self.community_id_list.index(posi)
                    
                except Exception as e:
                    self.warn("No lat or lng is supported.", err=e)
                    return data_dict
            
            data_dict["community_id"] = community_id
            self.debug("Get community_id for ziroom house info.", community_id=community_id, lat=data_dict['lat'], lng=data_dict['lng'])
            return data_dict

        # Load data from redis to transformer.
        t_dict = dict(
            house_id        = "house_id",
            community_id    = "",
            community_name  = "comm_name",
            lat             = "lat",
            lng             = "lng",
            cw_district     = "",
            cw_busi         = "busiarea",
            house_type      = "house_type",
            orientation     = "orientation",
            price           = "price",
            floor           = "floor",
            area            = "area",
            status          = 'status',
            house_code      = "house_code",
            
            paymentlist     = "paymentlist"
        )

        # Clean data by lamdba functions.
        t_clean_dict = dict (
            floor       = lambda f, data: ",".join([str(int(i)) for i in re.findall(r"楼层：(.+)层", f)[0].split('/')]),
            area        = lambda a, data: float(re.findall("([0-9.]+)", a)[0]),
            cw_busi     = lambda b, data: re.findall("(.+)公寓出租", b)[0],
            orientation = lambda o, data: re.findall(r"朝向：(.+)", o)[0],
            house_type  = lambda t, data: re.findall(r'户型：(.+)', t)[0],
            community_name=lambda c, data: c.replace('租房信息','')
            
        )

        for data in e_data:
            
            data_dict = self.__transformer__(data, t_dict, t_clean_dict)

            data_dict["source_from"] = 2
            data_dict["source_name"] = "自如"

            data_dict = get_community(data_dict)
            
            if "community_id" not in data_dict.keys():
                continue

            data_dict = self.__bd_mapper__(data_dict)

            yield data_dict

    def __l_ziroom__(self, t_data):
        for data in t_data:
            if data['community_id'] is not None:
                self.db.update_data(self.community_tbname, data, self.community_tbkeys, source_from=data["source_from"], lat=data['lat'], lng=data['lng'])
                self.db.update_data(self.base_tbname, data, self.base_tbkeys, house_id=data['house_id'])
                self.db.update_data_list("house_price_infozr", data, use=["house_id", "paymentlist"], sql_key=["house_id", "period"])

######################### ETL QINGKE #########################

    def etl_qk(self):
        '''etl_qk
        ETL project for qk.
        '''

        e_data = self.__e_data_iter__
        t_data = self.__t_qk__(e_data)
        _      = self.__l_qk__(t_data)
            
    def __t_qk__(self, e_data):
        '''__t_qk__
        QK transformer.
        '''

        # Turn &#xxxx; to char.
        def hex_to_str(hex_match):
            hex_data = re.findall(r"[0-9A-Z]+", hex_match.group())[0]
            return chr(int(hex_data, 16))

        def html_to_str(html):
            cpl = re.compile(r"&#x[0-9A-Z]+;")
            html = re.sub(cpl, hex_to_str, html)
            return html
            
        t_dict = dict(
            origin_price    = "origin_price",
            house_id        = "house_id",
            community_id    = "comm_id",
            community_name  = "comm_name",
            lat             = "latitude",
            lng             = "longitude",
            cw_district     = "district",
            cw_busi         = "busi_name",
            cw_detail       = "",
            house_type      = "",
            orientation     = "orientation",
            price           = "price",
            floor           = "floor",
            area            = "area"        
        )

        # Clean data by lamdba functions.
        t_clean_dict = dict (
            floor           = lambda f, data: ",".join(re.findall(r"楼层：(.+)", f)[0].split('/')),
            area            = lambda a, data: int(re.findall("([0-9.]+)", a)[0]),
            orientation     = lambda o, data: re.findall(r"朝向：朝(.+)", o)[0],
            origin_price    = lambda p, data: re.findall(r"租金：([0-9.]+)元/月", p)[0],
            cw_busi         = lambda b, data: html_to_str(b),
            community_name  = lambda c, data: html_to_str(c)
        )

        for data in e_data:
            
            data_dict = self.__transformer__(data, t_dict, t_clean_dict)

            data_dict["source_from"] = 3
            data_dict["source_name"] = "青客"

            data_dict = self.__bd_mapper__(data_dict)

            yield data_dict

    def __l_qk__(self, t_data):

        for data in t_data:
            self.db.update_data(self.community_tbname, data, self.community_tbkeys, community_id=data['community_id'])
            self.db.update_data(self.base_tbname, data, self.base_tbkeys, house_id=data['house_id'])


######################### ETL DANKE #########################

    def etl_danke(self):
        '''etl_danke
        ETL project for danke.
        '''

        e_data = self.__e_data_iter__
        t_data = self.__t_danke__(e_data)
        _      = self.__l_danke__(t_data)
            
    def __t_danke__(self, e_data):
        '''__t_danke__
        DanKe transformer.
        '''
        
        self.db.execute(
            "select max(cast(community_id as unsigned integer)) as max from community_info where source_from = 4 and enabled = 1"
        )
        data = self.db.cur.fetchone()
        max_id = 0 if data["max"] is None else data["max"]
            
        self.info("The max_id in community table for danke =>", max=max_id)

        def get_community(data_dict):
            '''get_community
            Get new community id if it's not exists.
            '''

            try:

                self.db.execute(
                    "select community_id from community_info where source_from = 4 and lat = {lat} and lng = {lng} and enabled = 1".format(
                        lat=data_dict['lat'], lng=data_dict['lng']
                    )
                )

                data = self.db.cur.fetchone()
                community_id = data["community_id"]
                self.debug("Find community_id for danke in table SECCEED.",community_id=community_id, lat=data_dict['lat'], lng=data_dict['lng'])

            except Exception:
                self.warning("No community_id for danke in table equals this lat and lng.", lat=data_dict['lat'], lng=data_dict['lng'])

                try:

                    posi = ",".join([data_dict['lat'], data_dict['lng']])
                    if posi not in self.community_id_list:
                        self.community_id_list.append(posi)    
                    community_id = max_id + 1 + self.community_id_list.index(posi)
                    
                except Exception as e:
                    self.warn("No lat or lng is supported.", err=e)
                    return data_dict
            
            data_dict["community_id"] = community_id
            self.debug("Get community_id for danke house info.", community_id=community_id, lat=data_dict['lat'], lng=data_dict['lng'])
            return data_dict

        # Turn &#xxxx; to char.
        def hex_to_str(hex_match):
            hex_data = re.findall(r"[0-9A-Z]+", hex_match.group())[0]
            return chr(int(hex_data, 16))

        def html_to_str(html):
            cpl = re.compile(r"&#x[0-9A-Z]+;")
            html = re.sub(cpl, hex_to_str, html)
            return html

        # Turn &#88888; to char.
        def dec_to_str(dec_match):
            # print("*****", dec_match)
            dec_data = re.findall(r'[0-9]+', dec_match.group())[0]
            return chr(int(dec_data))

        def html_to_str_dec(html):
            cpl = re.compile(r"&#[0-9]+;")
            html = re.sub(cpl, dec_to_str, html)
            return html
            
        t_dict = dict(
            house_id        = "house_id",
            community_id    = "",
            community_name  = "comm_name",
            lat             = "lat",
            lng             = "lng",
            cw_district     = "district",
            cw_busi         = "busi_name",
            cw_detail       = "",
            house_type      = "house_type",
            orientation     = "orientation",
            price           = "price",
            floor           = "floor",
            area            = "area",
            house_code      = "house_code",
            ser_fee_12      = "ser_fee_12",
            ser_fee_6       = "ser_fee_6",
            ser_fee_1       = "ser_fee_1",
            de_fee_12       = "de_fee_12",
            de_fee_6        = "de_fee_6",
            de_fee_1        = "de_fee_1"
        )

        # Clean data by lamdba functions.
        t_clean_dict = dict (
            floor           = lambda f, data: ",".join((re.findall(r"楼层：(.+)层", f)[0]).split('/')),
            area            = lambda a, data: int(re.findall("([0-9.]+)", a)[0]),
            orientation     = lambda o, data: re.findall(r"朝向：(.+)", o)[0],
            cw_busi         = lambda b, data: html_to_str_dec(b),
            community_name  = lambda c, data: html_to_str(c),
            house_type      = lambda t, data: re.findall(r'户型：(.+)', t)[0],
            house_code      = lambda c, data: re.findall(r'编号：(.+)', c)[0],
            ser_fee_12      = lambda f, data: re.findall(r'([0-9]+)', f)[0],
            ser_fee_6       = lambda f, data: re.findall(r'([0-9]+)', f)[0],
            ser_fee_1       = lambda f, data: re.findall(r'([0-9]+)', f)[0],
            de_fee_12       = lambda f, data: re.findall(r'([0-9]+)', f)[0],
            de_fee_6        = lambda f, data: re.findall(r'([0-9]+)', f)[0],
            de_fee_1        = lambda f, data: re.findall(r'([0-9]+)', f)[0]
        )

        for data in e_data:
            
            data_dict = self.__transformer__(data, t_dict, t_clean_dict)

            data_dict["source_from"] = 4
            data_dict["source_name"] = "蛋壳"

            data_dict = get_community(data_dict)
            data_dict = self.__bd_mapper__(data_dict)

            yield data_dict

    def __l_danke__(self, t_data):
        # from pprint import pprint
        self.db.reInitializeTableData(self.base_tbname)
        for data in t_data:
            if data['community_id'] is not None:
                self.db.update_data(self.community_tbname, data, self.community_tbkeys, source_from=data["source_from"], lat=data['lat'], lng=data['lng'])
                self.db.update_data(self.base_tbname, data, self.base_tbkeys, house_id=data['house_id'])

######################### BAIDU MAP #########################

    def __bd_map__(self, community_id, lat, lng):
        from requests import get
        
        def get_k_tree(data, k):
            k = k.split('.')
            for key in k:
                data = data[key]
            return data

        if lat is None or lng is None:
            self.warn("No lat or lng to request BD MAP.", community_id=community_id, lat=lat, lng=lng)
            return dict()
        
        if community_id in self.community_dict.keys():
            self.debug("Get BD Map info from hash map.", community_id=community_id, lat=lat, lng=lng)
            return self.community_dict[community_id]
            
        else:
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
            else:
                self.err("Get BD Map info FAILED.", lat=lat, lng=lng, rtn=bd_data)
            
            self.debug("Get BD Map info SUCCEED.", lat=lat, lng=lng, **bd_data_dict)

            self.community_dict[community_id] = bd_data_dict
            return bd_data_dict
