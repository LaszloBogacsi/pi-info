from repository import get_pool

pool = get_pool


def save_humidity(humidity_data):
    conn = pool.getconn()
    if conn:
        print("successfully received connection from connection pool ")
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO humidity(humidity, status, sensor_location, published_time) VALUES (%s, %s, %s, %s)""",
            (humidity_data['humidity'], humidity_data['status'], humidity_data['sensor_location'], humidity_data['timestamp']))
        cursor.close()
        conn.commit()
        pool.putconn(conn)
        print("Put away a PostgreSQL connection")
