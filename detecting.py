import CHIP_IO.GPIO as GPIO
GPIO.setup("XIO-P0", GPIO.IN)

# adding an event trigger on the rising edge

GPIO.add_event_detect("XIO-P0", GPIO.RISING)
if GPIO.event_detected("XIO-P0"):
    print "Rising edge detected ==========="

# constantly pump out the current state.

while True:
    if GPIO.input("XIO-P0"):
        print("HIGH")
    else:
        print("LOW")
    sleep(100)
