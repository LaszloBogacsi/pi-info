import datetime
from dateutil.relativedelta import relativedelta
from pi_info.repository import get_db


def get_conn():
    pool = get_db()
    connection = pool.getconn()
    return pool, connection


def get_timerange_query(timerange):
    today = datetime.date.today()
    day = datetime.datetime.now() - datetime.timedelta(hours=24)
    week = today - datetime.timedelta(weeks=1)
    month = today - relativedelta(months=1)
    year = today - relativedelta(months=1)
    ranges = {
        "today": " AND published_time > '%s'" % str(day),
        "week": " AND published_time::date > '%s'" % str(week),
        "month": " AND published_time::date > '%s'" % str(month),
        "year": " AND published_time::date > '%s'" % str(year)
    }
    return ranges.get(timerange, "")


def save(query):
    pool, conn = get_conn()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        id = cursor.fetchone()[0]
        cursor.close()
        conn.commit()
        pool.putconn(conn)
        return id


def load_all(query, mapper):
    pool, conn = get_conn()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        all_raw_data = cursor.fetchall()
        list = []
        for raw_data in all_raw_data:
            list.append(mapper(raw_data))
        cursor.close()
        pool.putconn(conn)
        return list


def load_one(query, mapper):
    pool, conn = get_conn()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        one = mapper(cursor.fetchone())
        cursor.close()
        pool.putconn(conn)
        return one
