#!/bin/bash
# -*- coding: utf-8 -*-

# Crawler Main
# 
# Author : Tau Woo
# Date   : 2018-07-19

from do.do import Do
from sys import argv

if __name__ == "__main__":
    '''Crawler Main
    Start crawl websites with appointed config.     
    '''
    # You will get appointed crawler name from command.
    if len(argv) == 1: crawler_name = "sample"
    elif len(argv) == 2: crawler_name = argv[1]
    
    crawler = Do(crawler_name)