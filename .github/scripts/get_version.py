import click
from loguru import logger as log

from utils import set_output, get_version_from_toml


@click.command()
@click.option("--name")
@click.option("--project", default="dbt", help="'dbt' or 'docker'")
def export_version(name, project):
    version = get_version_from_toml(project)
    log.info(f"'{name}' branch {version=}")

    set_output(f"VERSION_{name.upper()}", version)


if __name__ == "__main__":
    export_version()
