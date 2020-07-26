from .readings import ReadingConsumer, ReadingProducer


class Sensor(ReadingConsumer):

    def __init__(self, name: str):
        self.name = name
        self.reading_producer = None

    def set_producer(self, reading_producer: ReadingProducer):
        self.reading_producer = reading_producer

    def read(self):
        reading = self.reading_producer.get_value(self)
        return self._read(reading)

    def _read(self, reading):
        return reading
