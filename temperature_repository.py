import psycopg2

from repository import get_pool

pool = get_pool


def save_temperature(temp_data):
    conn = pool.getconn()
    if conn:
        print("successfully received connection from connection pool ")
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO temperature(temperature, status, sensor_location, published_time) VALUES (%s, %s, %s, %s)""",
            (temp_data['temperature'], temp_data['status'], temp_data['sensor_location'], temp_data['timestamp']))
        cursor.close()
        conn.commit()
        pool.putconn(conn)
        print("Put away a PostgreSQL connection")


def load_all_temperature():
    conn = pool.getconn()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM temperature")
        all_temperature = cursor.fetchall()
        all_temp = []
        for temp in all_temperature:
            all_temp.append(cast_temperature(temp))

        cursor.close()
        pool.putconn(conn)
        print("Put away a PostgreSQL connection")
        return all_temp


def load_current_temperature():
    conn = pool.getconn()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM temperature ORDER BY published_time DESC LIMIT 1")
        current_temperature = cast_temperature(cursor.fetchone())
        cursor.close()
        pool.putconn(conn)
        print("Put away a PostgreSQL connection")
        return current_temperature


class Temperature(object):
    def __init__(self, id, temperature, sensor_status, sensor_location, published_time):
        self.published_time = published_time
        self.sensor_location = sensor_location
        self.sensor_status = sensor_status
        self.temperature = temperature
        self.id = id


def cast_temperature(value):
    if value is None:
        return None
    return Temperature(value[0], value[1], value[2], value[3], value[4])