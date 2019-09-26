from pi_info.repository.Device import Device
from pi_info.repository.repository import save, load_all, load_one


def save_device(device):
    query = "INSERT INTO device(device_id, name, location, type) VALUES ('{}', {}, '{}', {})".format(
        device['id'], device['name'], device['location'], device['type'])
    save(query)


def load_all_devices() -> [Device]:
    sql = "SELECT * FROM device ORDER BY device_id"
    return load_all(sql, cast_device)


def load_device_by(device_id) -> Device:
    sql = 'SELECT * FROM device WHERE device_id={}'.format(device_id)
    return load_one(sql, cast_device)


def cast_device(value) -> Device or None:
    if value is None:
        return None
    return Device(id=value[0], name=value[1], location=value[2], type=value[4])
