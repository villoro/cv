"""
    Loads CV as a web for testing purpouses
"""

from flask import Flask, render_template

from utilities import get_content, get_config

APP = Flask(__name__)


@APP.route("/print.html")
def print():
    """ Display CV without any frame for printing """

    content = get_content()
    config = get_config()

    return render_template("cv.html", config=config, **content)


@APP.route("/")
def preview():
    """ Render the CV before converting to html """

    content = get_content()
    config = get_config()

    return render_template("cv.html", preview=True, config=config, **content)


if __name__ == "__main__":
    APP.run(debug=True)
