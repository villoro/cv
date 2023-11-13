import click

from packaging import version
from loguru import logger as log

from utils import set_output


@click.command()
@click.option("--version_current")
@click.option("--version_main")
@click.option("--project", default="dbt", help="'dbt' or 'docker'")
def compare_versions(version_current, version_main, project):
    log.info(f"Running with {version_current=}, {version_main=}")

    version_current = version.parse(version_current)
    version_main = version.parse(version_main)

    needs_update = version_current <= version_main

    log.info(f"Outcome {needs_update}")

    set_output("NEEDS_UPDATE", str(needs_update).lower())


if __name__ == "__main__":
    compare_versions()
