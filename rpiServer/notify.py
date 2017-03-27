# -*- coding: utf8 -*-

from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import email_info


class QQEmail(object):
    def __init__(self, user, passwd):
        self.from_addr = user
        self.pwd = passwd

    def send(self, to_addr, subject, content):
        statu_info = 'Email sent successful'
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = formataddr(['rpi-server', self.from_addr])
            msg['To'] = formataddr(['Admin', to_addr])
            msg['Subject'] = Header(subject, 'utf-8')
            # 填写qq邮箱服务器地址
            sender = smtplib.SMTP('smtp.qq.com', 25)
            # [debug]查看邮件发送状态信息
            # sender.set_debuglevel(1)
            sender.ehlo()
            sender.starttls()
            sender.login(self.from_addr, self.pwd)
            sender.sendmail(self.from_addr, to_addr, msg.as_string())
            sender.quit()
        except smtplib.SMTPException as e:
            statu_info = '[BUG]sending eamil failed:', e
        print statu_info


if __name__ == '__main__':
    frm, to, authcode = email_info()
    sender = QQEmail(frm, authcode)
    subject = 'test'
    content = 'hello rpi sensor'
    sender.send(to, subject, content)
