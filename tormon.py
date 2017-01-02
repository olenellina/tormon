#! /usr/bin/env python

from urllib2 import urlopen
from socket import socket
from sys import argv

# Tests that I will want:
# Inbound port 80 (OrPort)
# Inbound port 443 (DirPort)
# General ping (so that if first two tests fail, I will no if the server is at least responsive)
# Idea here is that, if one of these tests fail --> push notification generated to mobile app

# Might still want a VERY basic cron job that tests for the Tor PID running and sends to API if not

def tcp_test(server_info):
    # Really, what I want to do here is test specific ports associated with tor
    # I could have functions that test inbound over Tor ports
    cpos = server_info.find(':')
    try:
        sock = socket()
        sock.connect((server_info[:cpos], int(server_info[cpos+1:])))
        sock.close
        return True
    except:
        return False

def http_test(server_info):
    # The tor server is not a web server, so I don't think I need this function
    # Maybe have a generic ping test here
    try:
        data = urlopen(server_info).read()
        return True
    except:
        return False

def server_test(test_type, server_info):
    # Again, don't think I want this script to be handed parameters - I will always want to test certain ports
    if test_type.lower() == 'tcp':
        return tcp_test(server_info)
    elif test_type.lower() == 'http':
        return http_test(server_info)

# Will need more extensive error handling here --> this is where I will invoke *something* to generate push notifications
if __name__ == '__main__':
    if len(argv) != 3:
        print('Wrong number of arguments.')
    elif not server_test(argv[1], argv[2]):
        print('Unable to connect to the service.')
