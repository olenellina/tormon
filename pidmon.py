#! /usr/bin/env python

from sys import argv
import psutil
from datetime import datetime

# So I think what I want to do here, is make a POST to the app engine backend with status & timestamp
# I want this script to be called by cron every minute

def pid_test(pid):

    if psutil.pid_exists(int(pid)):
        return True
    else:
        return False

def net_io_test():
    result = psutil.net_io_counters()
    print(result)

def net_test():
    result = psutil.net_connections(kind='tcp')
    print(result)

if __name__ == '__main__':
    pid = argv[1]
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not pid_test(pid):
        print("a process with pid %d exists" % int(pid))
        print("timestamp %s" % current_time)
    else:
        print("a process with pid %d does not exist" % int(pid))
        print("timestamp %s" % current_time)

    net_io_test()
    net_test()
