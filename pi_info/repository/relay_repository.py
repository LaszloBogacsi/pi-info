from pi_info.repository.Relay import Relay
from pi_info.repository.repository import save, load_all, load_one


def save_relay(relay):
    query = "INSERT INTO relay(relay_id, name, location, type) VALUES ('{}', {}, '{}', {})".format(
        relay['id'], relay['name'], relay['location'], relay['type'])
    save(query)


def load_all_relays() -> [Relay]:
    sql = "SELECT * FROM relay ORDER BY relay_id"
    return load_all(sql, cast_relay)


def load_relay_by(relay_id) -> Relay:
    sql = 'SELECT * FROM relay WHERE relay_id={}'.format(relay_id)
    return load_one(sql, cast_relay)


def cast_relay(value) -> Relay or None:
    if value is None:
        return None
    return Relay(id=value[0], name=value[1], location=value[2], type=value[4])
