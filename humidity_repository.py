from repository import save, load_all, load_one, get_timerange_query


def save_humidity(humidity_data):
    query = 'INSERT INTO humidity(humidity, status, sensor_id, published_time) VALUES ({}, {}, {}, {})'.format(
        humidity_data['humidity'], humidity_data['status'], humidity_data['sensor_id'], humidity_data['timestamp'])
    save(query)


def load_all_humidity():
    sql = "SELECT * FROM humidity ORDER BY published_time"
    return load_all(sql, cast_humidity)


def load_current_humidity():
    sql = "SELECT * FROM humidity ORDER BY published_time DESC LIMIT 1"
    return load_one(sql, cast_humidity)


def load_humidity_for(sensor, timerange):
    timerange_query = get_timerange_query(timerange)
    sql = "SELECT * FROM humidity WHERE sensor_id={}{}".format(sensor["sensor_id"], timerange_query)
    return load_all(sql, cast_humidity)


class Humidity(object):
    def __init__(self, id, humidity, sensor_status, published_time, sensor_id):
        self.published_time = published_time
        self.sensor_id = sensor_id
        self.sensor_status = sensor_status
        self.humidity = humidity
        self.id = id


def cast_humidity(value):
    if value is None:
        return None
    return Humidity(id=value[0], humidity=value[1], sensor_status=value[2], published_time=value[3],
                    sensor_id=value[4])
