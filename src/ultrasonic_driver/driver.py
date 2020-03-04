import re
import sys

import serial
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Range
from std_msgs.msg import Header


class UltrasonicDriver(Node):
    def __init__(self):
        super().__init__('ultrasonic_driver')
        self.range_pub = self.create_publisher(Range, 'ultrasonic_range', 10)

        self.port = self.declare_parameter('port', '/dev/tty.usbmodem141301').value
        self.baudrate = self.declare_parameter('baud', 115200).value

        self.min_range = self.declare_parameter('min_range', 0.10).value
        self.max_range = self.declare_parameter('max_range', 1.0).value

        # We need to have one frame_id per sensor
        # TODO loop through arbitrary defined sensors
        # self.frame_id_a = self.declare_parameter('sensor_a_fid', 'ultrasonic_sensor_a').value

        try:
            self.range_serial_reader = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=2)
        except serial.SerialException as e:
            self.get_logger().fatal(f"Serial communication failed {e}")
            sys.exit()

        while rclpy.ok():
            data = self.read_data()
            try:
                sensor_id, distance = UltrasonicDriver.parse_data(data)
            except Exception as e:
                self.get_logger().warning(f"Data parsing failed for data: {data}, Error: {e}")
                continue

            msg = self.to_msg(sensor_id, distance)
            self.get_logger().info(f"{msg.range}")
            self.range_pub.publish(msg)

    def read_data(self):
        data = self.range_serial_reader.readline().strip()
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        return data

    @staticmethod
    def parse_data(data):
        if data:
            parts = data.split(" ")
            if len(parts) != 2:
                # self.get_logger().warning("Could not parse sensor data")
                raise Exception("Incorrect data format")

            distance = float(parts[1])
            # from cm to m
            distance *= 0.01

            id_regex = r'A|B|C|D|E|F|G|H'
            sensor_id = re.findall(id_regex, parts[0])[0]

            return sensor_id, distance

        raise Exception("Data empty")

    def to_msg(self, sensor_id, distance):

        msg = Range()
        msg.header = Header()

        msg.header.stamp = self.get_clock().now().to_msg()
        # need to define transforms for all sensors
        msg.header.frame_id = f"ultrasonic_sensor_{sensor_id}"

        msg.radiation_type = 0

        msg.field_of_view = 0
        msg.min_range = self.min_range
        msg.max_range = self.max_range
        msg.range = distance

        return msg


def main(args=None):
    rclpy.init(args=args)
    driver = UltrasonicDriver()

    rclpy.spin(driver)

    driver.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
