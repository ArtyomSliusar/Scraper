#!/usr/bin/env python3

import os
import smtplib
from email.mime.text import MIMEText


CURRENT_PATH = os.path.dirname(__file__)


class MailSender(object):

    def __init__(self, sender: str, recipients: list, subject: str, buf_data, mime_type:str):
        self.sender = sender
        self.recipients = recipients
        self.subject = subject
        self.mime_type = mime_type
        if isinstance(buf_data, list):
            self.data = "".join(buf_data)
        elif isinstance(buf_data, str):
            self.data = buf_data
        else:
            TypeError("Data type: '{}' is not supported!".format(type(buf_data)))
        self.msg = MIMEText(self.data, self.mime_type)
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.sender
        self.msg['To'] = ", ".join(self.recipients)

    def get_sercet_info(self):
        print("Getting password ...")
        file_path = CURRENT_PATH + "/secret_info.txt"
        with open(file_path) as f:
            secret_info = f.read().split()
            password = secret_info[0]
        return password

    def send(self):
        password = self.get_sercet_info()
        print("Sending email to:", self.recipients)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('ScraperWorker@gmail.com', password)
        server.sendmail(self.sender, self.recipients, self.msg.as_string())
        server.quit()
        print("Email sent.")
