#!/bin/bash

ps -ef | grep crawler | awk {' print $2 '} | xargs kill -s 9
ps -ef | grep etl     | awk {' print $2 '} | xargs kill -s 9
