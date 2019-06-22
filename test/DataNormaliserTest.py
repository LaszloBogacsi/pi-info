import unittest

from datetime import datetime

from Temperature import Temperature
from data.data_normaliser import make_minute_resolution_data


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


if __name__ == '__main__':
    unittest.main()
