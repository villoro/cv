""" Load data from yamls as ordered dicts """

import oyaml as yaml

PATH_CONTENT = "src/content/"


def _read_yaml(uri):
    """ auxiliar function to raad a yaml """

    with open(uri, encoding="utf-8") as file:
        return yaml.load(file)


def get_content():
    """ Return content of the CV """
    return _read_yaml(f"{PATH_CONTENT}data.yaml")


def get_config():
    """ Return configuration of the page """
    return _read_yaml(f"{PATH_CONTENT}config.yaml")
