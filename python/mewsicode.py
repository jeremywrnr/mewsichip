# mewsician CHIP code, by team goacat.

import CHIP_IO.GPIO as GPIO
from datetime import timedelta
from time import sleep
import subprocess
import datetime
import serial
import random
import psutil
import sys
import os

GPIO.cleanup()
sing_channel = "XIO-P1"
record_channel = "XIO-P7"

GPIO.setup(record_channel, GPIO.IN)
GPIO.setup(sing_channel, GPIO.IN)

GPIO.add_event_detect(record_channel, GPIO.RISING)
GPIO.add_event_detect(sing_channel, GPIO.RISING)


# hardcoded file locations
codeLoc = "/home/chip/mewsician/"
audioLoc = "/home/chip/audio/"
queue = audioLoc + "queue"

# auth passed in from (../start)
authentication = sys.argv[1]
recording = False
listening = False
singing = False
play_pid = None
fname = None
bname = None
mpid = None

# trigger playback of audio file
def playback():
    global play_pid
    print("Starting playback...")

    # get a random audio clip to play from the audio folder
    music_files = [f for f in os.listdir(audioLoc) if f.endswith('.mp3')]
    if len(music_files) > 0:
        m_index = random.randint(0, len(music_files)-1)
        print 'm_index is', m_index
        music_path = audioLoc + music_files[m_index]
        playback_fname = music_path

        args = ['mplayer', playback_fname]
        playproc = subprocess.Popen(args)
        play_pid = psutil.Process(playproc.pid)
    else:
        print 'no playable music...'


# code that runs once when the script is starting.
def startup():
    print "\n<||||| - mewsician . commences - |||||>\n"
    try: # reupload and files that previously failed
        for file in open(queue, 'r'):
            retryUpload(file)
    except: # no uploads || !file exists yet || upload err
        args = ['touch', queue]
        subprocess.Popen(args)
        print sys.exc_info()[0]


# trigger external recording and create a new subprocess for this
# combine current time and uid for the filename to be uploaded
def record():
    global fname, bname, mpid
    print("Starting recording...")

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
    print("\nStopping recording...")
    mpid.terminate() # from record()
    mname = bname + ".mp3"

    # stopped recording, update arduino lights
    send_serial('u')

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

def trigger_record():
    print 'trigger record'
    if recording:
        end_recording()
        send_serial('d')
    else:
        start_recording()

def start_recording():
    global recording
    global listening
    global singing
    recording = True
    listening = False
    singing = False

    # global hunger
    # hunger = 0

    # write_time_to_file()
    send_serial('r')
    record()

def end_recording():
    send_serial('e')
    upload()
    global recording
    recording = False

def write_time_to_file():
    with open('last_time_practiced.txt', 'w+') as f:
        f.write(datetime.datetime.now().isoformat())

def start_singing():
    global listening
    global singing
    singing = True
    listening = False

    send_serial('s')
    playback()

def end_singing():
    global singing
    global play_pid

    singing = False
    send_serial('d')
    # if still playing, kill the playback process
    if pid_active(play_pid):
        p = psutil.Process(play_pid)
        p.terminate()
    print "playback ending."
    play_pid = None

def trigger_listen():   
    if listening:
        end_listening()
    else:
        start_listening()

def start_listening():
    global recording
    global listening
    global singing
    listening = True
    recording = False
    singing = False
    send_serial('l')

def end_listening():
    global listening
    listening = False
    send_serial('d')

def send_serial(ch):
    # d, r, s, c
    for i in range(0,2):
        try:
            ser.write(ch)
        except:
            print "failed to send '", ch, "'... try again"

def pid_active(pid):
    return pid in psutil.pids()


def calc_hunger():
    # get last time entered listen or record state
    try:
        with open('last_time_practiced.txt', 'r+') as f:
            # process last date
            lastdatestr = f.readline()
            if lastdatestr:
                lastdate = datetime.datetime.strptime(lastdatestr, "%Y-%m-%dT%H:%M:%S.%f")
                now = datetime.datetime.now()
                difference = now - lastdate
                days = difference.days
            else:
                days = 0
            send_serial('h')
            sleep(3)
            send_serial(bytes([days]))
            print "it's been ", days, " since you practiced"
            return days
    except:
        print "oh no file error"
        return 0


last_time = -1

ser = serial.Serial('/dev/ttyS0')
sleep(1) # wait for channel to open
# hunger = calc_hunger()

# initialize as dreaming
send_serial('d')

startup() # setting up code to initialize the board/uploads

while True: # continually in this state, check if channel HI
    # print(GPIO.input(record_channel))
    # record ing
    if GPIO.event_detected(record_channel) and not GPIO.input(record_channel):
        trigger_record() # on button press, trigger callback
        sleep(10) # wait 10 secs for debouncing, bad but works.
        # THIS MEANS RECORD FOR AT LEAST 10 seconds please:

    # start sing
    if not recording: 
        if not singing and not GPIO.input(sing_channel):
            if last_time is -1:
                last_time = datetime.datetime.now()
            else:
                if datetime.datetime.now() - last_time > timedelta(0, 0, 250):
                    last_time = -1
                    print "singing..."
                    start_singing()
                    sleep(3) # wait 3 secs for debouncing, bad but works.

        # # end sing
        if singing and GPIO.input(sing_channel):
            print "stop singing..."
            end_singing()
            sleep(3) # wait 3 secs for debouncing, bad but works.
