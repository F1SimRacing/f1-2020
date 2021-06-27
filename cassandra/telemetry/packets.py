class Packet:
    def __init__(self, packet):
        for i in packet.header._fields_:
            setattr(self, i[0], getattr(packet.header, i[0]))

    def as_dict(self):
        return self.__dict__


class HeaderData(Packet):
    pass


class CarStatusData(Packet):
    pass


class CarTelemetryData(Packet):
    def __init__(self, packet):
        for i in packet._fields_:
            setattr(self, i[0], getattr(packet, i[0]))

    def __repr__(self):
        return "car_telemetry_data"
