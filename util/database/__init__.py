# -*- coding: utf-8 -*-

from constant.config import MYSQL_CFG
from util.common.logger import LogBase

import pymysql

from pymysql.err import IntegrityError

class DBController(LogBase):
    """DBController
    
    Available properties or functions：
    - cur
    - IntegrityError
    - execute(sql)
    - close

    """

    def __init__(self, project_name="sample_project"):
        # Register Log service.
        logger_name = "database"
        LogBase.__init__(self, project_name, logger_name)

        # try to connect to database.
        try:
            self._conn = pymysql.connect(
                host=MYSQL_CFG["host"], port=int(MYSQL_CFG["port"]), 
                user=MYSQL_CFG["user"], passwd=MYSQL_CFG["passwd"],
                db=MYSQL_CFG["db"],     charset='utf8'
            )
        except Exception:
            self.err("Connect to database FAILED.", **MYSQL_CFG)
            
        self.cur = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.IntegrityError = IntegrityError

        self.info("Connect to database SUCCEED.", **MYSQL_CFG)

    def execute(self, SQL):
        # Execute a SQL string and commit. It may be a tx.
        self.cur.execute(SQL)
        self._conn.commit()

    @property
    def close(self):
        # Close
        self._conn.close()
        self.cur.close()
        self.info("Close the connection to database succeed.")