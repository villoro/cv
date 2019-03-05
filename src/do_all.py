""" Create all CVs from the input folder """

import os
from subprocess import call

import config as c

WKHTML_CONFIG = {
    "--javascript-delay": 5000,  # With a high number we allow the fonts to load
    "--dpi": 300,  # Having this number high prevents resolution problems
    "--disable-smart-shrinking": "",
    "--print-media-type": "",
    "-T": 0,
    "-B": 0,
    "-L": 0,
    "-R": 0,
}

# PATH_WKHTML needs to be around " "
# The other part is a concat of all options
RAW_COMAND = [f'"{c.PATH_WKHTML}"'] + [f"{i} {x}".strip() for i, x in WKHTML_CONFIG.items()]


def main():

    # Do all in input folder
    for filename in os.listdir(c.PATH_INPUT):

        # No extension if present
        name = filename.split(".")[0]

        input_url = f"{c.URL_PRINT}{name}.html"
        output_file = f"{c.PATH_OUTPUT}{name}.pdf"

        print(f"\n-- Creating {name}.pdf --")
        call(" ".join(RAW_COMAND + [input_url, output_file]).strip(), shell=True)


if __name__ == "__main__":
    main()
