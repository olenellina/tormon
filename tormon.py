#! /usr/bin/env python

# Replaced by torrealymon.py

import psutil
from datetime import datetime
from stem.control import Controller
import stem.control
from stem.util.system import pid_by_name
import sys
import ConfigParser
from pyfcm import FCMNotification

####### Configuring secure storage of API key #######
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

api_key = ConfigSectionMap("SectionOne")['api_key']
registration_id = ConfigSectionMap("SectionOne")['reg_id']

####### Starting integration of PyFCM #######
# Send notifications to single device.

push_service = FCMNotification(api_key=str(api_key))

message_title = "Tor relay status"
message_body = "Your relay is having some troubles"
firebase_result = push_service.notify_single_device(registration_id=str(registration_id), message_title=message_title, message_body=message_body)

print firebase_result

# Tor Pid Test:
def pid_test():
    # ToDo: If tor relay does not generate mulitple Tor pids, need to change this code:
    tor_pids = pid_by_name('tor', multiple = True)

    if not tor_pids:
        print("Unable to get tor's pid. Is it running?")
        sys.exit(1)
    elif len(tor_pids) > 1:
        print("You're running %i instances of tor, picking the one with pid %i" % (len(tor_pids), tor_pids[0]))
    else:
        print("Tor is running with pid %i" % tor_pids[0])

# Network Traffic Test
def net_io_test():
    net_traffic = psutil.net_io_counters()
    print(net_traffic)

# Tor Secific Network Test
def tor_net_test():
    all_traffic = psutil.net_connections(kind='tcp')
    for traffic in all_traffic:
        if traffic.pid in tor_pids:
            print(traffic)

if __name__ == '__main__':
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tor_pids = []

    net_io_test()
    tor_net_test()
    pid_test()
