from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from time import time
from functools import partial
from math import floor
from typing import List, Any
import gpiozero



@dataclass
class AnalogInput():
    channel: int
    select_pin: int

    def value(self):
        mcp = gpiozero.MCP3008(
            channel=self.channel,
            select_pin=self.select_pin
        )
        value = mcp.value
        mcp.close()
        return value


def select_pins(total: int = 2):
    default = [8, 7]
    if total > 2:
        total = total - 2
        start_pin = 12
        for pin in range(
            start_pin,
            min((total + start_pin), 26),
            1  
        ):
            default.append(pin)
    return default


@dataclass
class Multiplexer():
    channels: int = 8
    devices: int = 2

    @property
    def max_channels(self):
        return self.channels * self.devices

    def __post_init__(self):
        self.select_pins = select_pins(
            total=self.devices
        )
        self.__inputs = []
        for channel in range(0, self.max_channels, 1): 
            device = floor(channel / self.channels)
            channel = channel % self.channels
            self.__inputs.append(AnalogInput(
                channel=channel,
                select_pin=self.select_pins[device]
            ))

    def __getitem__(self, channel: int):
        if channel >= 0 and channel < len(self.__inputs):
            return self.__inputs[channel].value()

    def __iter__(self):
        return (
            self.__inputs[channel].value
            for channel in range(0, self.max_channels, 1)
        )


@dataclass
class Sensor(metaclass=ABCMeta):
    channel: int
    multiplexer: Multiplexer
   
    @abstractmethod
    def __transform(self, value):
        return value

    @property
    def value(self):
        return self.__transform(
            value=self.multiplexer[self.channel]
        )




m = Multiplexer()
for  i in range(0, 16, 1):
    print(i, m[i])
