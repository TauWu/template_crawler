# -*- coding: utf-8 -*-
# Reporter: Send data email to recver.

from module.mail.mail import Sender
from module.database.db_opter import DBController
from module.config.reporter import RPTerConfigReader
from util.xlsx.writer import write_xlsx
from util.common.date import Time

import os
import shutil

class Do():

    def __init__(self, rpt_name):
        self.rpt_name   = rpt_name
        self.rpt_conf   = RPTerConfigReader.rpter_config(rpt_name)
        self.sender     = Sender(
            msg     = "%s\n数据采样时间：%s"%(self.rpt_conf['recv']['recv_msg'], Time.now_date_str()),
            subject = "%s => %s"%(self.rpt_conf['recv']['recv_sub'], Time.now_date_str()),
            recvers = self.rpt_conf['recv']['recv_mail']
        )
        self.db         = DBController(rpt_name)

    def do(self):
        lj_path = self.data_from_db_lj
        qk_path = self.data_from_db_qk
        dk_path = self.data_from_db_dk
        zr_path = self.data_from_db_zr

        self.sender.add_attachment(*lj_path)
        self.sender.add_attachment(*qk_path)
        self.sender.add_attachment(*dk_path)
        self.sender.add_attachment(*zr_path)

        self.sender.send()


    def __data_from_db__(self, SQL, filename, sheetname, orderlist):
        RPT_PATH = "./_output/{rpt}".format(
            rpt = self.rpt_name
        )
        XLSX_PATH = "{rpt}/{date}".format(
            rpt = RPT_PATH,
            date = Time.now_date_str()
        )

        if not os.path.exists(RPT_PATH):
            os.mkdir(RPT_PATH)

        path = "{xlsx}/{filename}.xlsx".format(
            xlsx        = XLSX_PATH,
            filename    = sheetname
        )

        if os.path.exists(path):
            os.remove(path)

        self.db.execute(SQL)
        data = self.db.cur.fetchall()
        
        with write_xlsx(path, sheetname) as x:
            for d in data:
                x.write_dict(d, orderlist=orderlist)
        return filename, path

    @property
    def data_from_db_lj(self):
        '''data_from_db_lj
        Get Lianjia house info data from database.
        '''
        SQL = """
            select
                h.house_id as '房源编号', h.community_id as '小区编号',
                h.house_type_new as '房型', h.house_area as '房屋面积',
                h.house_price as '租金', c.community_name as '小区名称',
                c.bd_district as '行政区', c.bd_busi as '商圈', 
                c.bd_detail as '详细地址'
            from
                house_base_infolj h
            inner join community_info c on 
                h.community_id = c.community_id and c.source_from = 1 and h.enabled = 1 
                and c.enabled = 1 and c.community_id <> '' and c.lat <> '' and c.lng <> '' 
        """
        sheetname   = '链家信息采集'
        filename    = 'LianjiaHouseInfo.xlsx'
        orderlist = [
            '房源编号', '小区编号', '房型', '房屋面积', '租金', '小区名称', '行政区', '商圈', '详细地址'
        ]
        return self.__data_from_db__(SQL, filename, sheetname, orderlist)


    @property
    def data_from_db_qk(self):
        '''data_from_db_qk
        Get Qingke house info data from database.
        '''
        SQL = """
            select
                h.house_id as '房源编号', h.community_id as '小区编号', '' as '房型',
                h.area as '房屋面积', h.price as '租金', c.community_name as '小区名称',
                c.bd_district as '行政区', c.bd_busi as '商圈', c.bd_detail as '详细地址'
            from
                house_base_infoqk h
            inner join community_info c on 
                h.community_id = c.community_id and c.source_from = 3 and 
                h.enabled = 1 
                and c.enabled = 1 and c.community_id <> '' and c.lat <> '' and c.lng <> '' 
        """
        sheetname   = '青客信息采集'
        filename    = 'QingkeHouseInfo.xlsx'
        orderlist = [
            '房源编号', '小区编号', '房型', '房屋面积', '租金', '小区名称', '行政区', '商圈', '详细地址'
        ]
        return self.__data_from_db__(SQL, filename, sheetname, orderlist)

    @property
    def data_from_db_dk(self):
        '''data_from_db_dk
        Get Danke house info data from database.
        '''
        SQL = """
            select
                h.house_id as '房源编号', h.community_id as '小区编号',
                h.house_type as '房型', h.area as '房屋面积',
                h.price as '租金', c.community_name as '小区名称',
                c.bd_district as '行政区', c.bd_busi as '商圈', 
                c.bd_detail as '详细地址'
            from
                house_base_infodk h
            inner join community_info c on 
                h.community_id = c.community_id and c.source_from = 4 and h.enabled = 1 
                and c.enabled = 1 and c.community_id <> '' and c.lat <> '' and c.lng <> '' 
        """
        sheetname   = '蛋壳信息采集'
        filename    = 'DankeHouseInfo.xlsx'
        orderlist = [
            '房源编号', '小区编号', '房型', '房屋面积', '租金', '小区名称', '行政区', '商圈', '详细地址'
        ]
        return self.__data_from_db__(SQL, filename, sheetname, orderlist)

    @property
    def data_from_db_zr(self):
        '''data_from_db_zr
        Get Ziroom house info data from database.
        '''
        SQL = """
            select
                h.house_id as '房源编号', h.community_id as '小区编号', h.house_type as '房型',
                h.area as '房屋面积', h.price as '租金', c.community_name as '小区名称', 
                c.bd_district as '行政区', c.bd_busi as '商圈', c.bd_detail as '详细地址'
            from
                house_base_infozr h
            inner join community_info c on 
                h.community_id = c.community_id and c.source_from = 2 and h.enabled = 1 
                and c.enabled = 1 and c.community_id <> '' and c.lat <> '' and c.lng <> ''
                and h.house_id <> ''
        """
        sheetname   = '自如信息采集'
        filename    = 'ZiroomHouseInfo.xlsx'
        orderlist = [
            '房源编号', '小区编号', '房型', '房屋面积', '租金', '小区名称', '行政区', '商圈', '详细地址'
        ]
        return self.__data_from_db__(SQL, filename, sheetname, orderlist)