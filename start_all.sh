#!/bin/bash

nohup python3 crawler_main.py lianjia; python3 etl_main.py lianjia > log/lianjia.log &
nohup python3 crawler_main.py ziroom;  python3 etl_main.py ziroom  > log/ziroom.log  &
nohup python3 crawler_main.py qk;      python3 etl_main.pyqk       > log/qk.log      &
