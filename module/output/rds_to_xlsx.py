# -*- coding: utf-8 -*-

from util.redis import RedisController
from util.xlsx.writer import write_xlsx
import json

class RdsToXlsx():

    @staticmethod
    def save(rds, file_name, sheet_name):
        with write_xlsx(file_name, sheet_name) as x:
            for data in rds.rscan:
                x.write_dict(json.loads(data[1]))