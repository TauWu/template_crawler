# -*- coding: utf-8 -*-
# Extract - Transform - Load
from do.etl import Do
from sys import argv

if __name__ == "__main__":
    '''etl_main
    Start ETL project.
    '''
    if len(argv) == 1: etl_name = "sample"
    elif len(argv) == 2: etl_name = argv[1]

    etl = Do(etl_name)
    etl.do()