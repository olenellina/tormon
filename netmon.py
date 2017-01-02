#! /usr/bin/env python

from urllib2 import urlopen
from socket import socket
from sys import argv
import os

# Tests that I will want:
# Inbound port 80 (OrPort)
# Inbound port 443 (DirPort)
# General ping (so that if first two tests fail, I will no if the server is at least responsive)

def tcp_test(server_info):
    # This code will be updated to have tests for specific ports
    cpos = server_info.find(':')
    try:
        sock = socket()
        sock.connect((server_info[:cpos], int(server_info[cpos+1:])))
        sock.close
        print('Tested succesfully')
        return True
    except:
        return False

def ping_test(server_info):
    # This code will handle the basic ping test
    # Needs to be updated to strip away the port that is passed in currently
    response = os.system("ping -c 1 " + server_info)

    if response == 0:
      print(server_info, 'is up!')
    else:
      print(server_info, 'is down!')

def server_test(server_info):
    # I guess this is the main function that executes others?
    ping_test(server_info)
    return tcp_test(server_info)


# Will need more extensive error handling here --> this is where I will invoke *something* to generate push notifications
if __name__ == '__main__':
    if len(argv) != 2:
        print('Wrong number of arguments.')
    elif not server_test(argv[1]):
        print('Unable to connect to the service.')

# General Notes:
# Idea here is that, if one of these tests fail --> push notification generated to mobile app
# There will be another script on the tor relay itself to monitor the Tor PID and send results to API
# Might want to get dynamic DNS or something to handle comcast changing WAN IP
# Script should allow people to define their own ports, so those should not be configured (instead passed by cron)

# Code I No Longer Need:
# def http_test(server_info):
#     # The tor server is not a web server, so I don't think I need this function
#     # Maybe have a generic ping test here
#     try:
#         data = urlopen(server_info).read()
#         return True
#     except:
#         return False
