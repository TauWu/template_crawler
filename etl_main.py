# -*- coding: utf-8 -*-
# Extract - Transform - Load
from do.etl import Do
from sys import argv

if __name__ == "__main__":
    '''etl_main
    Start ETL project.
    '''
    etl_name = "sample" if len(argv) == 1 else argv[1]

    etl = Do(etl_name)
    etl.do()