import configparser
import psycopg2
from flask import Flask
from Credentials import Credentials
from MqttClient import MqttClient

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
credentials = Credentials(config['MQTT-BROKER']['MQTT_USERNAME'], config['MQTT-BROKER']['MQTT_PASSWORD'])
host = config['MQTT-BROKER']['MQTT_HOST']
mqttClient = MqttClient(credentials, host)

database_config = config['DATABASE-POSTGRES']
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
published_time TIMESTAMP

 )
""")
try:
    cursor.execute(create_tables)
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    cursor.close()
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Hello, World!\nThe current temperature is: " + "some message" + " C"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9080)
