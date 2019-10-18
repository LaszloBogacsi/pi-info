from pi_info.data.DeviceType import DeviceType
from pi_info.data.room import Room
from pi_info.repository.Device import Device
from pi_info.repository.DeviceStatus import Status
from pi_info.repository.DeviceWithStatus import DeviceWithStatus
from pi_info.repository.repository import save, load_all, load_one


def save_device(device: Device):
    query = "INSERT INTO device(device_id, name, location, type) VALUES ({}, '{}', '{}', '{}')".format(
        device.device_id, device.name, device.location.value, device.device_type.value)
    save(query)


def update_device(device: Device):
    query = "UPDATE device SET name='{}', location='{}', type='{}' WHERE device_id={}".format(
        device.name, device.location.value, device.device_type.value, device.device_id)
    save(query)


def load_all_devices() -> [Device]:
    sql = "SELECT * FROM device ORDER BY device_id"
    return load_all(sql, cast_device)


def load_all_devices_with_status() -> [DeviceWithStatus]:
    sql = "SELECT device.*, ds.status FROM device JOIN device_status ds on device.device_id = ds.device_id ORDER BY device.device_id"
    return load_all(sql, cast_device_with_status)


def load_all_devices_with_status_by(room: Room) -> [DeviceWithStatus]:
    sql = "SELECT device.*, ds.status FROM device JOIN device_status ds on device.device_id = ds.device_id WHERE location='{}' ORDER BY device.device_id".format(room.value)
    return load_all(sql, cast_device_with_status)


def load_device_with_status_by(device_id: int) -> [DeviceWithStatus]:
    sql = "SELECT device.*, ds.status FROM device JOIN device_status ds on device.device_id = ds.device_id WHERE ds.device_id={}".format(device_id)
    return load_one(sql, cast_device_with_status)

def load_device_by(device_id: int) -> Device:
    sql = 'SELECT * FROM device WHERE device_id={}'.format(device_id)
    return load_one(sql, cast_device)


def delete_device_by(device_id: int):
    query = 'DELETE FROM device WHERE device_id={}'.format(device_id)
    save(query)


def cast_device(value) -> Device or None:
    if value is None:
        return None
    return Device(device_id=value[0], name=value[1], location=Room(value[2]), type=DeviceType(value[3]))


def cast_device_with_status(value) -> DeviceWithStatus or None:
    if value is None:
        return None
    return DeviceWithStatus(device_id=value[0], name=value[1], location=Room(value[2]), device_type=DeviceType(value[3]), status=Status(value[4]))
