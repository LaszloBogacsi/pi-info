import datetime

from dateutil.relativedelta import relativedelta
from psycopg2.pool import SimpleConnectionPool

from applicationConfig import Config

database_config = Config.get_database_config()
get_pool = SimpleConnectionPool(1, 5,
                                host=database_config['host'],
                                database=database_config['database'],
                                user=database_config['user'],
                                password=database_config['password'])


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


def save(query):
    pool = get_pool
    conn = pool.getconn()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
        pool.putconn(conn)


def load_all(query, mapper):
    pool = get_pool
    conn = pool.getconn()
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
    pool = get_pool
    conn = pool.getconn()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        one = mapper(cursor.fetchone())
        cursor.close()
        pool.putconn(conn)
        return one
