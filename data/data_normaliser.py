from datetime import timedelta

from Temperature import Temperature
from sensors import SENSORS, get_sensor_by_id


def make_minute_resolution_data(data_arr) -> [Temperature]:
    if len(data_arr) <= 1:
        return data_arr

    DEFAULT_SAMPLING_RATE = 20
    temp_by_minute = []
    for i in range(len(data_arr)):
        first = data_arr[i]
        if i == len(data_arr) - 1:
            break
        second = data_arr[i + 1]
        sampling_frequency_mins = get_sensor_by_id(first.sensor_id).get("sampling_rate_mins", DEFAULT_SAMPLING_RATE)
        tolerance = 1.5 * sampling_frequency_mins
        d_temp = second.temperature - first.temperature
        d_time_mins = (second.published_time - first.published_time).seconds / 60
        first_time_rounded = first.published_time.replace(second=0, microsecond=0)
        nearest_minute = first_time_rounded + timedelta(minutes=1)
        nearest_minute_temp = first.temperature + float((nearest_minute - first_time_rounded).seconds / 60) * d_temp / d_time_mins

        for j in range(int(d_time_mins)):
            new_temp = nearest_minute_temp + (d_temp / d_time_mins) * j if d_time_mins < tolerance else 0.0
            temp_by_minute.append(Temperature("", new_temp, first.sensor_status, nearest_minute + timedelta(minutes=j), first.sensor_id))

    return temp_by_minute


def get_data_for_resolution(data_by_minute, resolution_mins) -> [Temperature]:
    pass
