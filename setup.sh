#!/bin/bash

#LOGFILE=todo.log
#LOGLEVEL=debug
#
#sudo killall gunicorn
#sudo gunicorn -k egg:gunicorn#tornado -D --log-level=$LOGLEVEL --log-file=$LOGFILE server:app

./server.py
