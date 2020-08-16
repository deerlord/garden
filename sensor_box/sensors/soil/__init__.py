from .. import Sensor


class Moisture(Sensor):
    def _transform(self, value):
        return value


moisture = Moisture(getter=lambda: 0.0)
print(moisture.value)
