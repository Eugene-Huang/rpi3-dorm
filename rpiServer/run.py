# -*- coding: utf8 -*-
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import MySQLdb
import time

# LCD screen
# Raspberry Pi pin configuration:
lcd_rs        = 14  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 15
lcd_d4        = 17
lcd_d5        = 18
lcd_d6        = 27
lcd_d7        = 22
lcd_backlight = 4

lcd_columns = 16
lcd_rows = 2

# DHT sensor
# data header: GPIO26 == PIN37
dht_gpio = 26

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4,
                           lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
while True:
	timecount = 0
    dht11 = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(dht11, dht_gpio)
    if humidity is not None and temperature is not None:
        lcd.clear()
        todaytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        msg =  time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))\
                    + '\n' + str(temperature) + ' C  ' + str(humidity) + '%'
        lcd.message(msg)
        print(msg)
    if timecount >= 60:
        timecount = 0
    time.sleep(60)
    timecount += 1
