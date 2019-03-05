""" Load data from yamls as ordered dicts """

import oyaml as yaml

import config as c


def _read_yaml(uri):
    """ auxiliar function to raad a yaml """

    with open(uri, encoding="utf-8") as file:
        return yaml.load(file)


def get_content(name=None):
    """ Return content of the CV """

    if name is None:
        name = c.DEFAULT_FILE
        path = c.PATH_CONTENT

    else:
        # No extension if present
        name = name.split(".")[0]
        path = c.PATH_INPUT

    # Read data
    out = _read_yaml(f"{path}{name}.yaml")

    # Add config data
    out["config"] = _read_yaml(c.CONFIG_FILE)

    return out
