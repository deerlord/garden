from dataclasses import dataclass
from .. import Sensor
import json
import os.path


@dataclass
class Moisture(Sensor):
    voltage: float

    def __post_init__(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        with open(f'{cwd}/moisture_voltages.json') as f:
            config = json.load(f)
        self.__value_map = config[str(self.voltage)]

    def __clamp_value(self, value):
        return max(0, min(self.__value_map['100'], value))

    def _transform(self, value):
        value = (value * float(self.__value_map['100']))
        return value

print('making Moisture')
moisture = Moisture(getter=lambda: 0.0, voltage=3.3)
print(moisture.value)
