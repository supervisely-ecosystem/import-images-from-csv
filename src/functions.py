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


def flat_tag_list(unique_tags):
    tags = []
    for tag in unique_tags:
        if g.TAGS_DELIMITER in tag:
            tag = tag.split(g.TAGS_DELIMITER)
        else:
            tag = tag.split()
        tags.append(tag)

    unique_tags = []
    for sublist in tags:
        for tag in sublist:
            unique_tags.append(tag)

    unique_tags = list(set(unique_tags))
    return unique_tags


def process_ann(csv_row, project_meta, image_path, tag_col_name, need_tag):
    if csv_row[tag_col_name] is None or need_tag is False:
        image_shape = get_image_size(image_path)
        ann = sly.Annotation((image_shape[0], image_shape[1]))
        return ann, project_meta

    tags = []
    tag_names = csv_row[tag_col_name].strip()
    if g.TAGS_DELIMITER in tag_names:
        tag_names = tag_names.split(g.TAGS_DELIMITER)
    else:
        tag_names = tag_names.split()

    for tag_name in tag_names:
        tag_name.strip()
        tag_meta = project_meta.get_tag_meta(tag_name)
        if tag_meta is None:
            image_tag_meta = sly.TagMeta(tag_name, sly.TagValueType.NONE)
            project_meta = project_meta.add_tag_meta(image_tag_meta)
            tags.append(image_tag_meta)
        else:
            tags.append(tag_meta)

    image_shape = get_image_size(image_path)
    tag_col = sly.TagCollection(tags)
    ann = sly.Annotation((image_shape[0], image_shape[1]), img_tags=tag_col)
    return ann, project_meta
