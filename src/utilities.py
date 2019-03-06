""" Load data from yamls as ordered dicts """

import oyaml as yaml
from markdown import markdown

import config as c


def _read_yaml(uri):
    """ auxiliar function to raad a yaml """

    with open(uri, encoding="utf-8") as file:
        return yaml.load(file)


def _transform_from_markdown(data):
    """ Transform markdown text to html """

    # Main description of CV
    if "description" in data:
        data["description"] = markdown(data["description"])

    # Descriptions in body
    for block_name, block_data in data["body"].items():
        for x in block_data:
            if "description" in x:
                x["description"] = markdown(x["description"])


def get_content(name=None):
    """ Return content of the CV """

    if name is None:
        name = c.FILE_DEFAULT
        path = c.PATH_CONTENT

    else:
        # No extension if present
        name = name.split(".")[0]
        path = c.PATH_INPUT

    # Read data
    out = _read_yaml(f"{path}{name}.yaml")
    _transform_from_markdown(out)

    # Add config data
    out["config"] = _read_yaml(c.FILE_CONFIG)

    return out
