import click

from cassandra.config import load_config
from cassandra.recorder import DataRecorder


@click.command()
@click.option("--port", default=20777, help="port to listen on")
def run(port: int = 20777):
    config = load_config()
    recorder = DataRecorder(config, port=port)
    recorder.listen()


if __name__ == "__main__":
    run()
