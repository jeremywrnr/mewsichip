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


# hardcoded file locations
codeLoc = "/home/chip/mewsician/"
audioLoc = "/home/chip/audio/"
queue = audioLoc + "queue"

# auth passed in from (../start)
authentication = sys.argv[1]
recording = False
fname = None
bname = None
mpid = None


# code that runs once when the script is starting.
def startup():
    print "\n<||||| - mewsician . commences - |||||>\n"
    try: # reupload and files that previously failed
        for file in open(queue, 'r'):
            retryUpload(file)
    except: # no uploads || !file exists yet || upload err
        args = ['touch', queue]
        subprocess.Popen(args)
        print(e)


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


def retryUpload(file):
    # TODO implement
    print(file)


# stop current recording, compress file format
# trigger external uploading if connected to the network
def upload():
    global mname
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
    try: # if upload fails (no network connection), write it to a queue
        print(subprocess.check_output(args))
        print("Cleaning up...")
        subprocess.call(['mv', '-v', mname, audioLoc])
        subprocess.call(['rm', '-v', fname])
        print("Complete.")
    except subprocess.CalledProcessError as e:
        with open(audioLoc + "queue", "a") as q:
            q.write(mname)
        print(e.output)


def trigger():
    global recording
    if recording:
        upload()
        recording = False
    else: # start recording
        record()
        recording = True
    sleep(3) # wait 3 secs for debouncing, bad but works.


while True: # continually in this state, check if channel HI
    if GPIO.event_detected(channel) and GPIO.input(channel):
        trigger() # on button press, trigger callback

