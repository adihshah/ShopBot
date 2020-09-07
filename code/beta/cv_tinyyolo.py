import cv2
import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import subprocess

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# gets video feed from the pi camera
cam = cv2.VideoCapture(0)
#model to detect object


#force quit external button on pitft
def Pin27_callback(channel):
    global y
    y = False
    print('quit button has been pressed')

#GPIO 27 as interrupt 
GPIO.add_event_detect(27, GPIO.FALLING, callback=Pin27_callback)

# checking to see if camera is opened
if(not cam.isOpened()):
    print('Camera cannot be found')
    y = False
    quit()


while(y):
    retVal, img= cam.read()
    if not retVal:
        print('image not received. Program quitting ...')
        y=False
    else:
        y = False
        print("Image received: Running tinyyolo")
        cmd = 'echo hello'
        print (subprocess.check_output(cmd,shell = True)



print('outside')
cam.release()
GPIO.cleanup()
cv2.destroyAllWindows()
quit()
