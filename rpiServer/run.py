# -*- coding: utf8 -*-
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import MySQLdb
import requests
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import db_info, email_info, heweather_info


# 和天气API
api_url, cityID, key = heweather_info()
# 数据库
HOST, PORT, DATABASE, USERNAME, PASSWD = db_info()
# DHT11 sensor
# data header: GPIO26 == PIN37
DHT11_GPIO = 26
# LCD screen
# Raspberry Pi pin configuration:
lcd_rs = 14
lcd_en = 15
lcd_d4 = 17
lcd_d5 = 18
lcd_d6 = 27
lcd_d7 = 22
lcd_backlight = 4

lcd_columns = 16
lcd_rows = 2


def db_connect(host, port, user, passwd, db):
    try:
        connect = MySQLdb.connect(
            host=host, port=port, user=user,
            passwd=passwd, db=db
        )
    except MySQLdb.Error as error:
        raise error
    return connect


def isconnect(connect):
    '''判断数据库连接是否因时间过长而断开
    断开返回False, 保持连接返回True
    ----------------------------------
    >>>isconnect(conn)
    >>>True
    '''
    conn = connect
    try:
        conn.ping()
        return True
    except MySQLdb.OperationError:
        return False
    except MySQLdb.InterfaceError:
        return False


def store2db(cursor, temperature, humidity):
    insert_temp = 'INSERT INTO temperature(value) VALUES({value})'.format(value=temperature)
    insert_hum = 'INSERT INTO humidity(value) VALUES({value})'.format(value=humidity)
    cur = cursor
    if cursor is not None:
        try:
            cur.execute(insert_temp)
            cur.execute(insert_hum)
        except MySQLdb.Error as e:
            raise e


def obtain_dht11(dht11, dht11_gpio):
    gpio = dht11_gpio
    dht = dht11
    humidity, temperature = Adafruit_DHT.read_retry(dht, gpio)
    if humidity is not None and temperature is not None:
        return [temperature, humidity]
    else:
        raise '[Error] Can not obtain DHT11 sensor data'


def displayLCD(lcd1602, temperature, humidity, pm25=None):
    temperature = temperature
    humidity = humidity
    pm25 = '0' if pm25 is None else str(pm25)
    lcd = lcd1602
    lcd.clear()
    first_info = time.strftime('%H:%M', time.localtime()) + ' PM25 ' + pm25
    second_data = '{0:0.1f} C   {1:0.1f}%'.format(humidity, temperature)
    msg = first_info + '\n' + second_data
    lcd.message(msg)
    print msg


def obtainPM25(api_url, city, key):
    api_url = api_url
    city = city
    key = key
    params = {'city': city, 'key': key}
    res = requests.get(api_url, params=params)
    pm25 = res.json()['HeWeather5'][0]['aqi']['city']['pm25'].encode('utf8')
    return int(pm25)


# Initialize the DHT11
dht11 = Adafruit_DHT.DHT11
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4,
                           lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# 建立数据库连接
conn = db_connect(HOST, PORT, USERNAME, PASSWD, DATABASE)
cur = conn.cursor()
conn.autocommit(True)

while True:
    humidity, temperature = obtain_dht11(dht11, DHT11_GPIO)
    displayLCD(lcd, temperature, humidity)
    if not isconnect(conn):
        conn = db_connect(HOST, PORT, USERNAME, PASSWD, DATABASE)
        cur = conn.cursor()
        conn.autocommit(True)
    store2db(cur, temperature, humidity)
    time.sleep(3)


if __name__ == '__main__':
    obtainPM25(api_url, cityID, key)
