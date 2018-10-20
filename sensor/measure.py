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

    while True:
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
        # Tell the program which function to associate with which direction
        sense.stick.direction_up = sense.clear(255, 0, 0)
        sense.stick.direction_down = sense.clear(0, 0, 255)
        sense.stick.direction_left = sense.clear(0, 255, 0)
        sense.stick.direction_right = sense.clear(255, 255, 0)
        sense.stick.direction_middle = sense.clear    # Press the enter key

