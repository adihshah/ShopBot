import cv2
import RPi.GPIO as GPIO
import numpy as np


#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# gets video feed from the pi camera
cam = cv2.VideoCapture(0)
#model to detect object
det_tom = cv2.CascadeClassifier('/home/pi/Downloads/tomato_classifier.xml')
det_tom1 = cv2.CascadeClassifier('/home/pi/Downloads/classifiers/detection/cascade.xml')
det_ban = cv2.CascadeClassifier('/home/pi/Downloads/classifiers/detection/cascade_1.xml')
#det_eye = cv2.CascadeClassifier('/tmp/opencv-master/data/haarcascades/haarcascade_eye.xml')

y = True #program runs if true

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


while(y):
    retVal, img= cam.read()
    if not retVal:
        print('image not received. Program quitting ...')
        y=False

    else:
        cv2.namedWindow('Shopping', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Shopping', 320, 300)
        #img_res = cv2.resize(img, (100,100))

        #convert image to gray scale for detection
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray_img_rs = cv2.resize(gray_img,(100,100))
        #detect img here
        eye_dec = det_ban.detectMultiScale(gray_img_rs, 1.5,3)

        #display a rectangle around the detected object
        for (x,y,w,h) in eye_dec:
            cv2.rectangle(img, (x,y),(x+w,y+h),(255,100,0),2)

        cv2.imshow('Shopping', img)
        cv2.waitKey(30) 


print('outside')
cam.release()
GPIO.cleanup()
cv2.destroyAllWindows()
quit()
