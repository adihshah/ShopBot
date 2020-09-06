import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



server = smtplib.SMTP('smtp.gmail.com', 587)


def mail(items, cost):
    server.starttls()
    msg = MIMEMultipart()
    #message = message_template.substitute(PERSON_NAME=name.title())
    msg['From']= 'shopbot5725@gmail.com'
    msg['To'] = 'cea95@cornell.edu'
    msg['Subject']= "Your Order from SmartKart"

    total = sum(cost)

    lines = [None]*len(cost) #Array of strings per line 
    for i in range(len(cost)):
        lines[i] = items[i] + ": $" + str(cost[i]) + "\n"

    display = ''.join(lines)
    message = "Thank you for shopping with SmartKart. We have attached your receipt below\n" + display + "\n" +  "Your total is $" + str(total)
    print(display)
    msg.attach(MIMEText(message, 'plain'))

    #Next, log in to the server
    server.login("shopbot5725", "wifhuvbgimobchom")
    
    server.send_message(msg)
    del msg
    server.quit()

items = ['Banana', 'Spoon', 'Apple']
cost = [0.99, 1.00, 0.50]
mail(items,cost)
