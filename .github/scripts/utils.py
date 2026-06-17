import json
import os

from loguru import logger as log

PACKAGE_JSON = "package.json"


def read_package_json():
    if not os.path.exists(PACKAGE_JSON):
        return {}
    with open(PACKAGE_JSON, encoding="utf8") as stream:
        return json.load(stream)


def set_output(name, value):
    log.info(f"Setting {name=} {value=}")
    with open(os.environ["GITHUB_ENV"], "a") as fh:
        print(f"{name}={value}", file=fh)


def get_version():
    # Fall back to 0.0.0 when package.json is missing (e.g. comparing against a
    # historical 'main' that predates the Astro migration).
    return read_package_json().get("version", "0.0.0")
