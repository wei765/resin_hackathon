
import os
import time
from sense_hat import SenseHat
from influxdb import InfluxDBClient
import datetime

influx_client = InfluxDBClient('influxdb', 8086, database='balena-sense')
influx_client.create_database('balena-sense')

sense = SenseHat()


blue = (0, 0, 255)
yellow = (255, 255, 0)
count = 0

sense.clear()
sense.show_message("Hi Wei!", text_colour=yellow, back_colour=blue)
sense.load_image("heart.png")
time.sleep(2)

while 1:
    sense.show_message("Start:{}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    measurements = [
        {
            'measurement': 'temperature',
            'fields': {
                'value': float(sense.temperature)
            }
        }
    ]

    measurements.extend([
        {
            'measurement': 'humidity',
            'fields': {
                'value': float(sense.humidity)
            }
        }
    ])

    measurements.extend([
        {
            'measurement': 'pressure',
            'fields': {
                'value': float(sense.pressure)
            }
        }
    ])

    sense.set_pixel(0, count, 0, 255, 0)
    count = count+1
    if count == 8:
        count = 0
    sense.set_pixel(0, count, 0, 0, 0)
    influx_client.write_points(measurements)

    time.sleep(1)
    sense.show_message("Temperatue: {}".format(int(sense.temperature)))

    red = (255, 0, 0)
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x = round(x,2)
    y = round(y,2)
    z = round(z,2)
    sense.show_message("Vel: x={x}, y={y}, z={z}".format(x=x,y=y,z=z))
    if abs(x) > 0.01 or abs(y) > 0.01 or abs(z) > 0.01:
        sense.show_letter("!", red)
        time.sleep(2)
    else:
        sense.clear()
    sense.show_message("End", text_colour=yellow)
    time.sleep(5)

# e = (0, 0, 0)
# w = (255, 255, 255)
# sense.clear()
# while True:
#     for event in sense.stick.get_events():
#         # Check if the joystick was pressed
#         if event.action == "pressed":
        
#             # Check which direction
#             if event.direction == "up":
#                 sense.show_letter("U")      # Up arrow
#             elif event.direction == "down":
#                 sense.show_letter("D")      # Down arrow
#             elif event.direction == "left": 
#                 sense.show_letter("L")      # Left arrow
#             elif event.direction == "right":
#                 sense.show_letter("R")      # Right arrow
#             elif event.direction == "middle":
#                 sense.show_letter("M")      # Enter key
        
#             # Wait a while and then clear the screen
#             time.sleep(0.5)
#             sense.clear()
