#! /usr/bin/env python

import psutil
from datetime import datetime
# from stem.control import Controller
from stem.util.system import pid_by_name
import sys
from stem.util.connection import get_connections, system_resolvers
import ConfigParser
from pyfcm import FCMNotification

# Configuring secure storage of API key:
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
print api_key
print registration_id

# Starting integration of PyFCM here:
# Send to single device.

push_service = FCMNotification(api_key=str(api_key))

message_title = "Tor relay status"
message_body = "Your relay is having some troubles"
result = push_service.notify_single_device(registration_id=str(registration_id), message_title=message_title, message_body=message_body)

print result

# End integration of PyFCM


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

if __name__ == '__main__':
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    net_io_test()
    # net_test()
    pid_test()

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
