import influxdb
import socket
from time import sleep
from . import Multiplexer


client = influxdb.InfluxDBClient(
    host='influxdb',
    port=443,
    ssl=True,
    verify_ssl=True,
    database='gardens'
)
multiplexer = Multiplexer(voltage=3.3)
while True:
    data_wrapper = [{
        'measurement': garden_boxes,
        'tags': [socket.gethostname()],
        'time': time,
        'fields': {index: value for index, value in enumerate((multiplexer))}
    }]
    client.write_points(data_wrapper)
    sleep(3600)
