import dht
import utime as time
from .readings import Multiplexer
from .sensor import Sensor


class DHT(Multiplexer):

    def __init__(self, dht_version, data_pin):
        self.__pin = data_pin
        dht_cls = getattr(dht, 'DHT{}'.format(str(dht_version)))
        self.__dht = dht_cls(data_pin)
        self.__dht.measure()
        self.last_measurement = time.time()

        channel_map = {
            "temperature": self.temperature,
            "humidity": self.humidity
        }
        super().__init__(channel_map)

    def measure(self):
        current_time = time.time()
        if self.last_measurement - current_time > 2:
            self.__dht.measure()
            self.last_measurement = current_time

    def temperature(self):
        self.measure()
        return self.__dht.temperature()

    def humidity(self):
        self.measure()
        return self.__dht.humidity()


class TemperatureSensor(Sensor):
    pass


class HumiditySensor(Sensor):
    pass
