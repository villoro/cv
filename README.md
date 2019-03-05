# Easy CV

Create a `pdf` CV based on some `html` templates and data from `yaml`.

Screenshot of the result:
![home](assets/preview.jpg)

You can view the full pdf [here](assets/sample.pdf).

## Installation
1. Install all python packages with

	pip install -r requirements.txt

2. Install [wkhtmltopdf](https://wkhtmltopdf.org/)

## Usage

1. First start the `flask` server from the root folder with:

	python src/index.py

2. Open `http://localhost:5000/` to preview the result

3. Run `create_sample.sh` to create the pdf

> You should change the `wkhtmltopdf` path inside `create_sample.sh`.

4. You will now have `assets/sample.pdf` with the result

## Configuration
There are two files to `src/sample_data.yaml` and `src/config.yaml`.

The first one (`sample_data.yaml`) has the actual content of the CV.
The second (`config.yaml`) allow users to change some parts of the template.

If you want further configuration you can edit the templates (`src/templates/base.html` and `src/templates/cv.html`) directly or create your own templates (recommended).

## Authors
* [Arnau Villoro](villoro.com)

## License
The content of this repository is licensed under a [MIT](https://opensource.org/licenses/MIT).

## Nomenclature
Branches and commits use some prefixes to keep everything better organized.

### Branches
* **f/:** features
* **r/:** releases
* **h/:** hotfixs

### Commits
* **[NEW]** new features
* **[FIX]** fixes
* **[REF]** refactors
* **[PYL]** [pylint](https://www.pylint.org/) improvements
* **[TST]** tests
