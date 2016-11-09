from time import sleep

# adding an event trigger on the rising edge

import CHIP_IO.GPIO as GPIO
GPIO.setup("XIO-P0", GPIO.IN)
GPIO.add_event_detect("XIO-P0", GPIO.RISING)
if GPIO.event_detected("XIO-P0"):
    print "Button press detected ==========="

def loop():
    return 0

while True:
    loop() # prevent exiting

# constantly pump out the current state.
# if GPIO.input("XIO-P0"):
# print("HIGH")
# else:
# print("LOW")
# sleep(0.5)
