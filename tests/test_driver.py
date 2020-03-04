import unittest

from ultrasonic.driver import UltrasonicDriver

class UltrasonicSensorTest(unittest.TestCase):

    def test_parse_data(self):

        test_data = "SensorA: 34\nSensorB: 0\nSensorC: 0\nSensorA: 40\nSensorD: 0"

        parsed_data = []
        for line in test_data.split("\n"):
            parsed_data.append(UltrasonicDriver.parse_data(line))

        self.assertIn(("A", 0.34), parsed_data)


if __name__ == '__main__':
    unittest.main()