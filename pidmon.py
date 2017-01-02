from sys import argv
import psutil

if psutil.pid_exists(int(argv[1])):
    print("a process with pid %d exists" % int(argv[1]))
else:
    print("a process with pid %d does not exist" % int(argv[1]))
