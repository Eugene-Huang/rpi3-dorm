# -*- coding: utf8 -*-

from flask import Flask, render_template
import MySQLdb
import time
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import db_info

app = Flask(__name__)


HOST, PORT, DATABASE, USERNAME, PASSWD = db_info()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/alltemp', methods=['GET'])
def get_all_tempperature():
    try:
        conn = MySQLdb.connect(
            host=HOST, port=PORT, user=USERNAME,
            passwd=PASSWD, db=DATABASE
        )
        cur = conn.cursor()
    except MySQLdb.Error as error:
        return error
    sql = 'SELECT * FROM (SELECT time, value FROM temperature ' + \
        'ORDER BY time DESC LIMIT 10) inverted ORDER BY time'
    cur.execute(sql)
    raws = list(cur.fetchall())
    if raws is None:
        return json.dumps([0, 0])
    conn.close()
    time_list = map(lambda x: time.mktime(x[0].timetuple()), raws)
    value_list = map(lambda x: float(x[1]), raws)
    data = [time_list, value_list]
    return json.dumps(data)


@app.route('/newtemp', methods=['GET'])
def get_new_temperature():
    try:
        conn = MySQLdb.connect(
            host=HOST, port=PORT, user=USERNAME,
            passwd=PASSWD, db=DATABASE
        )
        cur = conn.cursor()
    except MySQLdb.Error as error:
        return error
    sql = 'SELECT time, value FROM temperature ORDER BY ' + \
        'time DESC LIMIT 1'
    cur.execute(sql)
    raw = cur.fetchone()
    if raw is None:
        return json.dumps([0, 0])
    data = [time.mktime(raw[0].timetuple()), raw[1]]
    return json.dumps(data)


@app.route('/allhum', methods=['GET'])
def get_all_humidity():
    try:
        conn = MySQLdb.connect(
            host=HOST, port=PORT, user=USERNAME,
            passwd=PASSWD, db=DATABASE
        )
        cur = conn.cursor()
    except MySQLdb.Error as error:
        return error
    sql = 'SELECT * FROM (SELECT time, value FROM humidity ' + \
        'ORDER BY time DESC LIMIT 10) inverted ORDER BY time'
    cur.execute(sql)
    raws = list(cur.fetchall())
    if raws is None:
        return json.dumps([0, 0])
    conn.close()
    time_list = map(lambda x: time.mktime(x[0].timetuple()), raws)
    value_list = map(lambda x: float(x[1]), raws)
    data = [time_list, value_list]
    return json.dumps(data)


@app.route('/newhum', methods=['GET'])
def get_new_humidity():
    try:
        conn = MySQLdb.connect(
            host=HOST, port=PORT, user=USERNAME,
            passwd=PASSWD, db=DATABASE
        )
        cur = conn.cursor()
    except MySQLdb.Error as error:
        return error
    sql = 'SELECT time, value FROM humidity ORDER BY ' + \
        'time DESC LIMIT 1'
    cur.execute(sql)
    raw = cur.fetchone()
    if raw is None:
        return json.dumps([0, 0])
    data = [time.mktime(raw[0].timetuple()), raw[1]]
    return json.dumps(data)


if __name__ == '__main__':
    app.run()
