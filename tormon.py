#! /usr/bin/env python

# Needs to answer four questions:
# Is the Tor pid (or pids) running? (complete)
# What are the network stats? (complete)
# Does relay appear offline to Tor?
# What are my relays flags (am I a guard?)?

import psutil
from datetime import datetime
from stem.control import Controller
import stem.control
from stem.util.system import pid_by_name
import sys
# from stem.util.connection import get_connections, system_resolvers
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
    # Not quite sure what interesting information this gives me, so might remove
    net_traffic = psutil.net_io_counters()
    print(net_traffic)

# Tor Secific Network Test
def tor_net_test():
    # Stub pid, until Tor is running and integrated
    tor_pids.append(1056)

    all_traffic = psutil.net_connections(kind='tcp')
    for traffic in all_traffic:
        if traffic.pid in tor_pids:
            print(traffic)


def flag_test():
    user_traffic = stem.control.UserTrafficAllowed
    print("whoot")
    print(user_traffic)

if __name__ == '__main__':
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tor_pids = []

    net_io_test()
    tor_net_test()
    flag_test()
    pid_test()

# Potential Code for HTTP POST/Put/Get
#
# import httplib, urllib
#
# headers = {'X-API-TOKEN': 'your_token_here'}
# payload = "'title'='value1'&'name'='value2'"
#
# conn = httplib.HTTPConnection("heise.de")
# conn.request("POST", "", payload, headers)
# response = conn.getresponse()
#
# print response
#
# OR
# payload = {'username': 'bob', 'email': 'bob@bob.com'}
# >>> r = requests.put("http://somedomain.org/endpoint", data=payload)
# You can then check the response status code with:
#
# r.status_code
# or the response with:
#
# r.content

#### Optional Tor Tests:

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
