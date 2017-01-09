#! /usr/bin/env python

# Needs to answer two questions:
# Is the server itself up and responsive -- ping_test (complete)
    # If not, needs to send a notification to firebase (or app engine)
    # This does depend on ping being reachable through our firewall at home and redirected to server
# Is it accepting connection inbound over the ports that are interesting to Tor --> port_test (complete)
    # This does depend on the right ports being fed to it via Cron execution
    # This is just part of its normal heartbeat status


from socket import socket
from sys import argv
import os

# Port Test --> generates informational if return false (means some network latency)
def port_test(server_info, port):
    try:
        sock = socket()
        sock.connect((server_info, int(port)))
        sock.close()
        return True
    except:
        return False

# Ping Test --> generates critical error if return false (means server is down or unreachable)
def ping_test(server_info):
    response = os.system("ping -c 1 " + server_info)

    if response == 0:
      return True
    else:
      return False


if __name__ == '__main__':
    # Python considers calling the executable file with the host for testing as two arguments
    if len(argv) < 3:
        print('Wrong number of arguments.')
    else:
        port_num = len(argv) - 2

    # Call Ping Test:
    if ping_test(argv[1]):
        print(argv[1], 'is up!')
    else:
        print(argv[1], 'is down!')

    # Call Port Test:
    test_port = 2
    counter = 1
    while (counter <= port_num):
        if port_test(argv[1], argv[test_port]):
            print(argv[1], 'is accepting conections over port %s' % argv[test_port])
        else:
            print(argv[1], 'is NOT accepting conections over port %s' % argv[test_port])
        test_port += 1
        counter += 1
