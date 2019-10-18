from pi_info.repository.DeviceStatus import Status
from pi_info.repository.Group import Group
from pi_info.repository.repository import load_all, save, save_and_get_id, load_one


def save_group(group: Group):
    query = "INSERT INTO device_group(group_id, name, delay, ids, status) VALUES ('{}', '{}', {}, '{}', '{}')".format(
        group.group_id, group.name, group.delay_in_ms, ','.join(map(str, group.ids)), group.status.value)
    return save(query)


def update_group(group: Group):
    query = "UPDATE device_group SET name='{}', delay={}, ids='{}', status='{}' WHERE group_id='{}'".format(
        group.name, group.delay_in_ms,','.join(map(str, group.ids)), group.status.value, group.group_id)
    save(query)


def delete_group(group_id: str):
    query = "DELETE FROM device_group WHERE group_id='{}'".format(group_id)
    save(query)


def load_all_groups() -> [Group]:
    sql = "SELECT * FROM device_group"
    return load_all(sql, cast_group)


def load_group_by(group_id: str) -> Group:
    sql = "SELECT * FROM device_group WHERE group_id='{}'".format(group_id)
    return load_one(sql, cast_group)


def cast_group(value) -> Group or None:
    if value is None:
        return None
    return Group(group_id=value[0], name=value[1], delay_in_ms=value[2], ids=[int(v) for v in value[3].split(',')], status=Status(value[4]))
