import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import 'time' library. Allows us to use 'sleep'
import sys


class RelayControl:
    # Define a function named Blink()
    def relay_control(self, relay_num, state):
        print('RELAY NUM :', relay_num)
        print('STATE :', state)

        GPIO.setmode(GPIO.BOARD)  # Use board pin numbering
        print("GPIO mode set to :", GPIO.getmode())

        pin_num = 0
        if relay_num == 1:
            GPIO.setup(38, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
            pin_num = 38
        elif relay_num == 2:
            GPIO.setup(40, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
            pin_num = 40
        elif relay_num == 3:
            GPIO.setup(29, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
            pin_num = 29
        elif relay_num == 4:
            GPIO.setup(31, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
            pin_num = 31
        elif relay_num == 5:
            GPIO.setup(33, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
            pin_num = 33
        elif relay_num == 6:
            GPIO.setup(35, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
            pin_num = 35
        elif relay_num == 7:
            GPIO.setup(37, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
            pin_num = 37
        elif relay_num == 8:
            GPIO.setup(7, GPIO.OUT)  # Setup GPIO Pin 7 to OUT
            pin_num = 7
        else:
            print('no option')

        if state == 1:
            GPIO.output(pin_num, False)  # Switch on pin 7
            time.sleep(5)  # Wait
        elif state == 0:
            GPIO.output(pin_num, True)  # Switch off pin 7
            time.sleep(5)  # Wait
        else:
            print('NO')
        print "Done"  # When loop is complete, print "Done"
        # GPIO.cleanup()

    # Ask user for total number of blinks and length of each blink


g = RelayControl()
g.relay_control(int(sys.argv[1]), int(sys.argv[2]))
