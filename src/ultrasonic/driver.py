import re
import serial

import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Range
from std_msgs.msg import Header


class UltrasonicDriver(Node):
    def __init__(self):
        super().__init__('ros2_ultrasonic_driver')
        self.range_pub = self.create_publisher(Range, 'ultrasonic_range', 10)

        self.port = self.declare_parameter('port', '/dev/ttyUSB0').value
        self.baudrate = self.declare_parameter('baud', 115200).value

        self.min_range = self.declare_parameter('min_range', 0.10).value
        self.max_range = self.declare_parameter('max_range', 1.0).value

        # We need to have one frame_id per sensor
        self.frame_id = self.declare_parameter('frame_id', 'ultrasonic').value

        try:
            self.range_serial_reader = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=2)
        except serial.SerialException as e:
            self.get_logger().fatal("Serial communication failed", e)

        while rclpy.ok():
            data = self.read_data()
            sensor_id, distance = self.parse_data(data)
            msg = self.to_msg(sensor_id, distance)
            self.range_pub.publish(msg)

    def read_data(self):
        return self.range_serial_reader.readline().strip()

    def parse_data(self, data):

        if data:
            parts = data.split(" ")
            if len(parts) != 2:
                self.get_logger().warning("Could not parse sensor data")
                return {}

            distance = float(parts[1])
            # from cm to m
            distance *= 0.01

            id_regex = r'A|B|C|D|E|F|G|H'
            sensor_id = re.findall(id_regex, parts[0])[0]

        return sensor_id, distance

    def to_msg(self, sensor_id, distance):

        msg = Range()

        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg

        msg.header.frame_id = self.frame_id
        msg.radiation_type = 0

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