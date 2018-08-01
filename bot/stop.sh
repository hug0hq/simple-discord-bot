#!/bin/bash

pid=`ps -ef | grep -n "python3 bot.py" | head -1 | awk '{print $2}'`
kill $pid
echo "Done"

