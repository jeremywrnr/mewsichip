from time import sleep
import os
import signal
import subprocess
from subprocess import PIPE
import CHIP_IO.GPIO as GPIO
import datetime
from time import sleep

GPIO.cleanup()
GPIO.setup("XIO-P0", GPIO.IN)
GPIO.add_event_detect("XIO-P0", GPIO.RISING)
is_playing = False
global musicprocess

while True:
    if GPIO.event_detected("XIO-P0"):
        print "Rising edge detected ==========="
        if not is_playing:
            fname = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            musicprocess = subprocess.Popen(['arecord', '-f', 'cd', '-D', 'hw:0,0', fname], stdout=PIPE, stderr=PIPE)
            print 'recording track'
	    is_playing = True
        else:
            os.killpg(os.getpgid(musicprocess.pid), signal.SIGTERM)
            is_playing = False
    sleep(3)
GPIO.cleanup()

