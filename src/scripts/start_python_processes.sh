#!/bin/sh

python src/python/imu_node.py \
  --server_address 'localhost' \
  --server_port 8767 \
  --serial_port '/dev/ttyUSB_IMU0' \
  --baudrate 921600 \
  --sleep_duration 0.2 

python src/python/imu_node.py \
  --server_address 'localhost' \
  --server_port 8768 \
  --serial_port '/dev/ttyUSB_IMU1' \
  --baudrate 921600 \
  --sleep_duration 0.2 

python src/python/motor_node.py \
  --server_address 'localhost' \
  --server_port 8766 \
  --distance_max 1.5 \
  --pwm_frequency 250 \
  --pwm_duty_cycle 0.5 \
  --dir_pin 11 \
  --pwm_pin 12 \
  --speed_factor 0.07 \
  --sleep_duration 0.2 

python src/python/height_node.py \
  --server_address 'localhost' \
  --server_port 8769 \
  --A 17 \
  --B 27 \
  --sleep_duration 0.2 \
  --height_factor 1

python src/python/height_node.py \
  --server_address 'localhost' \
  --server_port 8770 \
  --A 0 \
  --B 5 \
  --sleep_duration 0.2 \
  --height_factor 1
