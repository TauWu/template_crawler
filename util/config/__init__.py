# -*- coding:utf-8 -*-
# 配置文件基础模块

import configparser

class ConfigParser():

    def __init__(self, config_file='config.cfg', section_name='config'):
        self.config_file = config_file
        self.section_name = section_name
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def add_section(self, section_name):
        self.config.add_section(section_name)
        self.use_section(section_name)

    def use_section(self, section_name):
        self.section_name = section_name

    def set_kv(self, k, v):
        self.config.set(self.section_name, k, str(v))
        self.save

    def read(self, k):        
        return self.config[self.section_name][k]

    def read_all(self):
        return {k:self.read(k) for k in self.config[self.section_name]}

    @property
    def save(self):
        self.config.write(open(self.config_file, 'w'))

class ConfigReader(ConfigParser):

    @staticmethod
    def read_section_key(config_name, section_name, *k, **kwargs):

        cp = ConfigParser(config_file=config_name, section_name=section_name)

        if "all" in kwargs.keys() and kwargs["all"]:
            return cp.read_all()
        elif len(k) == 1:
            return cp.read(k[0])
        else:
            return {ik:cp.read(ik) for ik in k}