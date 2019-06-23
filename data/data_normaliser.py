from datetime import timedelta, datetime

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
        first_time = first.published_time.replace(microsecond=0)
        first_time_rounded = first_time.replace(second=0)
        nearest_minute = first_time_rounded + timedelta(minutes=1)
        nearest_minute_temp = first.temperature + float((nearest_minute - first_time).seconds / 60) * d_temp / d_time_mins

        for j in range(int(d_time_mins)):
            new_temp = nearest_minute_temp + (d_temp / d_time_mins) * j if d_time_mins < tolerance else 0.0
            temp_by_minute.append(Temperature("", new_temp, first.sensor_status, nearest_minute + timedelta(minutes=j), first.sensor_id))

    return temp_by_minute


def get_data_for_resolution(minute_data, resolution_mins):
    def by_time(data):
        return {data.published_time: data}

    data_by_time = list(map(by_time, minute_data))

    def group_by_time_for_resolution(data, res):
        first_time = list(data[0].keys())[0]
        diff_seconds = datetime.timestamp(first_time) % (resolution_mins * 60)
        bucket_start_time = first_time - timedelta(seconds=diff_seconds)
        grouped_by_time_buckets = {}
        bucket_end_time = bucket_start_time + timedelta(minutes=resolution_mins)
        for d in data:
            for time, value in d.items():
                if time < bucket_end_time:
                    if bucket_start_time in grouped_by_time_buckets:
                        grouped_by_time_buckets[bucket_start_time].append(value)
                    else:
                        grouped_by_time_buckets[bucket_start_time] = [value]
                else:
                    bucket_start_time = bucket_end_time
                    bucket_end_time = bucket_end_time + timedelta(minutes=resolution_mins)
                    grouped_by_time_buckets[bucket_start_time] = [value]
        return grouped_by_time_buckets

    data_by_time_by_resolution = group_by_time_for_resolution(data_by_time, resolution_mins)

    def calculate_average_for_buckets(data):
        averaged_data = []
        for time, bucket in data.items():
            average_data_for_bucket = sum(list(map(lambda b: b.temperature, bucket))) / len(bucket)
            a_data = bucket[0]
            averaged_data.append({time: Temperature("", average_data_for_bucket, a_data.sensor_status, time, a_data.sensor_id)})
        return averaged_data

    averagedata_by_resolution = calculate_average_for_buckets(data_by_time_by_resolution)
    return averagedata_by_resolution
