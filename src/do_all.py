""" Create all CVs from the input folder """

import os
from subprocess import call

import config as c

WKHTML_CONFIG = {
    "--javascript-delay": 5000,
    "--disable-smart-shrinking": "",
    "--print-media-type": "",
    "--dpi": 300,
    "-T": 0,
    "-B": 0,
    "-L": 0,
    "-R": 0,
}

RAW_COMAND = [f'"{c.PATH_WKHTML}"'] + [f"{i} {x}".strip() for i, x in WKHTML_CONFIG.items()]


def main():

    for filename in os.listdir(c.PATH_INPUT):
        # No extension if present
        name = filename.split(".")[0]

        input_url = f"{c.URL_PRINT}{name}.html"
        output_file = f"{c.PATH_OUTPUT}{name}.pdf"

        print(f"\n-- Creating {name}.pdf --")
        call(" ".join(RAW_COMAND + [input_url, output_file]).strip(), shell=True)


if __name__ == "__main__":
    main()
