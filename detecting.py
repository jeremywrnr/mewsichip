# adding an event trigger on the rising edge

import CHIP_IO.GPIO as GPIO
from time import sleep

channel = "XIO-P0"
record = False

GPIO.setup(channel, GPIO.IN)
print "Mewsician starting."

while True: # continually in this state

    GPIO.wait_for_edge(channel, GPIO.FALLING)
    print "Button press detected =========="

    sleep(0.1) # wait for debouncing

    if record:
        print "Stopping recording."
        record = False
    else:
        print "Starting recording."
        record = True

GPIO.cleanup()
