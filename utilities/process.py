import yaml

from tqdm import tqdm

from images_jobs import ImageJobConfig, Job

YAML_FILE = "jobs.yaml"


def get_jobs_from_yaml():
    """Get all jobs info"""

    with open(YAML_FILE) as f:
        return yaml.safe_load(f)


def do_all(data=None, tqdm_class=tqdm):

    if data is None:
        data_all = get_jobs_from_yaml()

    for data in tqdm_class(data_all):
        for x in tqdm_class(data.get("configs")):
            config = ImageJobConfig(**x)

            Job(data.get("path_in"), config, data.get("reprocess")).process()


if __name__ == "__main__":
    do_all()
