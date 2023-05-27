"""
All constants that can be modified

For the data, I'm using a submodule (more info in https://www.youtube.com/watch?v=eJrh5IjWSGM).
If you want to use the sample, uncomment the PATH_DATA = "sample"
"""

# Paths
PATH_DATA = "cv_private"
# PATH_DATA = "sample"  # Uncomment if you want to use the sample folder
PATH_INPUT = f"{PATH_DATA}/input/"
PATH_OUTPUT = f"{PATH_DATA}/output/"
PATH_CONTENT = "src/"
PATH_WKHTML = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"


# Files
FILE_DEFAULT = "sample_1"
FILE_CONFIG = f"{PATH_CONTENT}config.yaml"


# URL
URL_PRINT = "localhost:5000/print/"
