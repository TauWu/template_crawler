#!/bin/bash

nohup python3 crawler_main.py lianjia > log/lianjia.log &
nohup python3 crawler_main.py ziroom  > log/ziroom.log  &
nohup python3 crawler_main.py qk      > log/qk.log      &
