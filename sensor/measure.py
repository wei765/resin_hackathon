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

        x = abs(x)
        y = abs(y)
        z = abs(z)
        sense.show_message("Tu velcidad: x={x}, y={y}, z={z}".format(x=x,y=y,z=z) )
        if x > 1 or y > 1 or z > 1:
            sense.show_letter("!", red)
        else:
            sense.clear()
    time.sleep(5)
