import click
from loguru import logger as log

from utils import set_output, get_version


@click.command()
@click.option("--name")
def export_version(name):
    version = get_version()
    log.info(f"'{name}' branch {version=}")

    set_output(f"VERSION_{name.upper()}", version)


if __name__ == "__main__":
    export_version()
