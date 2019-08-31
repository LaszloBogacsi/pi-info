from pi_info.data.room import Room
from pi_info.data.SensorType import SensorType
from pi_info.repository.Sensor import Sensor
from pi_info.repository.repository import save, load_all, load_one


def save_sensor(sensor):
    query = "INSERT INTO sensor(sensor_id, name, location, code, type, sampling_rate) VALUES ({}, '{}', '{}', '{}', '{}', {})".format(
        sensor['id'], sensor['name'], sensor['location'], sensor['code'], sensor['type'], sensor['sampling_rate'])
    save(query)


def update_sensor(sensor):
    query = "UPDATE sensor SET name='{}', location='{}', code='{}', type='{}', sampling_rate={} WHERE sensor_id={}".format(
        sensor['name'], sensor['location'], sensor['code'], sensor['type'], sensor['sampling_rate'], sensor["id"])
    save(query)


def load_all_sensors() -> [Sensor]:
    sql = "SELECT * FROM sensor ORDER BY sensor_id"
    return load_all(sql, cast_sensor)


def load_sensor_by(sensor_id) -> Sensor:
    sql = 'SELECT * FROM sensor WHERE sensor_id={}'.format(sensor_id)
    return load_one(sql, cast_sensor)


def load_sensors_by_room(room) -> [Sensor]:
    sql = "SELECT * FROM sensor WHERE location='{}'".format(room.value)
    return load_all(sql, cast_sensor)


def delete_sensor_by_id(sensor_id):
    sql = 'DELETE FROM sensor WHERE sensor_id={}'.format(sensor_id)
    save(sql)


def cast_sensor(value) -> Sensor or None:
    if value is None:
        return None
    return Sensor(id=value[0], name=value[1], location=Room(value[2]), code=value[3], type=SensorType(value[4]), sampling_rate=value[5])
