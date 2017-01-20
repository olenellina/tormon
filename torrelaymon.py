#! /usr/bin/env python

# Needs to answer four questions:
# Is the Tor pid (or pids) running? (complete)
# What are the network stats? (complete)
# Does relay appear offline to Tor?
# What are my relays flags (am I a guard?)?

import psutil
import stem.control
from stem.util.system import pid_by_name
# import sys
# from stem.util.connection import get_connections, system_resolvers
import requests

# Tor Pid Test:
def pid_test():
    # ToDo: If tor relay does not generate mulitple Tor pids, need to change this code:
    tor_pids = pid_by_name('tor', multiple = True)

    if not tor_pids:
        print("Unable to get tor's pid. Is it running?")
        data['tor_pid'] = False
    elif len(tor_pids) > 1:
        print("You're running %i instances of tor, picking the one with pid %i" % (len(tor_pids), tor_pids[0]))
        data['tor_pid'] = True
    else:
        print("Tor is running with pid %i" % tor_pids[0])
        data['tor_pid'] = True


# Network Traffic Test
def net_io_test():
    # Not quite sure what interesting information this gives me, so might remove
    net_traffic = psutil.net_io_counters()
    print(net_traffic)

# Tor Secific Network Test
def tor_net_test():
    # Stub pid, until Tor is running and integrated
    tor_net_connections = 0
    tor_pids.append(1056)

    all_traffic = psutil.net_connections(kind='tcp')
    for traffic in all_traffic:
        if traffic.pid in tor_pids:
            print(traffic)
            tor_net_connections += 1
    data['net_connections'] = tor_net_connections

# Tor Flag Test:
def flag_test():
    user_traffic = stem.control.UserTrafficAllowed
    print(user_traffic)

# Function that will handle packaging and sending of data to app engine:
def appengine_send():
    r = requests.post("http://torrelaymonitoring.appspot.com", data=data)
    # r = requests.post("http://localhost:8080", data=data)
    print(r.status_code)
    print(r.content)

if __name__ == '__main__':
    tor_pids = []
    data = {'name': 'Obama', 'tor_pid': None, 'net_connections': None}

    net_io_test()
    tor_net_test()
    flag_test()
    pid_test()
    appengine_send()
