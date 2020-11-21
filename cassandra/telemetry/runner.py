from cassandra.telemetry.source import Feed


def main():
    feed = Feed()
    while True:
        packet = feed.get_latest()
        if 'carTelemetryData' in packet:
            tele = packet['carTelemetryData'][19]
            #print(f'{tele.engineRPM} rpm')


if __name__ == '__main__':
    main()