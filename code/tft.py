import RPi.GPIO as GPIO
import time
import numpy as np
import pygame
from pygame.locals import *
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import defaultdict
import concurrent.futures as cf

# display on pitft

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)

#color
WHITE = 255,255,255
BLACK= 0,0,0

#display setup
screen=pygame.display.set_mode((320,240))
my_font=pygame.font.Font(None,26)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_BUFFERSIZE,1)

def detectobject(name,test_image, haar_cascade):
     test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
     faces_rects = haar_cascade.detectMultiScale(test_image_gray)
     #print(f'{name}: Objects detected {len(faces_rects)}')
     return True if len(faces_rects)>0 else False

def sift(name,img2, img1, thresh):
     img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
     img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

     #sift
     sift = cv2.xfeatures2d.SIFT_create()
     keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
     keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

     FLANN_INDEX_KDTREE = 0
     index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
     search_params = dict(checks=50)   # or pass empty dictionary

     flann = cv2.FlannBasedMatcher(index_params,search_params)
     matches = flann.knnMatch(descriptors_1,descriptors_2,k=2)

     # Need to draw only good matches, so create a mask
     matchesMask = [[0,0] for i in range(len(matches))]
     count = 0
     #print(f'{name}: Matches are {len(matches)}')
     retval = False
     # ratio test as per Lowe's paper
     for i,(m,n) in enumerate(matches):
          if m.distance < 0.7*n.distance:
               count +=1
               matchesMask[i]=[1,0]
     print(f'{name}: Count is {count}')

     if count>=thresh:
         retval = True

     return retval

def object_detector(name):
    test_image = cv2.imread('/home/pi/finalProj/test_img.jpg')

    if name =='Lays':
        lays_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/Lays_classifier.xml')
        benchmark = cv2.imread('/home/pi/finalProj/image/lays1.jpg')
        n='Lays'
        sift_true = sift(n,test_image,benchmark,12)
        return detectobject(n,test_image, lays_clf) or sift_true

    elif name=='Kellogs':
        benchmark = cv2.imread('/home/pi/finalProj/image/kellogs.png')
        n='Kellogs'
        return sift(n,test_image,benchmark,12)

    elif name=='Kitkat':
        kitkat_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/kitkat_classifier.xml')
        benchmark = cv2.imread('/home/pi/finalProj/image/kitkat.jpg')
        n = 'kitkat'
        sift_true = sift(n,test_image,benchmark,12)
        return detectobject(n,test_image, kitkat_clf) or sift_true

    elif name=='Cheetos':
        cheetos_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/cheetos_classifier.xml')
        benchmark = cv2.imread('/home/pi/finalProj/image/cheetos.jpg')
        n = 'cheetos'
        sift_true = sift(n,test_image,benchmark,12)
        return detectobject(n,test_image, cheetos_clf) or sift_true

    elif name=='Clif':
        n = 'Clif'
        benchmark = cv2.imread('/home/pi/finalProj/image/clif-logo.jpg')
        return sift(n,test_image,benchmark,35)

    elif name=='Clorox':
        clorox_clf= cv2.CascadeClassifier('/home/pi/finalProj/Cascades/Clorox_classifier.xml')
        n ='Clorox'
        #benchmark = cv2.imread('/home/pi/finalProj/image/clorox.jpg')
        #sift_true = sift(n,test_image, benchmark,35)
        return detectobject(n,test_image, clorox_clf)


#mail code

def mail(items,cost, quantity):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    msg = MIMEMultipart()
#message = message_template.substitute(PERSON_NAME=name.title())
    msg['From']= 'shopbot5725@gmail.com'
    msg['To'] = 'as2564@cornell.edu'
    msg['Subject']= "Your Order from SmartKart"

    total = sum(cost)
    lines = [None]*len(cost) #Array of strings per line

    print(lines)
    for i in range(len(cost)):
        lines[i] = items[i] + "\t   $" + str(cost[i]) + "\t   Quantity: " + str(quantity[i]) + "\n"


    summary = '\n\n********************************\n'+'Total: $' + f'{total: .2f}' +'\tTotal Items purchased: ' + str(sum(quantity)) +'\n\nCome shop with shopbot again soon. Have a wonderful day!'

    print(lines)
    display = ''.join(lines)
    message = "Thank you for shopping with SmartKart. We have attached your receipt with the mail" +"\n\n"+ display + summary
    msg.attach(MIMEText(message, 'plain'))
    #Next, log in to the server
    server.login("shopbot5725", "wifhuvbgimobchom")
    server.send_message(msg)
    del msg
    server.quit()


#buttons
my_checkout={'CHECKOUT':(250,220)}
my_start={'START':(160,120)}

#GPIO mode setup
GPIO.setmode(GPIO.BCM)
cost_db = {'Lays':2.79,'Kellogs':3.19, 'Kitkat':3.79,'Cheetos':4.49, 'Clif': 5.99, 'Clorox': 4.48}


# arrays for items, quantity and cost
my_font_item =pygame.font.Font(None,18)

# font setup for log display
total_items={(80,40):'List of items in your cart'}
quantity={(180,40):'Quantity'}
cost={(240,40):'Cost'}

#GPIO 27 callback function to end the program
def GPIO27_cb(channel):
    screen.fill(BLACK)
    pygame.display.quit()
    GPIO.cleanup()

# GPIO 27 setup
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_cb)

#image setup for buttons
start_img = pygame.image.load("/home/pi/finalProj/image/start.png")
start_rect = start_img.get_rect(center = (160,120))


a = True  #to run level 1
b = False #for level 2

while a:
# in level 1
    screen.fill(BLACK)
    screen.blit(start_img,start_rect)

    for my_text,text_pos in my_start.items():
        text_surface=my_font.render(my_text,True,WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)

    pygame.display.flip()

    #Define x and y to get touch
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            x,y=pos
            if 120<x<190 and 90<y<150: #start button has been pressed
                screen.fill(BLACK)

                for my_text,text_pos in my_checkout.items():
                    text_surface=my_font_item.render(my_text,True,WHITE)
                    rect=text_surface.get_rect(center=text_pos)
                    screen.blit(text_surface,rect)

                for text_pos, my_text in total_items.items():
                    text_surface = my_font_item.render(my_text,True,WHITE)
                    rect = text_surface.get_rect(center = text_pos)
                    screen.blit(text_surface,rect)

                for text_pos, my_text in quantity.items():
                    text_surface = my_font_item.render(my_text,True,WHITE)
                    rect = text_surface.get_rect(center = text_pos)
                    screen.blit(text_surface,rect)

                for text_pos, my_text in cost.items():
                    text_surface = my_font_item.render(my_text,True,WHITE)
                    rect = text_surface.get_rect(center = text_pos)
                    screen.blit(text_surface,rect)

                pygame.display.flip()

                b = True

    #if start button is pressed, then b = True
    # level 2
    alays = [0,0,0,0]
    akellogs = [0,0,0,0]
    akitkat = [0,0,0,0]
    acheetos = [0,0,0,0]
    aclif = [0,0,0,0]
    aclorox = [0,0,0,0]
    while b:
        # Fill black on half of the page
        screen.fill(BLACK,rect=(0,50,320,140))
        
        #flash items detected
        item_cost = defaultdict(int)  
        item_amt = defaultdict(int)

        val, test_img = cam.read()
        if not val:
            print('No image captured')
        else:
            cv2.imwrite('/home/pi/finalProj/test_img.jpg',test_img)
            item_list = list(cost_db.keys())

            #create Multiprocessing
            with cf.ProcessPoolExecutor() as executor:
                f0= executor.submit(object_detector,item_list[0])
                f1= executor.submit(object_detector,item_list[1])
                f2= executor.submit(object_detector,item_list[2])
                f3= executor.submit(object_detector,item_list[3])
                f4= executor.submit(object_detector,item_list[4])
                f5= executor.submit(object_detector,item_list[5])
                
                f= [f0.result(),f1.result(),f2.result(),f3.result(),f4.result(),f5.result()]
                #print(f)
                '''for idx,item in enumerate(item_list):
                    if f[idx]:
                        item_amt[item] = 1
                        item_cost[item] = cost_db[item]'''
                print("Printing Most Recent Detections")
                print("Lays: " + str(alays))
                print("Kellogs "+ str(akellogs))
                print("Kitkat "+ str(akitkat))
                print("Cheetos " + str(acheetos))
                print("Clif " + str(aclif))
                print("Clorox " + str(aclorox))
                print()

                if sum(alays) >=2:
                    item_amt['Lays'] = 1
                    item_cost['Lays'] = cost_db['Lays']

                if sum(akellogs) >=2:
                    item_amt['Kellogs'] = 1
                    item_cost['Kellogs'] = cost_db['Kellogs']

                if sum(akitkat) >=2:
                    item_amt['Kitkat'] = 1
                    item_cost['Kitkat'] = cost_db['Kitkat']

                if sum(acheetos) >=2:
                    item_amt['Cheetos'] = 1
                    item_cost['Cheetos'] = cost_db['Cheetos']

                if sum(aclif) >=2:
                    item_amt['Clif'] = 1
                    item_cost['Clif'] = cost_db['Clif']

                if sum(aclorox) >=2:
                    item_amt['Clorox'] = 1
                    item_cost['Clorox'] = cost_db['Clorox']



                if f[0]:
                    alays.append(1)
                else:
                    alays.append(0)
                
                if f[1]:
                    akellogs.append(1)
                else:
                    akellogs.append(0)
               
                if f[2]:
                    akitkat.append(1)
                else:
                    akitkat.append(0)
                
                if f[3]:
                    acheetos.append(1)
                else:
                    acheetos.append(0)
                
                if f[4]:
                    aclif.append(1)
                else:
                    aclif.append(0)
                
                if f[5]:
                    aclorox.append(1)
                else:
                    aclorox.append(0)
                
                alays.pop(0)
                akellogs.pop(0)
                akitkat.pop(0)
                acheetos.pop(0)
                aclif.pop(0)
                aclorox.pop(0)

            #Print on tft screen
            y = 60
            for key,value in item_cost.items():
                item_text = my_font_item.render(key,True,WHITE)
                item_rect = item_text.get_rect(center=(50,y))
                cost_text = my_font_item.render(str(value),True,WHITE)
                cost_rect = cost_text.get_rect(center = (250,y))
                quant_text = my_font_item.render(str(item_amt[key]),True,WHITE)
                quant_rect = quant_text.get_rect(center=(160,y))
                screen.blit(item_text,item_rect)
                screen.blit(cost_text,cost_rect)
                screen.blit(quant_text,quant_rect)
                y+=20

        pygame.display.flip()

        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                u,v=pygame.mouse.get_pos()

                #checkout button has been pressed
                if u>200 and v>160:
                    screen.fill(BLACK)
                    b = False
                    itemarray = list(item_cost.keys())
                    costarray = list(item_cost.values())
                    quantarray = list(item_amt.values())
                    mail(itemarray,costarray, quantarray)
    
