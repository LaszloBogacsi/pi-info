from pi_info.repository.Schedule import Schedule
from pi_info.repository.repository import save, load_all


def save_schedule(schedule):
    query = "INSERT INTO schedule(device_id, status, days, time) VALUES ({}, '{}', '{}', '{}') RETURNING schedule_id".format(
        schedule['device_id'], schedule['status'], schedule['days'], schedule['time'])
    return save(query)

def update_schedule(schedule):
    query = "UPDATE schedule SET device_id={}, status='{}', days='{}', time='{}' WHERE schedule_id={} RETURNING schedule_id".format(
        schedule['device_id'], schedule['status'], schedule['days'], schedule['time'], schedule['schedule_id'])
    return save(query)


def delete_schedule(schedule_id):
    query = "DELETE FROM schedule WHERE schedule_id={}".format(schedule_id)
    save(query)


def load_all_schedules() -> [Schedule]:
    sql = "SELECT * FROM schedule"
    return load_all(sql, cast_schedule)


def load_schedules_for(device_id) -> [Schedule]:
    sql = 'SELECT * FROM schedule WHERE device_id={}'.format(device_id)
    return load_all(sql, cast_schedule)


def cast_schedule(value) -> Schedule or None:
    if value is None:
        return None
    return Schedule(schedule_id=value[0], device_id=value[1], status=value[2], days=value[3], time=str(value[4]))
