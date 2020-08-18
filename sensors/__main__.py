import influxdb
import socket
from time import sleep
from gpiozero import LED
from . import Multiplexer


client = influxdb.InfluxDBClient(
    host='influxdb',
    port=443,
    ssl=True,
    verify_ssl=True,
    database='gardens'
)
multiplexer = Multiplexer(voltage=3.3)
devices = LED(26)
while True:
    devices.on()
    data_wrapper = [{
        'measurement': garden_boxes,
        'tags': [socket.gethostname()],
        'time': time,
        'fields': {index: value for index, value in enumerate((multiplexer))}
    }]
    devices.off()
    client.write_points(data_wrapper)
    sleep(3600)
