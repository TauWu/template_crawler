# -*- coding: utf-8 -*-
# Database operator
from util.database import DBController

NO_DATA         = 0
DATA_CHANGE     = 1
DATA_EQUAL      = 2

class DBOpter(object):

    def __init__(self):
        self.db = DBController()

    def update_data(self, tb_name, data, use, **kwargs):
        data_status = self.sql_is_equal(tb_name, data, use, **kwargs)
        sql = self.sql_maker_insert(tb_name, data, use=use)

        if data_status == NO_DATA:
            print("NO_DATA insert.")
            print(sql)
            try:
                self.db.execute(sql)
            except Exception:
                self.db._conn.rollback()
            else:
                self.db._conn.commit()

        elif data_status == DATA_CHANGE:
            print("DATA_CHANGE update.")
            kv_list = list()

            for kv in kwargs.items():
                kv_list.append("`{}`='{}'".format(kv[0], kv[1]))

            sql_update = "update {tb_name} set enabled = 0 where {kv_val}".format(
                tb_name=tb_name, kv_val=" and ".join(kv_list)
            )

            print(sql, '\n', sql_update)

            try:
                self.db.execute(sql_update)
                self.db.execute(sql)
            except Exception:
                self.db._conn.rollback()
            else:
                self.db._conn.commit()
            
        elif data_status == DATA_EQUAL:
            print("DATA_EQUAL pass.")

    def sql_maker_insert(self, tb_name, data, **kwargs):
        '''sql_maker_insert
        Make insert SQL string by data.
        '''
        k_list = list()
        v_list = list()
        use    = list()
        
        if "use" in kwargs:
            use = kwargs['use']

        for k, v in zip(data.keys(), data.values()):
            if v is not None:
                if len(use) > 0 and k not in use:
                    continue
                
                k_list.append("`%s`"%str(k))
                v_list.append("'%s'"%str(v))

        return "insert into {tb_name} ({k_val}) values ({v_val})".format(
            tb_name=tb_name, k_val=", ".join(k_list), v_val=", ".join(v_list)
        )

    def sql_id_exists(self, tb_name, **kwargs):
        kv_list = list()
        
        if len(kwargs.keys()) == 0:
            return False
        else:
            for kv in kwargs.items():
                kv_list.append("`{}`='{}'".format(kv[0], kv[1]))
            sql =  "select count(1) as count from {tb_name} where enabled = 1 and {kv_val}".format(
                tb_name=tb_name, kv_val=" and ".join(kv_list)
            )
            
            self.db.execute(sql)

            if self.db.cur.fetchone()['count'] > 0:
                return True
            else:
                return False

    def sql_is_equal(self, tb_name, data, use, **kwargs):
        kv_list = list()
        
        if len(kwargs.keys()) == 0:
            return -1

        if self.sql_id_exists(tb_name, **kwargs):   # This `not` is a debugger.
            for kv in kwargs.items():
                kv_list.append("`{}`='{}'".format(kv[0], kv[1]))

            sql = "select {col_name} from {tb_name} where enabled =1 and {kv_val}".format(
                tb_name=tb_name, kv_val=" and ".join(kv_list), 
                col_name=", ".join([k for k in data.keys() if k in use])
            )
            
            self.db.execute(sql)

            res = self.db.cur.fetchone()

            res = {k:v for k, v in zip(res.keys(), res.values())}
            res1 = {k:v for k, v in zip(data.keys(), data.values()) if (v is not None and k in use)}

            # print("****\n{}\n{}\n{}\n".format(res, use, res1))

            for kv in res1.items():

                if res[kv[0]] == kv[1]:
                    continue
                else:
                    try:
                        if float(res[kv[0]]) == float(res[kv[0]]):
                            continue
                    except Exception:
                        pass
                        
                    return DATA_CHANGE

            return DATA_EQUAL
            
        else:
            return NO_DATA

            