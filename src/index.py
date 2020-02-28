"""
    Loads CV as a web for testing purpouses
"""

from flask import Flask, render_template

import config as c
from utilities import get_content

APP = Flask(__name__)


@APP.route("/v/<name>")
def show(name=None, preview=True):
    """ Render a CV for previews """
    return render_template(c.FILE_DEFAULT_TEMPLATE, **get_content())


@APP.route("/")


@APP.route("/print/<name>")
def mprint(name=None):
    """ Display a CV without any frame for printing """
    return show(name, preview=False)


@APP.route("/print.html")
def print_sample():
    """ Display the sample CV without any frame for printing """
    return mprint()


@APP.route("/")
def show_sample():
    """ Render the sample CV for previews """
    return show(None)


if __name__ == "__main__":
    APP.run(debug=True)
