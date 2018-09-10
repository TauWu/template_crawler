# -*- coding: utf-8 -*-
# Reporter System

# Translate data from redis/database to xlsx table, and send it to ordered email.

from do.reporter import Do
from sys import argv

if __name__ == "__main__":
    '''reporter_main
    Start Reporter project.
    '''
    rpt_name = "sample" if len(argv) == 1 else argv[1]

    rpt = Do(rpt_name)
    rpt.do()