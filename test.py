import random
import time
import MySQLdb
from config import db_info


HOST, PORT, DATABASE, USERNAME, PASSWD = db_info()


try:
    conn = MySQLdb.connect(
        host=HOST, port=PORT, user=USERNAME,
        passwd=PASSWD, db=DATABASE
    )
    conn.autocommit(True)
    cur = conn.cursor()
except MySQLdb.Error as error:
    raise error
for x in xrange(0, 10):
    current_temperature = round(random.uniform(1, 30), 2)
    sql = 'INSERT INTO temperature(value) VALUES({value})'.format(value=current_temperature)
    sql_hum = 'INSERT INTO humidity(value) VALUES({value})'.format(value=current_temperature)
    print sql
    print sql_hum
    cur.execute(sql)
    cur.execute(sql_hum)
    time.sleep(3)

