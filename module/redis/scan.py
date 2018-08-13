from util.redis import RedisController as RC

class RedisScanner():

    @staticmethod
    def rds_data_iter(db, project_name):
        rds_ctl = RC(db, project_name)
        yield from rds_ctl.rscan