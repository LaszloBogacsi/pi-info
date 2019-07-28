from pi_info.application_config import Config
Config('../config_dev.ini')
import random
import unittest
from datetime import datetime, timedelta
import psycopg2
from pi_info.repository.sensor_data_repository import save_sensor_data


class SensorDataGeneratorTest(unittest.TestCase):

    def test_generate_test_data(self):
        generated_data = []
        start = datetime.strptime('12/2/2019 1:30 PM', '%d/%m/%Y %I:%M %p')
        end = datetime.strptime('12/7/2019 1:30 PM', '%d/%m/%Y %I:%M %p')

        for i in range(0, 13000):
            a_data = {"timestamp": self.random_date(start, end),
                      "values": [
                          {"type": "temperature", "value": random.randrange(0, 40, 1)},
                          {"type": "humidity", "value": random.randrange(0, 101, 1)}
                      ],
                      "status": "OK",
                      "sensor_id": 100}
            generated_data.append(a_data)

        for data in generated_data:
            save_sensor_data(data)

    def random_date(self, start, end):
        delta = end - start
        int_delta = delta.total_seconds()
        random_second = random.randrange(0, int_delta, 60 * 20)
        return start + timedelta(seconds=random_second)


def init_db(database_config):
    conn = psycopg2.connect(host=database_config.host, database=database_config.database,
                            user=database_config.username, password=database_config.password)

    cursor = conn.cursor()
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()
    print(db_version)

    create_tables = ["""CREATE TABLE IF NOT EXISTS sensor_data (
        sensor_data_id SERIAL PRIMARY KEY,
        type1 varchar(20),
        value1 decimal,
        type2 varchar(20),
        value2 decimal,
        status varchar(20),
        sensor_id INTEGER,
        published_time TIMESTAMP)"""]
    try:
        for table in create_tables:
            cursor.execute(table)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cursor.close()
        conn.commit()
        conn.close()


init_db(Config.get_database_config())


if __name__ == '__main__':
    unittest.main()



