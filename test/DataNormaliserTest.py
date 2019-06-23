import unittest

from datetime import datetime

from Temperature import Temperature
from data.data_normaliser import make_minute_resolution_data, get_data_for_resolution


class DataNormaliserTest(unittest.TestCase):

    def test_can_interpolate_between_two_datapoints(self):
        data1 = [
            Temperature( "001", 20.5, "OK", datetime.strptime("2019-06-16 10:50:30.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            Temperature( "001", 22.5, "OK", datetime.strptime("2019-06-16 10:52:30.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
        ]

        expected = [
            Temperature( "", 21.0, "OK", datetime.strptime("2019-06-16 10:51:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            Temperature( "", 22.0, "OK", datetime.strptime("2019-06-16 10:52:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)
         ]
        actual = make_minute_resolution_data(data1)
        self.assertEqual(actual, expected)

    def test_can_interpolate_between_two_datapoints_with_microseconds(self):
        data1 = [
            Temperature( "001", 20.5, "OK", datetime.strptime("2019-06-16 10:50:30.123456", '%Y-%m-%d %H:%M:%S.%f'), 100),
            Temperature( "002", 22.5, "OK", datetime.strptime("2019-06-16 10:52:30.456789", '%Y-%m-%d %H:%M:%S.%f'), 100),
        ]

        expected = [
            Temperature( "", 21.0, "OK", datetime.strptime("2019-06-16 10:51:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            Temperature( "", 22.0, "OK", datetime.strptime("2019-06-16 10:52:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)
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
            Temperature( "001", 20.5, "OK", datetime.strptime("2019-06-16 10:10:30.123456", '%Y-%m-%d %H:%M:%S.%f'), 100),
            Temperature( "002", 22.5, "OK", datetime.strptime("2019-06-16 10:42:30.456789", '%Y-%m-%d %H:%M:%S.%f'), 100),
        ]

        expected = []
        for i in range(11, 43,):
            padded_minute_str = str(i)
            expected.append(Temperature( "", 0.0, "OK", datetime.strptime("2019-06-16 10:" + padded_minute_str  + ":00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100))
        actual = make_minute_resolution_data(data1)
        self.assertEqual(actual, expected)

    def test_can_create_data_for_selected_resolution(self):
        minute_data = [
            Temperature( "", 21.0, "OK", datetime.strptime("2019-06-16 10:35:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            Temperature( "", 23.0, "OK", datetime.strptime("2019-06-16 10:55:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            Temperature( "", 23.0, "OK", datetime.strptime("2019-06-16 11:10:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100),
            Temperature( "", 24.0, "OK", datetime.strptime("2019-06-16 11:15:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)
        ]
        expected = [
            {datetime.strptime("2019-06-16 10:30:00.000000", '%Y-%m-%d %H:%M:%S.%f'): Temperature( "", 22.0, "OK", datetime.strptime("2019-06-16 10:30:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)},
            {datetime.strptime("2019-06-16 11:00:00.000000", '%Y-%m-%d %H:%M:%S.%f'): Temperature( "", 23.5, "OK", datetime.strptime("2019-06-16 11:00:00.000000", '%Y-%m-%d %H:%M:%S.%f'), 100)},
        ]
        actual = get_data_for_resolution(minute_data, 30)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
