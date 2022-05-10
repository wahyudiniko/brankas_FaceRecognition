#!/usr/bin/python3

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


subject = "An intruder has been detected"
to = "wahyudiniko0@gmail.com"           # receiver email address
UserName = "raspipengirim1@gmail.com"   # sender e-mail address
UserPassword = "ihfpxvhrrjzuizlt"       # both sender and receiver e-mail address only works for gmail


def sendEmail(ImgFileName):
    print("Sending mail...")
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = UserName
    msg['To'] = to

    text = MIMEText("Here is an attached image of the intruder")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP("smtp.gmail.com:587")
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(UserName, UserPassword)
    s.sendmail(to, to, msg.as_string())
    print("Successfully sending an email. \n")
    s.quit()
