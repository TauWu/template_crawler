# -*- coding: utf-8 -*-
# Database operator
from util.database import DBController
from copy import deepcopy

NO_DATA         = 0
DATA_CHANGE     = 1
DATA_EQUAL      = 2

class DBOpter(DBController):

    def __init__(self, project_name):
        DBController.__init__(self, project_name)

    def update_data(self, tb_name, data, use, **kwargs):
        data_status = self.sql_is_equal(tb_name, data, use, **kwargs)
        sql = self.sql_maker_insert(tb_name, data, use=use)

        if data_status == NO_DATA:
            self.info("NO_DATA, insert =>", **kwargs)
            self.debug(sql)
            
            try:
                self.execute(sql)
            except Exception:
                self._conn.rollback()
            else:
                self._conn.commit()

        elif data_status == DATA_CHANGE:
            self.info("DATA_CHANGE, update＝>", **kwargs)
            kv_list = list()

            for kv in kwargs.items():
                kv_list.append("`{}`='{}'".format(kv[0], kv[1]))

            sql_update = "update {tb_name} set enabled = 0 where {kv_val}".format(
                tb_name=tb_name, kv_val=" and ".join(kv_list)
            )

            self.debug("debug sql and sql_update", sql=sql, sql_update=sql_update)

            try:
                self.execute(sql_update)
                self.execute(sql)
            except Exception:
                self._conn.rollback()
            else:
                self._conn.commit()
            
        elif data_status == DATA_EQUAL:
            self.info("DATA_EQUAL, pass =>", **kwargs)

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

    def update_data_list(self, tb_name, data, use, sql_key):
        '''update_data_list
        Make insert SQL string by list data.
        params:
            tb_name
            data
            use
            **kwargs => key in database with its val.
        '''
        k_list      = list()
        v_list      = list()
        v_list_list = list()
        
        select_tpl      = "select count(1) as count from {tb_name} where {kv_val}"
        select_dtl_tpl  = "select {col_name} from {tb_name} where {kv_val}"
        insert_tpl      = "insert into {tb_name} ({k_val}) values ({v_val})"
        update_tpl      = "update {tb_name} set enabled = 0 where {kv_val}"

        # Get data from t(ransformer) module.
        for k, v in zip(data.keys(), data.values()):
            if k not in use:
                continue

            if not isinstance(v, list):
                k_list.append(str(k))
                v_list.append(str(v))

        raw_v_list = deepcopy(v_list)

        for k, v in zip(data.keys(), data.values()):
            if k not in use:
                continue

            if isinstance(v, list):
                v_kv = v[0]
                for v_k in v_kv.keys():
                    k_list.append(str(v_k))
                for v_kv in v:
                    for v_v in v_kv.values():
                        v_list.append(str(v_v))
                    v_list_list.append(v_list)
                    v_list = deepcopy(raw_v_list)

        # Check the data if existed.
        for v_list in v_list_list:
            sql_kv_val = dict()
            value_kv   = dict()
            for k, v in zip(k_list, v_list):
                if k in sql_key:
                    sql_kv_val = dict(sql_kv_val, **{k:v})
                value_kv = dict(value_kv, **{k:v})
                
            kv_val = " and ".join(
                ["`{}`='{}'".format(k, v) for k, v in sql_kv_val.items()]
            )
            # Check the data if existed.
            select_sql = select_tpl.format(
                tb_name=tb_name, kv_val= kv_val
            )
            self.execute(select_sql)
            count = self.cur.fetchone()["count"]
            
            update_sql = update_tpl.format(
                tb_name=tb_name, kv_val=kv_val
            )
            insert_sql = insert_tpl.format(
                tb_name=tb_name,
                k_val=", ".join(["`{}`".format(k) for k in value_kv.keys()]),
                v_val=", ".join(["'{}'".format(v) for v in value_kv.values()])
            )
            select_dtl_sql = select_dtl_tpl.format(
                tb_name=tb_name,
                col_name=",".join(["`{}`".format(k) for k in value_kv.keys()]),
                kv_val=kv_val
            )

            try:
                if count == 0:
                    self.info("NO_DATA, insert", key=kv_val)
                    print(insert_sql)
                    self.execute(insert_sql)
                    self._conn.commit
                else:
                    self.execute(select_dtl_sql)
                    db_data = self.cur.fetchone()
                    if db_data == value_kv:
                        self.info("DATA_EQUAL, pass", key=kv_val)
                    else:
                        self.info("DATA_UPDATE, update", key=kv_val)
                        self.execute(update_sql)
                        self.execute(insert_sql)
                        self._conn.commit

            except Exception:
                self.error("Database update FAILED.", key=kv_val)


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
            
            self.execute(sql)

            if self.cur.fetchone()['count'] > 0:
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
            
            self.execute(sql)

            res = self.cur.fetchone()

            res = {k:v for k, v in zip(res.keys(), res.values())}
            res1 = {k:v for k, v in zip(data.keys(), data.values()) if (v is not None and k in use)}

            for kv in res1.items():

                if kv[0].endswith("id"):
                    continue

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

            