# mewsician CHIP code, by team goacat.

import CHIP_IO.GPIO as GPIO
from time import sleep
import subprocess
import datetime
import psutil
import sys
import os

# TODO source authentication from device environment file
# TODO mechanism for creation / uploading of these??????

GPIO.cleanup()
outled = "XIO-P1"
channel = "XIO-P0"
GPIO.setup(channel, GPIO.IN)
GPIO.setup(outled, GPIO.OUT)
GPIO.output(outled, GPIO.HIGH)
GPIO.add_event_detect(channel, GPIO.RISING)

print "\n<||||| - mewsician . commences - |||||>\n"

# auth passed in from (../start)
authentication = sys.argv[1]
recording = False
fname = None
bname = None
mpid = None

# trigger external recording and create a new subprocess for this
# combine current time and uid for the filename to be uploaded
def record():
    global fname, bname, mpid
    print("Starting recording...")
    GPIO.output(outled, GPIO.LOW)
    bname = datetime.datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
    fname =  bname + '.wav'

    # TODO get this recording thing working
    args = ['arecord', '-f', 'cd', fname]
    musicproc = subprocess.Popen(args)
    mpid = psutil.Process(musicproc.pid)
    print(fname)
    print(mpid)
    print("""meow - edge detected.
  |\      _,,,---,,_
  /,`.-'`'    -.  ;-;;,_
 |,4-  ) )-,_..;\ (  `'-'
'---''(_/--'  `-'\_)
        """) # =^_^=

# stop current recording
# trigger external uploading
# will use authentication
def upload():
    GPIO.output(outled, GPIO.HIGH)
    print("Stopping recording...")
    mpid.terminate() # from record()
    mname = bname + ".mp3"
    subprocess.call(['sudo', 'chown', 'chip:chip', fname])
    subprocess.call(['lame', '-V2', fname, mname]) # convert
    subprocess.call(['sudo', 'chown', 'chip:chip', mname])
    print("Terminated. Uploading...")
    auth = 'auth=' + authentication
    file = 'file=@' + os.getcwd() + mname
    # TODO figure out what is crashing here
    args = ['curl', '--form', file, '--form', auth, 'http://mewsician.win/upload']
    prog = subprocess.check_output(args)
    print("Status: ", prog)
    # TODO move mp3 to the audio folder and clean up/remove wav file

def trigger():
    if recording:
        upload()
        global recording
        recording = False
    else: # start recording
        record()
        global recording
        recording = True
    sleep(3) # wait 3 secs for debouncing, bad but works.

while True: # continually in this state, check if channel HI
    if GPIO.event_detected(channel) and GPIO.input(channel):
        trigger() # on button press, trigger callback
