from pi_info.repository.DeviceStatus import DeviceStatus, Status
from pi_info.repository.repository import save, load_one


def save_device_status(device_status: DeviceStatus):
    query = "INSERT INTO device_status(device_id, status) VALUES ({}, '{}')".format(
        device_status.device_id, device_status.status.value)
    save(query)


def load_device_status_by(device_id) -> DeviceStatus:
    sql = 'SELECT * FROM device_status WHERE device_id={}'.format(device_id)
    return load_one(sql, cast_device_status)


def update_device_status(device_status: DeviceStatus):
    query = "UPDATE device_status SET status='{}' WHERE device_id={}".format(device_status.status.value, device_status.device_id)
    save(query)


def cast_device_status(value) -> DeviceStatus or None:
    if value is None:
        return None
    return DeviceStatus(device_id=value[1], status=Status(value[2]))
