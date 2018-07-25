# -*- coding: utf-8 -*-

from redis import Redis, ConnectionPool
import json
from util.config import ConfigReader
from constant.config import REDIS_CFG

def equal(object1, object2):
    if object1 == object2:
        return True
    else:
        return False


class RedisController():
        
    def __init__(self, db):
        host, port = REDIS_CFG['host'], REDIS_CFG['port']
        self.db = db
        self.__pool__ = ConnectionPool(host=host, port=port, db=self.db)
        self._redis_conn = Redis(connection_pool=self.__pool__)
        print("Redis连接创建成功！[%s:%s db%s]"%(host, port, self.db))

    def rset(self, key, value):
        rvalue = self.rget(key)
        if rvalue is not None:
            try:
                rvalue = json.loads(rvalue)
            except Exception:
                pass

        if equal(value, rvalue):
            print("db{}:set【{} => <=】".format(self.db, key))
        elif rvalue == None:
            print("db{}:set【{} () => {}】".format(self.db, key, value))
        else:
            print("db{}:set【{} {} => {}】".format(self.db, key, rvalue, value))
        
        if isinstance(value, dict):
            value = json.dumps(value)
        
        self._redis_conn.set(key, value)
    
    def rget(self, key):
        try:
            res = self._redis_conn.get(key)
            if res is not None:
                return res.decode('utf-8')
            else:
                return None
        except Exception as e:
            print(str(e))
            return None

    def rdel(self, key):
        self._redis_conn.delete(key)
        print("db%s:删除【%s】的缓存"%(self.db,key))

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
                print("__update_dict_to_redis__ failed. {}".format(e))
                pass
        else:
            self.rset(k, v)

if __name__ == "__main__":
    pass