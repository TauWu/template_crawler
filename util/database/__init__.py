# -*- coding: utf-8 -*-

from constant.config import MYSQL_CFG

class DBController():
    """
    数据库操作模块
    
    可访问成员（函数）：
    - cur
    - IntegrityError
    - execute(sql)
    - close

    """

    def __init__(self):
        import pymysql
        from pymysql.err import IntegrityError

        # 保护连接为私有成员
        try:
            self._conn = pymysql.connect(
                host=MYSQL_CFG["host"], port=int(MYSQL_CFG["port"]), 
                user=MYSQL_CFG["user"], passwd=MYSQL_CFG["passwd"],
                db=MYSQL_CFG["db"], charset='utf8'
            )
        except Exception:
            print("数据库连接创建失败！[{user}:{passwd}@{host}:{port}?charset=utf-8/{db}]".format_map(MYSQL_CFG))
        self.cur = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.IntegrityError = IntegrityError
        print("数据库连接创建成功！[{user}:{passwd}@{host}:{port}?charset=utf-8/{db}]".format_map(MYSQL_CFG))

    def execute(self, SQL):
        # 执行一条SQL语句
        self.cur.execute(SQL)
        self._conn.commit()

    @property
    def close(self):
        # 关闭数据库连接
        self._conn.close()
        self.cur.close()
        print("数据库连接断开成功！")