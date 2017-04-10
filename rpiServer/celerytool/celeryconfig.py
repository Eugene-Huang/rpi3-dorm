#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery.schedules import crontab
from datetime import timedelta
from run import read_dht11
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import heweather_info

# 和天气API
api_url, cityID, key = heweather_info()

temperature, humidity = read_dht11()


CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379//'
BROKER_URL = 'redis://127.0.0.1:6379//'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'add-every-30-minutes': {
        'task': 'tasks.obtainPM25',
        'schedule': timedelta(minutes=30),
        'args': (api_url, cityID, key),
    },
    'add-every-morning': {
        'task': 'tasks.daily_notification',
        'schedule': crontab(hour=6, minute=30),
        'agrs': (temperature, humidity)
    }
}
