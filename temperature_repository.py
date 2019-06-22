from Temperature import Temperature
from repository import get_timerange_query, save, load_all, load_one


def save_temperature(temp_data):
    query = "INSERT INTO temperature(temperature, status, sensor_id, published_time) VALUES ({}, '{}', {}, '{}')".format(
        temp_data['temperature'], temp_data['status'], temp_data['sensor_id'], temp_data['timestamp'])
    save(query)


def load_all_temperature():
    sql = "SELECT * FROM temperature ORDER BY published_time"
    return load_all(sql, cast_temperature)


def load_current_temperature():
    sql = "SELECT * FROM temperature ORDER BY published_time DESC LIMIT 1"
    return load_one(sql, cast_temperature)


def load_temperature_for(sensor, timerange):
    timerange_query = get_timerange_query(timerange)
    sql = 'SELECT * FROM temperature WHERE sensor_id={}{}'.format(sensor["sensor_id"], timerange_query)
    return load_all(sql, cast_temperature)


def cast_temperature(value):
    if value is None:
        return None
    return Temperature(id=value[0], temperature=value[1], sensor_status=value[2], published_time=value[3],
                       sensor_id=value[4])
