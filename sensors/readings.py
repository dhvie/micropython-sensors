import machine
import time


class ReadingProducer:
    def get_value(self, sensor):
        raise NotImplementedError()


class ReadingConsumer:
    def set_producer(self, value_producer: ReadingProducer):
        raise NotImplementedError()


class Multiplexer(ReadingProducer):

    def __init__(self, channel_map):
        self.__channel_map = channel_map
        self._channels_by_sensor = {}

    @property
    def channels(self):
        return self.__channel_map.keys()

    def register(self, sensor, channel):
        self._channels_by_sensor[sensor.name] = channel
        sensor.set_producer(self)

    def deregister(self, sensor):
        if sensor.name in self._channels_by_sensor:
            del self._channels_by_sensor[sensor.name]
            sensor.set_producer(None)

    def get_value(self, sensor):
        channel = self._channels_by_sensor.get(sensor.name, None)
        if channel is None:
            return None

        return self.__channel_map[channel]()


class AnalogMultiplexer(Multiplexer):
    class channel_map:

        def __init__(self, num_channels, amux):
            self.__all_channels = range(num_channels)
            self.__amux = amux

        def __getitem__(self, item):
            def read():
                self.__amux.select_channel(item)
                time.sleep(self.__amux.read_delay)
                return self.__amux.read()

            return read

        def keys(self):
            return self.__all_channels

    def __init__(self, channel_pins, read_delay=0.05):
        self.masks = tuple((0b1 << idx for idx in range(len(channel_pins))))
        self.channel_pins = channel_pins
        self.adc = machine.ADC(0)
        self.read_delay = read_delay
        super().__init__(AnalogMultiplexer.channel_map(len(channel_pins), self))

    def select_channel(self, channel):
        for idx, pin in enumerate(self.channel_pins):
            pin.value(1 if channel & self.masks[idx] else 0)

    def read(self):
        return self.adc.read()
