import os

from rembg import remove
from PIL import Image
from v_palette import get_colors


def get_folder_out_and_name(path_in):
    """Gets the path where data should be stored and the base name"""

    folder_in = "/".join(path_in.split("/")[:-1])
    folder_out = f"{folder_in}/transformed"

    if not os.path.exists(folder_out):
        os.makedirs(folder_out)

    name = path_in.split("/")[-1].split(".")[0]

    return folder_out, name


def get_image(path_in):
    """Gets a pillow image"""
    return Image.open(path_in)


def remove_bg(image_in, alpha_matting=True, alpha_matting_erode_size=40):
    """Remove image background"""
    return remove(
        image_in, alpha_matting=alpha_matting, alpha_matting_erode_size=alpha_matting_erode_size
    )


def add_background(image_in, background_color, mask=None):
    """Fill background with solid color"""

    if mask is None:
        mask = image_in

    if type(background_color) is tuple:
        background_color = get_colors(background_color)

    image_out = Image.new("RGBA", image_in.size, background_color)
    image_out.paste(image_in, mask=mask)

    return image_out


def to_grayscale(image_in, background_color=None):
    """Turn image to grayscale"""

    return add_background(image_in.convert("L"), background_color=background_color, mask=image_in)
