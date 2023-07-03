import os

from pydantic import BaseModel, validator, root_validator
from typing import Literal, Union
from tqdm import tqdm
from vpalette import get_colors

from image_transformations import (
    get_image,
    remove_bg,
    to_grayscale,
    add_background_color,
    round_image,
)


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
    path_in: str
    folder_out: str

    transformations: list[Union[RoundImage, RemoveBg, AddBackgroundColor, ToGrayscale]]
    name_out: str = None
    extension: str = None
    path_out: str = None
    reprocess: bool = False

    @validator("extension", pre=True, always=True)
    def populate_extension(cls, v, values):
        transformations = values.get("transformations")
        last_transformation = transformations[-1]

        if isinstance(last_transformation, RoundImage) or isinstance(last_transformation, RemoveBg):
            return "png"
        return "jpg"

    @validator("name_out", pre=True, always=True)
    def populate_name_out(cls, v, values):
        transformations = values.get("transformations")
        path_in = values.get("path_in")

        out = path_in.split("/")[-1].rsplit(".", maxsplit=1)[0]
        for x in transformations:
            if x.action == "remove_bg":
                if len(transformations) == 0:
                    return x.suffix

            else:
                out += x.suffix

        return out

    @validator("path_out", pre=True, always=True)
    def populate_path_out(cls, v, values):
        folder_out = values.get("folder_out").rstrip("/")
        name_out = values.get("name_out")
        extension = values.get("extension")

        return f"{folder_out}/{name_out}.{extension}"

    @property
    def needs_reprocessing(self):
        return self.reprocess or not os.path.exists(self.path_out)

    def process(self):
        if not self.needs_reprocessing:
            return get_image(self.path_out)

        image = get_image(self.path_in)

        for transformation in self.transformations:
            image = transformation.run(image)

        if self.extension in ("jpg", "jpeg"):
            image = image.convert("RGB")

        if self.reprocess:
            image.save(self.path_out)
        return image
