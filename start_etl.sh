#!/bin/bash

nohup python3 etl_main.py lianjia  &
nohup python3 etl_main.py ziroom   &
nohup python3 etl_main.py qk       &
