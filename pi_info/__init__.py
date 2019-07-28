from pi_info.application_config import Config
Config('../config.ini')
import psycopg2
from pi_info.Credentials import Credentials
from pi_info.mqtt.MqttClient import MqttClient
from pi_info.mqtt.message_handler import MessageHandler
from pi_info.repository.sensor_data_repository import save_sensor_data

in_stub_mode = False
mqtt_client = None
if not in_stub_mode:
    mqtt_config = Config.get_mqtt_config()
    handlers = [MessageHandler('sensor/temperature', save_sensor_data)]
    mqtt_client = MqttClient(Credentials(mqtt_config.username, mqtt_config.password), mqtt_config.host, handlers)


def init_db(config):
    conn = psycopg2.connect(host=config.host, database=config.database, user=config.username, password=config.password)

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


database_config = Config.get_database_config()
init_db(database_config)
