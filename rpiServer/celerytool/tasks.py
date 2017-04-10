#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from celery import app
from rpiServer import QQEmail
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import email_info

# 测试配置文件读取
print email_info()
frm, to, authcode = email_info()
# sender = QQEmail(frm, authcode)
# subject = '温湿度邮件通知'
# content = 'Hello， admin\nTemperature: 35 C\nHumidity: 90%'
# sender.send(to, subject, content)


@app.task
def obtainPM25(api_url, city, key):
    api_url = api_url
    city = city
    key = key
    params = {'city': city, 'key': key}
    res = requests.get(api_url, params=params)
    pm25 = res.json()['HeWeather5'][0]['aqi']['city']['pm25'].encode('utf8')
    with open('../pm25.txt') as f:
        f.write(pm25)
        f.close()
    # return int(pm25)


@app.task
def daily_notification(temperature, humidity, pm25):
    sender = QQEmail(frm, authcode)
    subject = '传感器数据通知'
    content = 'Morning, admin\nTemperature: {}℃\nHumidity: {}%\nPM2.5: {}'.format(
        temperature, humidity, pm25)
    sender.send(to, subject, content)


@app.task
def email_notification(temperature=None, humidity=None):
    sender = QQEmail(frm, authcode)
    subject = '传感器异常数据通知'
    content = 'Warning, admin\nTemperature: {}℃\nHumidity: {}%\n'.format(
        temperature, humidity)
    sender.send(to, subject, content)


if __name__ == '__main__':
    pass
