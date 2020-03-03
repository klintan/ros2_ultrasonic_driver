import os
from glob import glob

from setuptools import setup, find_packages

PACKAGE_NAME = 'ros2_ultrasonic_driver'
SHARE_DIR = os.path.join("share", PACKAGE_NAME)

setup(
    name=PACKAGE_NAME,
    version='0.0.1',
    packages=["ultrasonic"],
    package_dir={'': 'src', },
    data_files=[
        (os.path.join(SHARE_DIR, "launch"), glob(os.path.join("launch", "*.launch.py"))),
        (os.path.join(SHARE_DIR, "config"), glob(os.path.join("config", "*.yaml")))],
    install_requires=['setuptools',
                      'pyserial'
                      ],
    author='Andreas Klintberg',
    author_email='andreas.klintberg@gmail.com',
    description='ROS2 ultrasonic sensors parking kit driver.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'ultrasonic_driver = ultrasonic.driver:main',
        ],
    },
)
