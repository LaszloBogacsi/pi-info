from repository import get_pool

pool = get_pool
temp_id = 0


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
