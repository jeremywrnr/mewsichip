# mewsician CHIP code, by team goacat.

import CHIP_IO.GPIO as GPIO
from time import sleep
import subprocess
import datetime
import psutil
import sys
import os

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

    # starting the recording
    args = ['arecord', '-f', 'cd', fname]
    musicproc = subprocess.Popen(args)
    mpid = psutil.Process(musicproc.pid)
    print(fname)
    print(mpid)
    print("""  ...meow, edge detected!
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
    print("\nStopping recording...")
    mpid.terminate() # from record()
    mname = bname + ".mp3"

    print("Compressing audio...")
    subprocess.call(['sudo', 'chown', 'chip:chip', fname])
    subprocess.call(['lame', '-V2', fname, mname]) # convert
    subprocess.call(['sudo', 'chown', 'chip:chip', mname])

    print("Uploading music...")
    auth = 'auth=' + authentication # upload
    path =  os.getcwd() + '/' + mname
    upload = 'file=@' + path
    args = ['curl', '--form', upload, '--form', auth, 'http://mewsician.win/upload']
    print(subprocess.check_output(args))

    print("Cleaning up...")
    # doesn't seem to recognize the home environment
    # subprocess.call(['mv', '-v', mname, os.environ['HOME'] + "/audio/"])
    subprocess.call(['mv', '-v', mname, "/home/chip/audio/"])
    subprocess.call(['rm', '-v', fname])
    print("Complete.")

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
