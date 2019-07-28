import datetime

from dateutil.relativedelta import relativedelta
from psycopg2.pool import SimpleConnectionPool

from pi_info.application_config import Config


def create_connection_pool(config) -> SimpleConnectionPool:
    return SimpleConnectionPool(1, 5,
                                host=config.host,
                                database=config.database,
                                user=config.username,
                                password=config.password)


pool = create_connection_pool(Config.get_database_config())


def get_connection(pool) :
    return pool.getconn()


def get_conn():
    return get_connection(pool)


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
    conn = get_conn()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
        pool.putconn(conn)


def load_all(query, mapper):
    conn = get_conn()
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
    conn = get_conn()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        one = mapper(cursor.fetchone())
        cursor.close()
        pool.putconn(conn)
        return one
