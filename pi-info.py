from applicationConfig import Config

Config('config.ini')

import psycopg2
from flask import Flask

from Credentials import Credentials
from blueprints.home import home
from blueprints.sensors import sensors


from MqttClient import MqttClient

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(sensors)

mqtt_config = Config.get_mqtt_config()
mqttClient = MqttClient(Credentials(mqtt_config['MQTT_USERNAME'], mqtt_config['MQTT_PASSWORD']),
                        mqtt_config['MQTT_HOST'])


def init_db(database_config):
    conn = psycopg2.connect(host=database_config['host'], database=database_config['database'],
                            user=database_config['user'], password=database_config['password'])

    cursor = conn.cursor()
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()
    print(db_version)

    create_tables = (
        """
    CREATE TABLE IF NOT EXISTS temperature (
    temprature_id SERIAL PRIMARY KEY,
    temperature DECIMAL,
    status varchar(20),
    sensor_location varchar(50),
    published_time TIMESTAMP
    
     )
    """,
        """
    CREATE TABLE IF NOT EXISTS humidity (
    humidity_id SERIAL PRIMARY KEY,
    humidity DECIMAL,
    status varchar(20),
    sensor_location varchar(50),
    published_time TIMESTAMP
    
    )
    """
    )
    try:
        for table in create_tables:
            cursor.execute(table)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cursor.close()
        conn.commit()
        conn.close()


if __name__ == "__main__":
    Config('config.ini')
    init_db(Config.get_database_config())
    app.run(host='0.0.0.0', port=9080)
