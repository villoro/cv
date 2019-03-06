"""
    Loads CV as a web for testing purpouses
"""

from flask import Flask, render_template

import config as c
from utilities import get_content

APP = Flask(__name__)


@APP.route("/print.html")
def print_sample():
    """ Display the sample CV without any frame for printing """

    return render_template(c.FILE_DEFAULT_TEMPLATE, **get_content())


@APP.route("/")
def preview_sample():
    """ Render the sample CV for previews """

    return render_template(c.FILE_DEFAULT_TEMPLATE, preview=True, **get_content())


@APP.route("/print/<name>")
def print(name):
    """ Display a CV without any frame for printing """

    return render_template(c.FILE_DEFAULT_TEMPLATE, **get_content(name))


@APP.route("/v/<name>")
def preview(name):
    """ Render a CV for previews """

    return render_template(c.FILE_DEFAULT_TEMPLATE, preview=True, **get_content(name))


if __name__ == "__main__":
    APP.run(debug=True)
