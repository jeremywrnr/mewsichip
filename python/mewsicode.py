# mewsician CHIP code.

import CHIP_IO.GPIO as GPIO
from subprocess import PIPE
from time import sleep
import subprocess
import datetime
import psutil

# TODO source authentication from device environment file
# TODO mechanism for creation / uploading of these??????

GPIO.cleanup()
outled = "XIO-P1"
channel = "XIO-P0"
GPIO.setup(channel, GPIO.IN)
GPIO.setup(outled, GPIO.OUT)
GPIO.output(outled, GPIO.HIGH)
GPIO.add_event_detect(channel, GPIO.RISING)

print "Mewsician starting."
recording = False
fname = None
mpid = None

# trigger external recording and create a new subprocess for this
# combine current time and uid for the filename to be uploaded
def record():
    global fname, mpid
    print("Starting recording...")
    GPIO.output(outled, GPIO.LOW)
    fname = datetime.datetime.now().strftime("%Y-%m-%d @ %H:%M:%S") + '.mp3'
    print(fname)
    args = ['arecord', '-f', 'cd', '-D', 'hw:0,0', fname]
    musicproc = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
    mpid = psutil.Process(musicproc.pid)
    print('musicprocess pid is ', mpid)
    print("""meow - edge detected.
  |\      _,,,---,,_
  /,`.-'`'    -.  ;-;;,_
 |,4-  ) )-,_..;\ (  `'-'
'---''(_/--'  `-'\_)
        """)

# trigger external uploading
# will use authentication
def upload():
    print("Stopping recording...")
    GPIO.output(outled, GPIO.HIGH)
    print('stop: musicprocess pid is ', mpid)
    # mpid.terminate()

def trigger():
    if recording:
        upload()
        global recording
        recording = False
    else:
        record()
        global recording
        recording = True
    sleep(3) # wait for debouncing 3 secs, bad.

while True: # continually in this state, check if channel HI
    if GPIO.event_detected(channel) and GPIO.input(channel):
        trigger()
