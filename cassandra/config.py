import configparser

from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

HOME: str = Path.home()
CONFIG_FILE_NAME: str = 'config.ini'


def load_config(filename: str = HOME / '.config' / 'cassandra' / CONFIG_FILE_NAME):
    config = configparser.ConfigParser()
    config_file = Path(filename)

    if config_file.is_file():
        config.read(filename)
        return config
    else:
        logger.error('Unable to fine config file.')
