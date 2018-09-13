#!/bin/bash
# -*- coding: utf-8 -*-

# Crawler Main
# 
# Author : Tau Woo
# Date   : 2018-07-19

from do.crawler import Do
from sys import argv

if __name__ == "__main__":
    '''Crawler Main
    Start crawl websites with appointed config.     
    '''
    # You will get appointed crawler name from command.  
    crawler_name = "sample" if len(argv) == 1 else argv[1]
    crawler = Do(crawler_name)

    crawler.do()

    # Here is a test for data from redis to xlsx files.
    # crawler.rds_to_xlsx("{}.xlsx".format(crawler_name), crawler_name)
