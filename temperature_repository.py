import datetime
from dateutil.relativedelta import *
import psycopg2

from repository import get_pool

pool = get_pool


def save_temperature(temp_data):
    conn = pool.getconn()
    if conn:
        print("successfully received connection from connection pool ")
        cursor = conn.cursor()
        sql = """INSERT INTO temperature(temperature, status, sensor_id, published_time) VALUES (%s, %s, %s, %s)"""
        cursor.execute(
            sql, (temp_data['temperature'], temp_data['status'], temp_data['sensor_id'], temp_data['timestamp']))
        cursor.close()
        conn.commit()
        pool.putconn(conn)
        print("Put away a PostgreSQL connection")


def load_all_temperature():
    conn = pool.getconn()
    if conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM temperature ORDER BY published_time"
        cursor.execute(sql)
        all_temperature = cursor.fetchall()
        all_temp = []
        for temp in all_temperature:
            all_temp.append(cast_temperature(temp))

        cursor.close()
        pool.putconn(conn)
        return all_temp


def load_current_temperature():
    conn = pool.getconn()
    if conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM temperature ORDER BY published_time DESC LIMIT 1"
        cursor.execute(sql)
        current_temperature = cast_temperature(cursor.fetchone())
        cursor.close()
        pool.putconn(conn)
        return current_temperature


def get_timerange_query(timerange):
    today = datetime.date.today()
    week = today - datetime.timedelta(weeks=1)
    month = today - relativedelta(months=1)
    year = today - relativedelta(months=1)
    ranges = {
        "today": " AND published_time::date = '%s'" % str(today),
        "week": " AND published_time::date > '%s'" % str(week),
        "month": " AND published_time::date > '%s'" % str(month),
        "year": " AND published_time::date > '%s'" % str(year)
    }
    return ranges.get(timerange, "")


def load_temperature_for(sensor, timerange):
    conn = pool.getconn()
    timerange_query = get_timerange_query(timerange)
    if conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM temperature WHERE sensor_id=%s" + timerange_query
        cursor.execute(sql, (sensor["sensor_id"],))
        all_temperature = cursor.fetchall()
        all_temp = []
        for temp in all_temperature:
            all_temp.append(cast_temperature(temp))

        cursor.close()
        pool.putconn(conn)
        return all_temp


class Temperature(object):
    def __init__(self, id, temperature, sensor_status, published_time, sensor_id):
        self.published_time = published_time
        self.sensor_id = sensor_id
        self.sensor_status = sensor_status
        self.temperature = temperature
        self.id = id


def cast_temperature(value):
    if value is None:
        return None
    return Temperature(id=value[0], temperature=value[1], sensor_status=value[2], published_time=value[3], sensor_id=value[4])