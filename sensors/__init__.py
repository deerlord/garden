from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from time import time
from functools import partial
from math import floor
from typing import List, Any
import gpiozero


@dataclass
class MCP():
    select_pin: int
    channels: int
    voltage: float

    def __post_init__(self):
        chip_name = f'MCP300{self.channels}'
        self.__chip = getattr(gpiozero, chip_name)

    def __getitem__(self, channel):
        mcp = self.__chip(
            channel=channel,
            select_pin=self.select_pin
        )
        value = mcp.value
        mcp.close()
        return round(value, 2)


@dataclass
class Multiplexer():
    channels: int = 8
    devices: int = 2
    voltage: float = 3.3

    @property
    def select_pins(self):
        pins = [8, 7]
        total = self.devices - 2
        start_pin = 12
        for pin in range(
            start_pin,
            min((total + start_pin), 25),
            1
        ):
            pins.append(pin)
        return pins

    def __post_init__(self):
        self.__chips = []
        for pin in self.select_pins:
            chip = MCP(
                select_pin=pin,
                channels=self.channels,
                voltage=self.voltage
            )
            self.__chips.append(chip)

    def __getitem__(self, channel):
        device = floor(channel / self.channels)
        channel = channel % self.channels
        return self.__chips[device][channel]

    def __iter__(self):
        return (value for value in self.__chips)


def main():
    import influxdb
    import socket
    from time import sleep

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
