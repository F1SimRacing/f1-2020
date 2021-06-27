import configparser

from pathlib import Path
from dataclasses import dataclass
import logging
from typing import Union

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

HOME: str = Path.home()
CONFIG_FILE_NAME: str = 'config.ini'


@dataclass
class KafkaConfiguration:
    bootstrap_servers: str


@dataclass
class InfluxDBConfiguration:
    host: str
    token: str
    org: str
    bucket: str


@dataclass
class RecorderConfiguration:
    kafka: Union[KafkaConfiguration, None] = None
    influxdb: Union[InfluxDBConfiguration, None] = None


def load_config(filename: str = HOME / '.config' / 'cassandra' / CONFIG_FILE_NAME) \
        -> RecorderConfiguration:
    config = configparser.ConfigParser()
    config_file = Path(filename)

    if config_file.is_file():
        config.read(filename)
    else:
        logger.error('Unable to fine config file.')
        return RecorderConfiguration()

    recorder_config = RecorderConfiguration()

    for section in config.keys():
        if section == 'kafka':
            recorder_config.kafka = KafkaConfiguration(
                config[section]['bootstrap_servers'])

        if section == 'influxdb':
            recorder_config.influxdb = InfluxDBConfiguration(
                config[section]['host'],
                config[section]['token'],
                config[section]['org'],
                config[section]['bucket']
            )

    return recorder_config
