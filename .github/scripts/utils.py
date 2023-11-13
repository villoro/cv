import os

import toml
from loguru import logger as log

PYPROJECT_FILE = "pyproject.toml"


def read_pyproject():
    return toml.load(PYPROJECT_FILE)


def set_output(name, value):
    log.info(f"Setting {name=} {value=}")
    with open(os.environ["GITHUB_ENV"], "a") as fh:
        print(f"{name}={value}", file=fh)


def get_version_from_toml(project="dbt"):
    config = read_pyproject()

    if project == "dbt":
        log.info("Retrieving dbt/python version")
        aux = config["tool"]["poetry"]
    elif project == "docker":
        log.info("Retrieving docker version")
        aux = config["docker"]
    else:
        log.error(f"{project=} must be 'dbt' or 'docker'")

    return aux["version"]


def save_pyproject(data):
    log.info(f"Exporting '{PYPROJECT_FILE}'")
    with open(PYPROJECT_FILE, "w", encoding="utf8") as stream:
        toml.dump(data, stream)
