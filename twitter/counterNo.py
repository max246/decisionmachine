import liblo
import time
import sys
from Arduino import *


server = None

# create server
try:
    server = liblo.Server(1235)
except liblo.ServerError, err:
    print str(err)
    sys.exit()


arduino = Arduino("/dev/ttyACM1")
arduino.init()


def updateNumber(path,number):
     print "number", number
     arduino.send("U"+str(number[0]))

def fallback(path, args, types, src):
    print "got unknown message '%s' from '%s'" % (path, src.url)
    for a, t in zip(args, types):
        print "argument of type '%s': %s" % (t, a)

server.add_method("/update", 'i', updateNumber)
server.add_method(None, None, fallback)


while True:
    output = arduino.read()
    if output != None and len(output) > 0:
         print output
    #print "test"
    server.recv(100)
