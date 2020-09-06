import cv2
import RPi.GPIO as GPIO
from time import sleep
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_BUFFERSIZE,1)

for i in range(100):
    _,img = cam.read()
    #cl_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    cv2.imwrite('/home/pi/finalProj/CHZ_LAY/img'+str(i)+'.jpg',img)
    print('Get Ready')
    sleep(3)
