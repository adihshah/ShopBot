#this file is to test the RPi camera

from picamera import  PiCamera
from time import sleep

cam = PiCamera()

cam.start_preview(fullscreen=False, window = (180,200,320,240))

sleep(100)

cam.stop_preview()


  
