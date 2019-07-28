import decimal
from datetime import timedelta, datetime

from pi_info.repository.SensorData import SensorData
from pi_info.data.sensors import get_sensor_by_id


def make_minute_resolution_data(data_arr) -> [SensorData]:
    if len(data_arr) <= 1:
        return data_arr

    DEFAULT_SAMPLING_RATE = 20
    data_by_minute = []

    def make_values(value):
        first_value = value["value"]
        second_value = next(v for v in second.values if v["type"] == value["type"])["value"]
        d_value = second_value - first_value
        nearest_minute_value = first_value + decimal.Decimal((nearest_minute - first_time).seconds / 60) * d_value / d_time_mins
        new_temp = nearest_minute_value + (d_value / d_time_mins) * j if d_time_mins < tolerance else decimal.Decimal(0.0)
        new_temp_rounded = decimal.Decimal(new_temp.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP))
        return {"type": value["type"], "value": new_temp_rounded}

    for i in range(len(data_arr)):
        first = data_arr[i]
        if i == len(data_arr) - 1:
            break
        second = data_arr[i + 1]
        sampling_frequency_mins = get_sensor_by_id(first.sensor_id).get("sampling_rate_mins", DEFAULT_SAMPLING_RATE)
        tolerance = 1.5 * sampling_frequency_mins

        d_time_mins = decimal.Decimal((second.published_time - first.published_time).seconds / 60)
        if d_time_mins == 0: continue
        first_time = first.published_time.replace(microsecond=0)
        first_time_rounded = first_time.replace(second=0)
        nearest_minute = first_time_rounded + timedelta(minutes=1)
        in_same_minute = first_time.minute == second.published_time.minute
        d_time_mins_int = 0

        if d_time_mins < 1 and not in_same_minute:
            d_time_mins_int = 1
        elif d_time_mins >= 1:
            d_time_mins_int = int(d_time_mins)
        for j in range(d_time_mins_int):
            values = list(map(make_values, first.values))
            data_by_minute.append(SensorData(values, first.sensor_status, nearest_minute + timedelta(minutes=j), first.sensor_id))

    return data_by_minute


def get_data_for_resolution(minute_data, resolution_mins):
    def by_time(data):
        return {"published_at": data.published_time, "data": data}

    data_by_time = list(map(by_time, minute_data))

    def group_by_time_for_resolution(data):
        if len(data) == 0: return data
        first_time = data[0]["published_at"]
        diff_seconds = datetime.timestamp(first_time) % (resolution_mins * 60)
        bucket_start_time = first_time - timedelta(seconds=diff_seconds)
        grouped_by_time_buckets = []
        bucket_end_time = bucket_start_time + timedelta(minutes=resolution_mins)
        for d in data:
            time = d["published_at"]
            value = d["data"]
            if time < bucket_end_time:
                exist = next((item for item in grouped_by_time_buckets if item["published_at"] == bucket_start_time), None)
                if exist is not None:
                    exist["data"].append(value)
                else:
                    grouped_by_time_buckets.append({"published_at": bucket_start_time, "data": [value]})
            else:
                bucket_start_time = bucket_end_time
                bucket_end_time = bucket_end_time + timedelta(minutes=resolution_mins)
                grouped_by_time_buckets.append({"published_at": bucket_start_time, "data": [value]})
        return grouped_by_time_buckets

    data_by_time_by_resolution = group_by_time_for_resolution(data_by_time)

    def calculate_average_for_buckets(data):
        averaged_data = []
        for d in data:
            time = d["published_at"]
            sensor_datas = d["data"]
            a_data = sensor_datas[0]

            def get_average_by_type(value):
                data_type = value["type"]
                return {"type": data_type, "value": decimal.Decimal((sum(list(map(lambda b: next(item for item in b.values if item["type"] == data_type)["value"], sensor_datas))) / len(sensor_datas)).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP))}

            values = list(map(get_average_by_type, a_data.values))
            averaged_data.append({"published_at": time, "data": SensorData(values, a_data.sensor_status, time, a_data.sensor_id)})
        return averaged_data

    averagedata_by_resolution = calculate_average_for_buckets(data_by_time_by_resolution)
    return averagedata_by_resolution
