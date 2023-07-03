import os
import yaml

from pydantic import BaseModel, validator, root_validator
from tqdm import tqdm
from typing import Literal, Union
from vpalette import get_colors

from image_transformations import (
    get_image,
    remove_bg,
    to_grayscale,
    add_background_color,
    round_image,
)

YAML_FILE = "jobs.yaml"


class RoundImage(BaseModel):
    action: Literal["round"]
    suffix: str = "_round"

    def run(self, image_in):
        return round_image(image_in)


class RemoveBg(BaseModel):
    action: Literal["remove_bg"]
    suffix: str = "_no_bg"
    alpha_matting: bool = True
    alpha_matting_erode_size = 40

    def run(self, image_in):
        return remove_bg(
            image_in,
            alpha_matting=self.alpha_matting,
            alpha_matting_erode_size=self.alpha_matting_erode_size,
        )


class AddColorGeneric(BaseModel):
    color: str = None
    color_name: str = None
    color_index: int = None

    @validator("color", pre=True, always=True)
    def populate_color(cls, v, values):
        """Infer color form color_name and color_index"""

        color_name = values.get("color_name")
        color_index = values.get("color_index")

        if (color_name is None) and (color_index is None):
            return v

        elif color_name is None:
            raise ValueError("'color_name' can't be null when 'color_index' is not null")

        elif color_index is None:
            raise ValueError("'color_index' can't be null when 'color_name' is not null")

        return get_colors((color_name, color_index))


class AddBackgroundColor(AddColorGeneric):
    action: Literal["add_background_color"]
    suffix: str = None

    @validator("suffix", pre=True, always=True)
    def populate_suffix(cls, v, values):
        """Infer color form color_name and color_index"""

        color_name = values.get("color_name")
        color_index = values.get("color_index")
        color = values.get("color")

        if color_name and color_index:
            return f"__{color_name}_{color_index}"

        elif color:
            return f"__{color}"

        raise ValueError("Invalid color configuration")

    def run(self, image_in):
        return add_background_color(image_in, background_color=self.color)


class ToGrayscale(AddColorGeneric):
    action: Literal["to_grayscale"]
    suffix: str = None

    @validator("suffix", pre=True, always=True)
    def populate_suffix(cls, v, values):
        """Infer color form color_name and color_index"""

        color_name = values.get("color_name")
        color_index = values.get("color_index")
        color = values.get("color")

        if color_name and color_index:
            return f"_grayscale__{color_name}_{color_index}"

        elif color:
            return f"_grayscale__{color}"

        return "_grayscale"

    def run(self, image_in):
        return to_grayscale(image_in, background_color=self.color)


class Job(BaseModel):
    transformations: list[Union[RoundImage, RemoveBg, AddBackgroundColor, ToGrayscale]]
    extension: str = None
    reprocess: bool = False

    @validator("extension", pre=True, always=True)
    def populate_extension(cls, v, values):
        transformations = values.get("transformations")
        last_transformation = transformations[-1]

        if isinstance(last_transformation, RoundImage) or isinstance(last_transformation, RemoveBg):
            return "png"
        return "jpg"

    @property
    def suffixes(self):
        out = ""
        for x in self.transformations:
            if x.action == "remove_bg":
                if len(self.transformations) == 0:
                    return x.suffix

            else:
                out += x.suffix

        return out

    def process(self, path_in, folder_out, name):
        folder_out = folder_out.rstrip("/")
        path_out = f"{folder_out}/{name}{self.suffixes}.{self.extension}"

        if not (self.reprocess or not os.path.exists(path_out)):
            return False

        image = get_image(path_in)

        for transformation in self.transformations:
            image = transformation.run(image)

        if self.extension in ("jpg", "jpeg"):
            image = image.convert("RGB")

        image.save(path_out)
        return True


class Jobs(BaseModel):
    path_in: str
    folder_out: str
    jobs: list[Job]

    def do_all(self, tqdm_class=tqdm):
        name = self.path_in.split("/")[-1].rsplit(".", maxsplit=1)[0]

        for job in tqdm_class(self.jobs):
            job.process(path_in=self.path_in, folder_out=self.folder_out, name=name)


if __name__ == "__main__":
    with open(YAML_FILE) as f:
        data = yaml.safe_load(f)

    jobs = Jobs(**data)
    jobs.do_all()
