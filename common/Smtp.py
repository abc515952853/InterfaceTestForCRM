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
        self.msg['from'] = readconfig.get_email('sendAddr')
        self.msg['to'] = readconfig.get_email('recipientAddrs')
        self.msg['subject'] = readconfig.get_email('subject')
        content = readconfig.get_email('content')
        txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
        self.msg.attach(txt)
        

    def add_accessory(self,accessoryfile):
        part = MIMEApplication(open(accessoryfile,'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=accessoryfile)
        self.msg.attach(part)

    def send_email(self,):
        smtpHost = readconfig.get_email('smtpHost')
        password = readconfig.get_email('password')
        print(smtpHost)
        smtp = smtplib.SMTP()
        smtp.connect(smtpHost, '25')
        smtp.login(self.msg['from'], password)
        smtp.sendmail(self.msg['from'], self.msg['to'], str(self.msg))
        print("邮件发送成功！")
        smtp.quit()
        
        
     
# def send_email(smtpHost, sendAddr, password, recipientAddrs, subject='', content=''):
#     msg = email.mime.multipart.MIMEMultipart()
#     msg['from'] = sendAddr
#     msg['to'] = recipientAddrs
#     msg['subject'] = subject
#     content = content
#     txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
#     msg.attach(txt)

#     # 添加附件，传送D:/软件/yasuo.rar文件
#     part = MIMEApplication(open('F:\PythonProject\InterfaceTestForQianketong\TextReport20181114161754.html','rb').read())
#     part.add_header('Content-Disposition', 'attachment', filename="TextReport20181113181737.html")
#     msg.attach(part)

#     smtp = smtplib.SMTP()
#     smtp.connect(smtpHost, '25')
#     smtp.login(sendAddr, password)
#     smtp.sendmail(sendAddr, recipientAddrs, str(msg))
#     print("邮件发送成功！")
#     smtp.quit()


# try:
#     subject = 'Python 测试邮件'
#     content = '这是一封来自 Python 编写的测试邮件。'
#     send_email('smtp.qq.com', '515952853@qq.com', 'lhenyaejzrlzbgcb', '515952853@qq.com', subject, content)
# except Exception as err:
#     print(err)  