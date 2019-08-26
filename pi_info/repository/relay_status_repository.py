from pi_info.repository.RelayStatus import RelayStatus
from pi_info.repository.repository import save, load_one


def save_relay_status(relay_status):
    query = "INSERT INTO relay_status(relay_id, status) VALUES ('{}', {})".format(
        relay_status['id'], relay_status['status'])
    save(query)


def load_relay_status_by(relay_id) -> RelayStatus:
    sql = 'SELECT * FROM relay_status WHERE relay_id={} ORDER BY status_id DESC LIMIT 1'.format(relay_id)
    return load_one(sql, cast_relay_status)


def cast_relay_status(value) -> RelayStatus or None:
    if value is None:
        return None
    return RelayStatus(relay_id=value[1], status=value[2])
