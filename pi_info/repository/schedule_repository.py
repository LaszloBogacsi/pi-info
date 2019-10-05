from pi_info.repository.Schedule import Schedule
from pi_info.repository.repository import save, load_all, save_and_get_id


def save_schedule(schedule: Schedule):
    query = "INSERT INTO schedule(group_id, device_id, status, days, time) VALUES ({}, '{}', '{}', '{}', '{}') RETURNING schedule_id".format(
        schedule.group_id, ','.join(map(str, schedule.device_id)), schedule.status, schedule.days, schedule.time)
    return save_and_get_id(query)


def update_schedule(schedule: Schedule):
    query = "UPDATE schedule SET device_id='{}', status='{}', days='{}', time='{}' WHERE schedule_id={}".format(
        ','.join(map(str, schedule.device_id)), schedule.status, schedule.days, schedule.time, schedule.schedule_id)
    save(query)
    return schedule.schedule_id


def delete_schedule(schedule_id):
    query = "DELETE FROM schedule WHERE schedule_id={}".format(schedule_id)
    save(query)


def load_all_schedules() -> [Schedule]:
    sql = "SELECT * FROM schedule"
    return load_all(sql, cast_schedule)


def load_schedules_for(group_id) -> [Schedule]:
    sql = 'SELECT * FROM schedule WHERE group_id={}'.format(group_id)
    return load_all(sql, cast_schedule)


def cast_schedule(value) -> Schedule or None:
    if value is None:
        return None
    return Schedule(schedule_id=value[0], group_id=value[1], device_id=[int(v) for v in value[2].split(',')], status=value[3], days=value[4], time=str(value[5]))
