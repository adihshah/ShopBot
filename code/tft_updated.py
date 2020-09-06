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

def detectobject(test_image, haar_cascade):
     #test_image = cv2.imread('lays2.jpg')
     #print(test_image.shape)
     test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

     faces_rects = haar_cascade.detectMultiScale(test_image_gray)

     #print('Objects found: ', len(faces_rects))
     return True if len(faces_rects)>0 else False

     #for x,y,w,h in faces_rects:
     #     cv2.rectangle(test_image, (x, y), (x+w, y+h), (0, 0, 255), 10)

     #plt.imshow(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
     #plt.show()

def sift(img2, img1):
     #reading image
     #img1 = cv2.imread('lays1.jpg')
     #img2 = cv2.imread('lays2.jpg')

     img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
     img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

     #sift
     sift = cv2.xfeatures2d.SIFT_create()

     keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
     keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

     FLANN_INDEX_KDTREE = 0
     #descriptors_1 = np.float32(descriptors_1)
     #descriptors_2 = np.float32(descriptors_2)
     index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
     search_params = dict(checks=50)   # or pass empty dictionary

     flann = cv2.FlannBasedMatcher(index_params,search_params)

     matches = flann.knnMatch(descriptors_1,descriptors_2,k=2)

     # Need to draw only good matches, so create a mask
     matchesMask = [[0,0] for i in range(len(matches))]
     count = 0
     # ratio test as per Lowe's paper
     for i,(m,n) in enumerate(matches):
          if m.distance < 0.7*n.distance:
               count +=1
               matchesMask[i]=[1,0]

     draw_params = dict(matchColor = (0,255,0),
                    singlePointColor = (255,0,0),
                    matchesMask = matchesMask,
                    flags = 0)

     #img3 = cv2.drawMatchesKnn(img1,keypoints_1,img2,keypoints_2,matches,None,**draw_params)
     #print(len(matches))
     #print(count)
     #if count >= 10:
     #     print("Detected Lays")
     #plt.imshow(img3,),plt.show()
     return count

def lays(test_image):
    haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/Lays_classifier.xml')
    #benchmark = cv2.imread('/home/pi/finalProj/image/lays1.jpg')

    #sift_true = True if sift(test_image,benchmark) >= 12 else False
    #return sift_true
    return detectobject(test_image, haar_cascade)

'''def vaseline(test_image):
    haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/vaseline_classifier.xml')
    benchmark = cv2.imread('/home/pi/finalProj/image/vaseline.jpg')
    print(test_image.shape)
    sift_true = True if sift(test_image,benchmark) >= 100 else False
    return detectobject(test_image, haar_cascade) or sift_true'''

def kellogs(test_image):
    #haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/kellogs_classifier.xml')
    benchmark = cv2.imread('/home/pi/finalProj/image/kellogs.png')

    sift_true = True if sift(test_image,benchmark) >= 12 else False
    return sift_true
    #return detectobject(test_image, haar_cascade) or sift_true

def kitkat(test_image):
    haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/kitkat_classifier.xml')
    benchmark = cv2.imread('/home/pi/finalProj/image/kitkat.jpg')

    sift_true = True if sift(test_image,benchmark) >= 12 else False
    #return sift_true
    return detectobject(test_image, haar_cascade) or sift_true

def cheetos(test_image):
    haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/cheetos_classifier.xml')
    benchmark = cv2.imread('/home/pi/finalProj/image/cheetos.jpg')

    sift_true = True if sift(test_image,benchmark) >= 12 else False
    return detectobject(test_image, haar_cascade) or sift_true
    #return sift_true
    
'''def pepsi(test_image):
    haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/pepsi_classifier.xml')
    benchmark = cv2.imread('/home/pi/finalProj/image/pepsi.jpg')

    sift_true = True if sift(test_image,benchmark) >= 100 else False
    return detectobject(test_image, haar_cascade) or sift_true'''

def clif(test_image):
    #haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/clif_classifier.xml')
    benchmark = cv2.imread('/home/pi/finalProj/image/clif-logo.jpg')

    sift_true = True if sift(test_image,benchmark) >= 22 else False
    return sift_true
    #return detectobject(test_image, haar_cascade) or sift_true

def clorox(test_image):
    haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/Clorox_classifier.xml')
    #benchmark = cv2.imread('/home/pi/finalProj/image/clorox.jpg')

    #sift_true = True if sift(test_image,benchmark) >= 12 else False
    #return sift_true
    return detectobject(test_image, haar_cascade)

'''def stonyfield(test_image):
    haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/StoneyField_classifier.xml')
    benchmark = cv2.imread('/home/pi/finalProj/image/lays1.jpg')

    sift_true = True if sift(test_image,benchmark) >= 50 else False
    return detectobject(test_image, haar_cascade) or sift_true'''

#mail code

def mail(items,cost, quantity):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    msg = MIMEMultipart()
#message = message_template.substitute(PERSON_NAME=name.title())
    msg['From']= 'shopbot5725@gmail.com'
    msg['To'] = 'cea95@cornell.edu'
    msg['Subject']= "Your Order from SmartKart"

    total = sum(cost)
    lines = [None]*len(cost) #Array of strings per line

    print(lines)
    for i in range(len(cost)):
        lines[i] = items[i] + "\t   $" + str(cost[i]) + "\t   Quantity: " + str(quantity[i]) + "\n"


    summary = '\n\n********************************\n'+'Total: $' + f'{total: .2f}' +'\tTotal Items purchased: ' + str(sum(quantity)) +'\n\nCome shop with shopbot gain soon. Have a wonderful day!'

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

# setup for log
#item_cost =  {'Lays':0,'Oreos':0,'Kellogs':0, 'Kitkat':0,'Cheetos':0, 'Lactaid': 0, 'Clif': 0, 'Clorox': 0, 'Tropicana': 0}
#item_amt =  {'Lays':0,'Oreos':0,'Kellogs':0, 'Kitkat':0,'Cheetos':0, 'Lactaid': 0, 'Clif': 0, 'Clorox': 0, 'Tropicana': 0}


# arrays for items, quantity and cost
my_font_item_loc_array=pygame.font.Font(None,18)

#item_loc_array = {'Lays':(50,60), 'Oreos':(50,80), 'Kellogs':(50,100), 'Kitkat':(50,120), 'Cheetos':(50,160), 'Lactaid':(50,180), 'Clif':(50,200), 'Clorox':(50,220), 'Tropicana':(50,230) }
#item_quant_array = {(160,60):'0', (160,80):'0', (160,100):'0'}
#item_cost_array = {(250,60):'0', (250,80):'0', (250,100):'0'}

# font setup for log display
total_items={(80,40):'List of items in your cart'}
quantity={(180,40):'Quantity'}
cost={(240,40):'Cost'}

#GPIO 27 callback function to end the program
def GPIO27_cb(channel):
    screen.fill(BLACK)
    pygame.display.quit()
    GPIO.cleanup()

#update function for list
def listUpdate(items, item_amt, item_cost):
    global cost_db
    if 'Lays' in items:
        item_amt['Lays'] += 1
        item_cost['Lays'] += cost_db['Lays']
    if 'Kellogs' in items:
        item_amt['Kellogs'] += 1
        item_cost['Kellogs'] += cost_db['Kellogs']
    if 'Kitkat' in items:
        item_amt['Kitkat'] += 1
        item_cost['Kitkat'] += cost_db['Kitkat']
    if 'Cheetos' in items:
        item_amt['Cheetos'] += 1
        item_cost['Cheetos'] += cost_db['Cheetos']
    if 'Clif' in items:
        item_amt['Clif'] += 1
        item_cost['Clif'] += cost_db['Clif']
    if 'Clorox' in items:
        item_amt['Clorox'] += 1
        item_cost['Clorox'] += cost_db['Clorox']

#alays = [0,0,0,0]
#akellogs = [0,0,0,0]
#akitkat = [0,0,0,0]
#acheetos = [0,0,0,0]
#aclif = [0,0,0,0]
#aclorox = [0,0,0,0]

# GPIO 27 setup
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_cb)

#image setup for buttons
#checkout_img= pygame.image.load("/home/pi/image/stop.png")
start_img = pygame.image.load("/home/pi/finalProj/image/start.png")

#checkout_rect = checkout_img.get_rect()
start_rect = start_img.get_rect(center = (160,120))

#checkout_rect= checkout_rect.move(100,60)
#start_rect= start_rect.move(100,60)

#screen.blit(start_img,start_rect)
#screen.blit(checkout_img,checkout_rect)

# button display
#for my_text,text_pos in my_start.items():
    #text_surface=my_font.render(my_text,True,WHITE)
    #rect=text_surface.get_rect(center=text_pos)
    #screen.blit(text_surface,rect)

#pygame.display.flip()

a = True  #to run level 1
b = False #for level 2
items_detected= dict()
item_cost = defaultdict(int)  
item_amt = defaultdict(int)

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
                    text_surface=my_font_item_loc_array.render(my_text,True,WHITE)
                    rect=text_surface.get_rect(center=text_pos)
                    screen.blit(text_surface,rect)

                for text_pos, my_text in total_items.items():
                    text_surface = my_font_item_loc_array.render(my_text,True,WHITE)
                    rect = text_surface.get_rect(center = text_pos)
                    screen.blit(text_surface,rect)

                for text_pos, my_text in quantity.items():
                    text_surface = my_font_item_loc_array.render(my_text,True,WHITE)
                    rect = text_surface.get_rect(center = text_pos)
                    screen.blit(text_surface,rect)

                for text_pos, my_text in cost.items():
                    text_surface = my_font_item_loc_array.render(my_text,True,WHITE)
                    rect = text_surface.get_rect(center = text_pos)
                    screen.blit(text_surface,rect)
                b = True

    #if start button is pressed, then b = True
    # level 2

    while b:
        # Fill black on half of the page
        screen.fill(BLACK,rect=(0,50,320,140))
        #logic for how to detect get information of the detected item
        #item_cost, item_amount = detect(item_cost, item_amt)
        

        #print('checking detection')
        #flash items detected
        item_cost = defaultdict(int)  
        item_amt = defaultdict(int)
        items_detected = dict()

        val, test_img = cam.read()
        if not val:
            print('No image captured')
        else:
            if lays(test_img):
                items_detected['Lays'] = 1
            if kellogs(test_img):
                items_detected['Kellogs'] = 1
            if kitkat(test_img):
                items_detected['Kitkat']= 1
            if cheetos(test_img):
                items_detected['Cheetos'] = 1
            if clorox(test_img):
                items_detected['Clorox'] = 1
            if clif(test_img):
                items_detected['Clif'] = 1
                    
            #Get newly detected items for display
            #item_cost = defaultdict(int)
            #item_amt = defaultdict(int)
            listUpdate(items_detected, item_amt, item_cost)

        y = 60
        for key,value in item_cost.items():
            item_text = my_font_item_loc_array.render(key,True,WHITE)
            item_rect = item_text.get_rect(center=(50,y))
            cost_text = my_font_item_loc_array.render(str(value),True,WHITE)
            cost_rect = cost_text.get_rect(center = (250,y))
            quant_text = my_font_item_loc_array.render(str(item_amt[key]),True,WHITE)
            quant_rect = quant_text.get_rect(center=(160,y))
            screen.blit(item_text,item_rect)
            screen.blit(cost_text,cost_rect)
            screen.blit(quant_text,quant_rect)
            y+=20

        pygame.display.flip()
        

        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                pos=pygame.mouse.get_pos()
                u,v=pos
                #checkout button has been pressed
                if u>200 and v>160:
                    screen.fill(BLACK)
                    b = False
                    itemarray = list(item_cost.keys())
                    costarray = list(item_cost.values())
                    quantityarray = list(item_amt.values())
                    mail(itemarray,costarray, quantityarray)
    
