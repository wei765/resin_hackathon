import os
import time
from sense_hat import SenseHat
from influxdb import InfluxDBClient

influx_client = InfluxDBClient('influxdb', 8086, database='balena-sense')
influx_client.create_database('balena-sense')

sense = SenseHat()

sense.clear()
sense.load_image("balena.png")
time.sleep(2)
sense.show_message("balena")

blue = (0, 0, 255)
yellow = (255, 255, 0)
count = 0
while 1:
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
    sense.show_message("Hello Wei", text_colour=yellow, back_colour=blue)
    sense.show_message("Temperatue: {}".format(int(sense.temperature)))

    red = (255, 0, 0)


    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x = round(x,2)
    y = round(y,2)
    z = round(z,2)
    sense.show_message("Tu velcidad: x={x}, y={y}, z={z}".format(x=x,y=y,z=z) )
    if x > 0.01 or y > 0.01 or z > 0.01:
        sense.show_letter("!", red,scroll_speed=1)
    else:
        sense.clear()
    time.sleep(2)

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
