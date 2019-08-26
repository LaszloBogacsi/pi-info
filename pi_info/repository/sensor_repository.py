from pi_info.repository.Sensor import Sensor
from pi_info.repository.repository import save, load_all, load_one


def save_sensor(sensor):
    query = "INSERT INTO sensor(sensor_id, name, location, code, type, sampling_rate) VALUES ({}, '{}', '{}', '{}', '{}', {})".format(
        sensor['id'], sensor['name'], sensor['location'], sensor['code'], sensor['type'], sensor['sampling_rate'])
    save(query)


def load_all_sensors() -> [Sensor]:
    sql = "SELECT * FROM sensor ORDER BY sensor_id"
    return load_all(sql, cast_sensor)


def load_sensor_by(sensor_id) -> Sensor:
    sql = 'SELECT * FROM sensor WHERE sensor_id={}'.format(sensor_id)
    return load_one(sql, cast_sensor)


def cast_sensor(value) -> Sensor or None:
    if value is None:
        return None
    return Sensor(id=value[0], name=value[1], location=value[2], code=value[3], type=value[4], sampling_rate=value[5])
