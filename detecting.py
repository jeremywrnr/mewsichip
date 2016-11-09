# adding an event trigger on the rising edge

import CHIP_IO.GPIO as GPIO

channel = "XIO-P0"
record = False

GPIO.setup(channel, GPIO.IN)

while True: # continually in this state
    GPIO.wait_for_edge(channel, GPIO.RISING)
    print "Button press detected =========="
    if record:
        print "Stopping recording."
        record = False
    else:
        print "Starting recording."
        record = True

GPIO.cleanup()
