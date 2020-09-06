import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

#mail code
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

def mail(items,cost):
    msg = MIMEMultipart()
#message = message_template.substitute(PERSON_NAME=name.title())
    msg['From']= 'shopbot5725@gmail.com'
    msg['To'] = 'cea95@cornell.edu'
    msg['Subject']= "Your Order from SmartKart"

    total = sum(cost)
    lines = [None]*len(cost) #Array of strings per line 
    
    print(lines)
    for i in range(len(cost)):
        lines[i] = items[i] + ": $" + str(cost[i]) + "\n"
    
    print(lines)
    display = ''.join(lines)
    message = "Thank you for shopping with SmartKart. We have attached your receipt with the mail" +"\n"+ display
    msg.attach(MIMEText(message, 'plain'))
    #Next, log in to the server
    server.login("shopbot5725", "wifhuvbgimobchom")
    server.send_message(msg)
    del msg


#buttons
my_checkout={'CHECKOUT':(250,200)}
my_start={'START':(160,120)}

#GPIO mode setup
GPIO.setmode(GPIO.BCM)
cost_db = {'Banana':0.59,'Tomato':1,'Spoon':2}

# setup for log 
item_cost = {'Banana':0,'Tomato': 0,'Spoon': 0}
item_amt = {'Banana': 0, 'Tomato': 0, 'Spoon':0}

# arrays for items, quantity and cost
my_font_item_loc_array=pygame.font.Font(None,18)
item_loc_array = {'BANANA':(50,60), 'TOMATO':(50,80), 'SPOON':(50,100)}
item_quant_array = {(160,60):'0', (160,80):'0', (160,100):'0'}
item_cost_array = {(250,60):'0', (250,80):'0', (250,100):'0'}

# font setup for log display
total_items={(80,40):'List of items in your cart'}
quantity={(180,40):'Quantity'}
cost={(240,40):'Cost'}

#GPIO 27 callback function to end the program
def GPIO27_cb(channel):
    pygame.display.quit()
    GPIO.cleanup()
    server.quit()

#update function for list
def listUpdate(item_detected, q):
    global item_cost, item_amt
    if item_detected == banana:
        item_amt[banana] += 1
        item_cost[banana] += cost_db[banana]
    if item_detected == tomato:
        item_amt[tomato] += 1
        item_cost[tomato] += cost_db[tomato]
    if item_detected ==spoon:
        item_amt[spoon] += 1
        item_cost[spoon] += cost_db[spoon]    

#Add a function to update the display lists for items, costs and quantities

# GPIO 27 setup
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_cb)

#image setup for buttons
checkout_img= pygame.image.load("stop.png")
start_img = pygame.image.load("start.png")

checkout_rect = checkout_img.get_rect()
start_rect = start_img.get_rect()

checkout_rect= checkout_rect.move(100,60)
start_rect= start_rect.move(100,60)

screen.blit(start_img,start_rect)
#screen.blit(checkout_img,checkout_rect)

# button display
for my_text,text_pos in my_start.items():
    text_surface=my_font.render(my_text,True,WHITE)
    rect=text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)

pygame.display.flip()

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
    
    #screen.blit(start_img,start_rect)
    pygame.display.flip() 

    #Define x and y to get touch 
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            x,y=pos
            
            if 130<x<190 and 90<y<150: #start button has been pressed
                screen.fill(BLACK)
                b = True

    #if start button is pressed, then b = True
    # level 2
    while b:

        for my_text,text_pos in my_checkout.items():
            text_surface=my_font_item_loc_array.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect) 

        #logic for how to detect get information of the detected item
        #item_cost, item_amount = detect(item_cost, item_amt)

        #logic for updating position arrays

        #Display detected items
        for my_text, text_pos in item_loc_array.items():
            text_surface = my_font_item_loc_array.render(my_text,True,WHITE)
            rect = text_surface.get_rect(center = text_pos)
            screen.blit(text_surface,rect)

        # for number of items
        for text_pos, my_text in item_cost_array.items():
            text_surface = my_font_item_loc_array.render(my_text,True,WHITE)
            rect = text_surface.get_rect(center = text_pos)
            screen.blit(text_surface,rect)

        for text_pos, my_text in item_quant_array.items():
            text_surface = my_font_item_loc_array.render(my_text,True,WHITE)
            rect = text_surface.get_rect(center = text_pos)
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

        pygame.display.flip()

        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                pos=pygame.mouse.get_pos()
                u,v=pos
        #How to deal with detecting touch when not in the for loop (Does an event get detected even when not in the for loop)

        #checkout button has been pressed   
                if u>200 and v>160: 
                    screen.fill(BLACK)
            #Can have a thank you for shopping message displayed. Display it for a set time.sleep()
                    b = False
                    itemarray = list(item_cost.keys())
                    costarray = list(item_cost.values())
                    mail(itemarray,costarray)
        if not b:
            break

