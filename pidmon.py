#! /usr/bin/env python

from sys import argv
import psutil
from datetime import datetime

# So I think what I want to do here, is make a POST to the app engine backend with status & timestamp
# I want this script to be called by cron every minute

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if psutil.pid_exists(int(argv[1])):
    print("a process with pid %d exists" % int(argv[1]))
    print("timestamp %s" % current_time)
else:
    print("a process with pid %d does not exist" % int(argv[1]))
    print("timestamp %s" % current_time)
