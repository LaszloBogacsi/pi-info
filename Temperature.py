class Temperature(object):

    def __init__(self, id, temperature, sensor_status, published_time, sensor_id):
        self.published_time = published_time
        self.sensor_id = sensor_id
        self.sensor_status = sensor_status
        self.temperature = temperature
        self.id = id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
