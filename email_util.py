import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate, COMMASPACE
from email import encoders
import os

SERVER = 'smtp.gmail.com'
username = 'towpebsmtp2@gmail.com'
password = 'Gerr@rd4'
to_address = ['rolycg89@gmail.com']
subject = 'Report about Rooms usage'
PORT = 465

body = "Please find attached a summary for rooms usage in this month."
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (username, ", ".join(to_address), subject, body)

to_address_tmp = ['34E51Operations@sedescoinc.com']


# 'alex@kdtechnology.net'

def send_email_with_attachment(pdf, room):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = COMMASPACE.join(to_address)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = room

    msg.attach(MIMEText(message))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(pdf, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(pdf)))
    msg.attach(part)
    smtp = smtplib.SMTP_SSL(SERVER, PORT)
    smtp.login(username, password)
    smtp.sendmail(username, to_address_tmp, msg.as_string())
    smtp.sendmail(username, to_address, msg.as_string())
    smtp.quit()

# def send_mail():
#     server = smtplib.SMTP_SSL('smtp.gmail.com:465')
#     server.login(username, password)
#     server.sendmail(username, to_address, message)
#     server.quit()
