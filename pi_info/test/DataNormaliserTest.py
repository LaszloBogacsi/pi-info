import unittest
from datetime import datetime
from decimal import Decimal

from pi_info.data.data_normaliser import make_minute_resolution_data, get_data_for_resolution
from pi_info.repository.SensorData import SensorData


class DataNormaliserTest(unittest.TestCase):

    # <<<< Minute resolution >>>>

    def test_can_interpolate_between_two_datapoints(self):
        data1 = [
            SensorData([
                {"type": "temperature", "value": Decimal(20.5)},
                {"type": "humidity", "value": Decimal(50.5)},
            ], "OK", datetime.strptime("2019-06-16 10:50:30.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([
                {"type": "temperature", "value": Decimal(22.5)},
                {"type": "humidity", "value": Decimal(54.5)},
            ], "OK", datetime.strptime("2019-06-16 10:52:30.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]

        expected = [
            SensorData([
                {"type": "temperature", "value": Decimal(21.0)},
                {"type": "humidity", "value": Decimal(51.5)},
            ], "OK", datetime.strptime("2019-06-16 10:51:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([
                {"type": "temperature", "value": Decimal(22.0)},
                {"type": "humidity", "value": Decimal(53.5)},
            ], "OK", datetime.strptime("2019-06-16 10:52:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]
        actual = make_minute_resolution_data(data1)
        self.assertEqual(actual, expected)

    def test_can_interpolate_between_two_datapoints_with_microseconds(self):
        data1 = [
            SensorData([
                {"type": "temperature", "value": Decimal(20.5)},
                {"type": "humidity", "value": Decimal(50.5)},
            ], "OK", datetime.strptime("2019-06-16 10:50:30.123456", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([
                {"type": "temperature", "value": Decimal(22.5)},
                {"type": "humidity", "value": Decimal(54.5)},
            ], "OK", datetime.strptime("2019-06-16 10:52:30.456789", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]

        expected = [
            SensorData([
                {"type": "temperature", "value": Decimal(21.0)},
                {"type": "humidity", "value": Decimal(51.5)},
            ], "OK", datetime.strptime("2019-06-16 10:51:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([
                {"type": "temperature", "value": Decimal(22.0)},
                {"type": "humidity", "value": Decimal(53.5)},
            ], "OK", datetime.strptime("2019-06-16 10:52:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]
        actual = make_minute_resolution_data(data1)
        self.assertEqual(actual, expected)

    def test_returns_empty_data_when_empty(self):
        data1 = []

        expected = []
        actual = make_minute_resolution_data(data1)
        self.assertEqual(actual, expected)

    def test_create_empty_datapoints_for_times_wider_than_tolerance(self):
        data1 = [
            SensorData([
                {"type": "temperature", "value": Decimal(20.5)},
                {"type": "humidity", "value": Decimal(50.5)},
            ], "OK", datetime.strptime("2019-06-16 10:10:30.123456", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([
                {"type": "temperature", "value": Decimal(22.5)},
                {"type": "humidity", "value": Decimal(54.5)},
            ], "OK", datetime.strptime("2019-06-16 10:42:30.456789", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]

        expected = []
        for i in range(11, 43, ):
            padded_minute_str = str(i)
            expected.append( SensorData([
                {"type": "temperature", "value": Decimal(0.0)},
                {"type": "humidity", "value": Decimal(0.0)},
            ], "OK", datetime.strptime("2019-06-16 10:" + padded_minute_str + ":00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100))
        actual = make_minute_resolution_data(data1)
        self.assertEqual(actual, expected)

    def test_can_ignore_datapoints_that_are_in_the_same_minute_but_keep_ones_that_are_less_than_a_minute_away_but_different_minute(
            self):
        data1 = [
            SensorData([{"type": "temperature", "value": Decimal(20.5)},{"type": "humidity", "value": Decimal(50.5)}],
                       "OK", datetime.strptime("2019-06-16 10:10:20.123456", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([{"type": "temperature", "value": Decimal(21.5)},{"type": "humidity", "value": Decimal(55.5)}],
                       "OK", datetime.strptime("2019-06-16 10:10:30.456789", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([{"type": "temperature", "value": Decimal(22.5)},{"type": "humidity", "value": Decimal(60.5)}],
                       "OK", datetime.strptime("2019-06-16 10:11:20.567891", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]

        expected = [
            SensorData([{"type": "temperature", "value": Decimal("22.10")},{"type": "humidity", "value": Decimal(58.5)}],
                       "OK", datetime.strptime("2019-06-16 10:11:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]
        actual = make_minute_resolution_data(data1)
        self.assertEqual(expected, actual)

    # <<<< data for resoluiton >>>>

    def test_can_create_data_for_selected_resolution(self):
        minute_data = [
            SensorData([{"type": "temperature", "value": Decimal(21.0)},{"type": "humidity", "value": Decimal(50.5)}],
                        "OK", datetime.strptime("2019-06-16 10:35:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([{"type": "temperature", "value": Decimal(23.0)},{"type": "humidity", "value": Decimal(60.5)}],
                        "OK", datetime.strptime("2019-06-16 10:55:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([{"type": "temperature", "value": Decimal(23.0)},{"type": "humidity", "value": Decimal(52.5)}],
                        "OK", datetime.strptime("2019-06-16 11:10:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            SensorData([{"type": "temperature", "value": Decimal(24.0)},{"type": "humidity", "value": Decimal(62.5)}],
                        "OK", datetime.strptime("2019-06-16 11:15:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]
        expected = [
            {"published_at": datetime.strptime("2019-06-16 10:30:00.000000", '%Y-%m-%d %H:%M:%S.%f'),
             "data":
                 SensorData([{"type": "temperature", "value": Decimal(22.0)},{"type": "humidity", "value": Decimal(55.5)}],
                            "OK", datetime.strptime("2019-06-16 10:30:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)},
            {"published_at": datetime.strptime("2019-06-16 11:00:00.000000", '%Y-%m-%d %H:%M:%S.%f'),
             "data":
                 SensorData([{"type": "temperature", "value": Decimal(23.5)},{"type": "humidity", "value": Decimal(57.5)}],
                            "OK", datetime.strptime("2019-06-16 11:00:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)},
        ]
        actual = get_data_for_resolution(minute_data, 30)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
