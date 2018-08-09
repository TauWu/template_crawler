#!/bin/bash

nohup python3 etl_main.py lianjia > log/etl_lianjia.log &
nohup python3 etl_main.py ziroom  > log/etl_ziroom.log  &
nohup python3 etl_main.py qk      > log/etl_qk.log      &
