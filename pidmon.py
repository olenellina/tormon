#! /usr/bin/env python

import psutil
from datetime import datetime
# from stem.control import Controller
from stem.util.system import pid_by_name
import sys
from stem.util.connection import get_connections, system_resolvers

# So I think what I want to do here, is make a POST to the app engine backend with status & timestamp
# I want this script to be called by cron every minute

def pid_test():
    tor_pids = pid_by_name('tor', multiple = True)

    # In Python, an empty array is false
    if not tor_pids:
        print("Unable to get tor's pid. Is it running?")
        sys.exit(1)
    elif len(tor_pids) > 1:
        print("You're running %i instances of tor, picking the one with pid %i" % (len(tor_pids), tor_pids[0]))
    else:
        print("Tor is running with pid %i" % tor_pids[0])

def net_io_test():
    result = psutil.net_io_counters()
    print(result)

def net_test():
    result = psutil.net_connections(kind='tcp')
    print(result)

#### Tor Tests:

# def pid_test2():
    # resolvers = system_resolvers()
    #
    # if not resolvers:
    #   print("Stem doesn't support any connection resolvers on our platform.")
    #   sys.exit(1)
    #
    # picked_resolver = resolvers[0]  # lets just opt for the first
    # print("Our platform supports connection resolution via: %s (picked %s)" % (', '.join(resolvers), picked_resolver))

    # with Controller.from_port(port = 9051) as controller:
    #   controller.authenticate()  # provide the password here if you set one
    #
    #   bytes_read = controller.get_info("traffic/read")
    #   bytes_written = controller.get_info("traffic/written")
    #
    #   print("My Tor relay has read %s bytes and written %s." % (bytes_read, bytes_written))

if __name__ == '__main__':
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not pid_test():
        print("a process with pid %d exists" % int(pid))
        print("timestamp %s" % current_time)
    else:
        print("a process with pid %d does not exist" % int(pid))
        print("timestamp %s" % current_time)

    net_io_test()
    # net_test()
    pid_test()
