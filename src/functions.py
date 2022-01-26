import os
import csv
import globals as g
import supervisely as sly
from PIL import Image
from supervisely.io.fs import download


def check_column_names(col_names_validate):
    if not any(image_url_name in g.possible_image_url_col_names for image_url_name in col_names_validate):
        raise Exception("IMAGE URL COLUMN NAME IS INVALID, PLEASE USE ONE OF:\n"
                        f"{g.possible_image_url_col_names}")
    if not any(tag_name in g.possible_tag_col_names for tag_name in col_names_validate):
        raise Exception("TAG COLUMN NAME IS INVALID, PLEASE USE ONE OF:\n"
                        f"{g.possible_tag_col_names}")


def validate_csv_table(first_csv_row):
    col_names_validate = [key.lower() for key in first_csv_row.keys()]
    col_names = [key for key in first_csv_row.keys()]

    check_column_names(col_names_validate)

    image_url_col_name = None
    tag_col_name = None
    for name in col_names:
        if name.lower().startswith("image") and name.lower().endswith("url"):
            image_url_col_name = name
        if name.lower().startswith("tag"):
            tag_col_name = name

    return image_url_col_name, tag_col_name


def download_file_from_link(link, save_path, file_name, app_logger):
    try:
        download(link, save_path)
        app_logger.info(f'{file_name} has been successfully downloaded')
    except Exception as e:
        sly.logger.warn(f"Could not download file {file_name}")
        sly.logger.warn(e)


def get_image_size(path_to_img):
    im = Image.open(path_to_img)
    w, h = im.size
    return h, w


def process_image_by_url(image_url, app_logger):
    image_url = image_url.strip()
    image_name = os.path.basename(os.path.normpath(image_url)) + ".png"
    image_path = os.path.join(g.img_dir, image_name)
    download_file_from_link(image_url, image_path, image_name, app_logger)
    success = os.path.isfile(image_path)

    return success, image_name, image_path


def process_ann(csv_row, project_meta, image_path, tag_col_name):
    tag_name = csv_row[tag_col_name].strip()
    image_shape = get_image_size(image_path)

    image_tag_meta = sly.TagMeta(tag_name, sly.TagValueType.NONE)
    try:
        project_meta = project_meta.add_tag_meta(image_tag_meta)
    except:
        pass

    tag_col = sly.TagCollection([sly.Tag(image_tag_meta)])

    ann = sly.Annotation((image_shape[0], image_shape[1]), img_tags=tag_col)
    return ann, project_meta
