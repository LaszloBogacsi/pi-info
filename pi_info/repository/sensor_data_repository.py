from pi_info.repository.SensorData import SensorData
from pi_info.repository.repository import save, load_all, load_one, get_timerange_query


def save_sensor_data(sensor_data):
    query = "INSERT INTO sensor_data(type1, value1, type2, value2, status, sensor_id, published_time) VALUES ('{}', {}, '{}', {}, '{}', {}, '{}')".format(
        sensor_data['values'][0]['type'], sensor_data['values'][0]['value'], sensor_data['values'][1]['type'], sensor_data['values'][1]['value'], sensor_data['status'], sensor_data['sensor_id'], sensor_data['timestamp'])
    save(query)


def load_all_sensor_data() -> [SensorData]:
    sql = "SELECT * FROM sensor_data ORDER BY published_time"
    return load_all(sql, cast_sensor_data)


def load_current_sensor_data() -> SensorData:
    sql = "SELECT * FROM sensor_data ORDER BY published_time DESC LIMIT 1"
    return load_one(sql, cast_sensor_data)


def load_sensor_data_for(sensor, timerange) -> [SensorData]:
    timerange_query = get_timerange_query(timerange)
    sql = 'SELECT * FROM sensor_data WHERE sensor_id={}{} ORDER BY published_time'.format(sensor["sensor_id"], timerange_query)
    return load_all(sql, cast_sensor_data)


def cast_sensor_data(value) -> SensorData or None:
    if value is None:
        return None
    return SensorData(values=[{"type": value[1], "value": value[2]}, {"type": value[3], "value": value[4]}], sensor_status=value[5], published_time=value[7],
                       sensor_id=value[6])
