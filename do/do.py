# -*- coding: utf-8 -*-

class Do(object):

    @staticmethod
    def start_crawler():
        Do.read_crawler_config()
        Do.read_quota_config()

    @staticmethod
    def read_crawler_config():
        pass

    @staticmethod
    def read_quota_config():
        pass