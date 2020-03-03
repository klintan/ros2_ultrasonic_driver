import unittest

from ultrasonic.driver import UltrasonicDriver

class UltrasonicSensorTest(unittest.TestCase):

    def test_parse_data(self):

        us_driver = UltrasonicDriver()

        test_data = """
        SensorA: 34
        SensorB: 0
        SensorC: 0
        SensorA: 40
        SensorD: 0
        """

        parsed_data = []
        for line in test_data.split("\n"):
            parsed_data.append(us_driver.parse_data(line))

        self.assertIn(("A", 0.34), parsed_data)
