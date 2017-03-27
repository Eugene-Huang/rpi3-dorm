# -*- coding: utf8 -*-
# filename: config.py
# -----------------------
# 运行该脚本建立数据表
# $ python config.py
# -----------------------
from ConfigParser import ConfigParser as cf
import MySQLdb
import ConfigParser
import os


def db_info():
    cfgpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini')
    config = cf()
    try:
        config.read(cfgpath)
        host = config.get('database', 'host')
        port = config.getint('database', 'port')
        database = config.get('database', 'dbname')
        username = config.get('database', 'username')
        password = config.get('database', 'password')
    except ConfigParser.Error as e:
        print '[CONFIG ERROR]parsing cfg file: ', e
    else:
        return [host, port, database, username,
                password]


def email_info():
    cfgpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini')
    config = cf()
    try:
        config.read(cfgpath)
        login_adr = config.get('email', 'login_adr')
        admin_addr = config.getint('email', 'admin_addr')
        authcode = config.get('email', 'authcode')
    except ConfigParser.Error as e:
        print '[CONFIG ERROR]parsing cfg file: ', e
    else:
        return [login_adr, admin_addr, authcode]


def heweather_info():
    cfgpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini')
    config = cf()
    try:
        config.read(cfgpath)
        key = config.get('heweather', 'key')
        api_url = config.get('heweather', 'api_url')
        cityID = config.get('heweather', 'cityID')
    except ConfigParser.Error as e:
        print '[CONFIG ERROR]parsing cfg file: ', e
    else:
        return [api_url, cityID, key]


def init_db():
    HOST, PORT, DATABASE, USERNAME, PASSWD = db_info()
    sql_temperature = '''
    CREATE TABLE IF NOT EXISTS temperature
    (
    id INT NOT NULL AUTO_INCREMENT,
    value FLOAT NOT NULL,
    time TIMESTAMP,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB
    '''
    sql_humidity = '''
    CREATE TABLE IF NOT EXISTS humidity
    (
    id INT NOT NULL AUTO_INCREMENT,
    value FLOAT NOT NULL,
    time TIMESTAMP,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB
    '''

    try:
        conn = MySQLdb.connect(
            host=HOST, port=PORT, user=USERNAME,
            passwd=PASSWD, db=DATABASE
        )
        cur = conn.cursor()
    except MySQLdb.Error as error:
        raise error
    else:
        cur.execute(sql_temperature)
        cur.execute(sql_humidity)
        conn.close()


if __name__ == '__main__':
    init_db()
    # print db_info()
