from util.redis import RedisController as RC

class RedisScanner():

    @staticmethod
    def rds_data_iter(db):
        rds_ctl = RC(db)
        yield from rds_ctl.rscan