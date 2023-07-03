import os

from pydantic import BaseModel, validator, root_validator

from image_transformations import (
    get_image,
    remove_bg,
    to_grayscale,
    add_background_color,
    round_image,
)
from vpalette import get_colors


def get_folder_out_and_name(path_in):
    """Gets the path where data should be stored and the base name"""

    aux = path_in.split("/")

    name = aux[-1].split(".")[0]
    folder_in = "/".join(aux[:-1])

    folder_out = f"{folder_in}/{name}"

    if not os.path.exists(folder_out):
        os.makedirs(folder_out)

    return folder_out, name


class ImageJobConfig(BaseModel):
    """Config for jobs that process images"""

    background: bool = False
    round: bool = False
    color: str = None
    color_name: str = None
    color_index: int = None
    grayscale: bool = False

    @root_validator
    def populate_color(cls, values):

        color_name = values.get("color_name")
        color_index = values.get("color_index")

        if (color_name is None) and (color_index is None):
            return values

        if color_name is None:
            raise ValueError("'color_name' can't be null when 'color_index' is not null")

        if color_index is None:
            raise ValueError("'color_index' can't be null when 'color_name' is not null")

        # Update color
        values["color"] = get_colors((color_name, color_index))

        return values

    @root_validator
    def round_only_if_background(cls, values):

        if not values.get("round"):
            return values

        for x in ["color", "background"]:
            if values.get(x):
                return values

        raise ValueError(f"Round is only allowed when there is background")


class Job:
    """Use for doing multiple transformations"""

    def __init__(self, path_in, job_config, reprocess=True):

        self.job_config = job_config

        self.folder_out, self.base_name = get_folder_out_and_name(path_in)
        self.image_in = get_image(path_in)

        self.reprocess = reprocess

    @property
    def path_out(self):
        """Infer out name based on the config"""
        out = f"{self.folder_out}/{self.base_name}"

        format_out = ".jpg"

        if self.job_config.color_name or self.job_config.color_index:
            out += f"__{self.job_config.color_name}_{self.job_config.color_index}"
        else:
            if self.job_config.color:
                out += f"__{self.job_config.color}"

        if self.job_config.background and not self.job_config.color:
            out += "_no_bg"
            format_out = ".png"

        if self.job_config.round:
            out += "_round"
            format_out = ".png"

        if self.job_config.grayscale:
            out += "_grayscale"

        return out + format_out

    @property
    def needs_reprocessing(self):
        return self.reprocess or not os.path.exists(self.path_out)

    def transform(self):
        """Aply all asked transformations"""

        if not self.needs_reprocessing:
            self.image_out = get_image(self.path_out)
            return False

        image = self.image_in

        if not self.job_config.background:
            image = remove_bg(image)

        if self.job_config.grayscale:
            image = to_grayscale(image, background_color=self.job_config.color)

        elif self.job_config.color:
            image = add_background_color(image, self.job_config.color)

        if self.job_config.round:
            image = round_image(image)

        self.image_out = image
        return True

    def export(self):
        """Export result"""

        if self.path_out.endswith(".jpg"):
            self.image_out = self.image_out.convert("RGB")

        if self.needs_reprocessing:
            self.image_out.save(self.path_out)

    def process(self):
        """Transform and export"""
        self.transform()
        self.export()
