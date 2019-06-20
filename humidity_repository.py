from repository import get_pool

pool = get_pool


def save_humidity(humidity_data):
    conn = pool.getconn()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO humidity(humidity, status, sensor_id, published_time) VALUES (%s, %s, %s, %s)""",
            (humidity_data['humidity'], humidity_data['status'], humidity_data['sensor_id'], humidity_data['timestamp']))
        cursor.close()
        conn.commit()
        pool.putconn(conn)
