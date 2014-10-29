import os
import time
import subprocess

def checkCamera():
    return os.path.exists("/dev/video0")

while True:
    if checkCamera():
        subprocess.call(['/bin/sh','stream.sh'])
    else:
        print "Error no camera!"
    time.sleep(1)

