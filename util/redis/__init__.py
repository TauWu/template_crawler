# -*- coding: utf-8 -*-

from redis import Redis, ConnectionPool
import json
from util.config import ConfigReader
from constant.config import REDIS_CFG
from util.common.logger import LogBase

def equal(object1, object2):
    return True if object1 == object2 else False

class RedisController(LogBase):
        
    def __init__(self, db, project_name="sample"):
        LogBase.__init__(self, project_name, "redis")

        host, port = REDIS_CFG['host'], REDIS_CFG['port']
        self.db = db
        self.__pool__ = ConnectionPool(host=host, port=port, db=self.db)
        self._redis_conn = Redis(connection_pool=self.__pool__)
        self.info("Connect to redis-server SUCCEED.", host=host, port=port, db=self.db)

    def rset(self, key, value):
        rvalue = self.rget(key)
        if rvalue is not None:
            try:
                rvalue = json.loads(rvalue)
            except Exception:
                pass

        if equal(value, rvalue):
            self.info("db{}:set【{} => <=】".format(self.db, key))
        elif rvalue == None:
            self.info("db{}:set【{} () => {}】".format(self.db, key, value))
        else:
            self.info("db{}:set【{} {} => {}】".format(self.db, key, rvalue, value))
        
        if isinstance(value, dict):
            value = json.dumps(value)
        
        self._redis_conn.set(key, value)
    
    def rget(self, key):
        try:
            res = self._redis_conn.get(key)
            return None if res is None else res.decode('utf-8')
            
        except Exception as e:
            self.error("Get value from redis error!", key=key, err=e)
            return None

    def rdel(self, key):
        self._redis_conn.delete(key)
        self.info("db%s:删除【%s】的缓存"%(self.db,key))

    @property
    def dbsize(self):
        return self._redis_conn.dbsize()

    def rpipeset(self, lists):

        pipe = self._redis_conn.pipeline(transaction=True)

        for list_detail in lists:
            key = list(list_detail.keys())[0]
            value = list_detail[key]
            self.rset(key, value)
        
        pipe.execute()

    @property
    def rscan(self):
        '''扫描Redis'''
        for key in self._redis_conn.keys():
            yield key.decode('utf-8'), self.rget(key)

    def __update_dict_to_redis__(self, k, v):
        '''__update_dict_to_redis__
        Merge dict rather than replace it.
        '''
        if self.rget(k) is not None:
            bf_val = self.rget(k)
            try:
                bf_val = json.loads(bf_val)
                bf_val = dict(bf_val, **v)
                self.rset(k, bf_val)
            except Exception as e:
                self.warn("__update_dict_to_redis__ failed.",err=e)
                pass
        else:
            self.rset(k, v)

if __name__ == "__main__":
    pass