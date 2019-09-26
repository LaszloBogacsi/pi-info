from pi_info.repository.DeviceStatus import DeviceStatus
from pi_info.repository.repository import save, load_one


def save_device_status(device_status):
    query = "INSERT INTO device_status(device_id, status) VALUES ('{}', {})".format(
        device_status['id'], device_status['status'])
    save(query)


def load_device_status_by(device_id) -> DeviceStatus:
    sql = 'SELECT * FROM device_status WHERE device_id={} ORDER BY status_id DESC LIMIT 1'.format(device_id)
    return load_one(sql, cast_device_status)


def cast_device_status(value) -> DeviceStatus or None:
    if value is None:
        return None
    return DeviceStatus(device_id=value[1], status=value[2])
