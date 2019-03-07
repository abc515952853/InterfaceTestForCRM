#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ReadConfig 

readconfig=ReadConfig.ReadConfig()

class Smtp:
    def __init__(self,):
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['from'] = readconfig.get_basedata('email_sendaddr')
        self.msg['to'] = readconfig.get_basedata('email_recipientaddrs')
        self.msg['subject'] = readconfig.get_basedata('email_subject')
        content = readconfig.get_basedata('email_content')
        txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
        self.msg.attach(txt)
        

    def add_accessory(self,accessoryfile):
        part = MIMEApplication(open(accessoryfile,'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=accessoryfile)
        self.msg.attach(part)

    def send_email(self,):
        smtpHost = readconfig.get_basedata('email_smtphost')
        password = readconfig.get_basedata('email_password')
        print(smtpHost)
        smtp = smtplib.SMTP()
        smtp.connect(smtpHost, '25')
        smtp.login(self.msg['from'], password)
        smtp.sendmail(self.msg['from'], self.msg['to'], str(self.msg))
        print("邮件发送成功！")
        smtp.quit()
        
        
      