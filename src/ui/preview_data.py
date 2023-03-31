import csv
import os.path

import sly_globals as g
import supervisely as sly


def create_project_meta_from_csv_tags(total_tags):
    tag_metas = []
    for tag_name in total_tags:
        tag_meta = sly.TagMeta(tag_name, sly.TagValueType.NONE)
        tag_metas.append(tag_meta)
    tag_meta_col = sly.TagMetaCollection(tag_metas)
    project_meta = sly.ProjectMeta(tag_metas=tag_meta_col)
    return project_meta


def flat_tag_list(total_tags):
    tags = []
    for tag in total_tags:
        if tag is None or tag == '':
            continue
        else:
            if g.TAGS_DELIMITER in tag:
                tag = tag.split(g.TAGS_DELIMITER)
            tags.append(tag)

    total_tags = []
    for sublist in tags:
        if type(sublist) == str:
            total_tags.append(sublist)
        else:
            for tag in sublist:
                if tag != '':
                    total_tags.append(tag)

    total_tags = list(set(total_tags))
    return total_tags


def check_column_names(col_names_validate):
    if not any(image_url_name in g.possible_image_url_col_names for image_url_name in col_names_validate) and not any(
            image_path_name in g.possible_image_path_col_names for image_path_name in col_names_validate):
        raise Exception("IMAGE COLUMN NAME IS INVALID, PLEASE USE ONE OF:\n"
                        f"{g.possible_image_url_col_names} FOR URL AND "
                        f"{g.possible_image_path_col_names} FOR PATH")
    if len(col_names_validate) == 2:
        if not any(tag_name in g.possible_tag_col_names for tag_name in col_names_validate):
            raise Exception("TAG COLUMN NAME IS INVALID, PLEASE USE ONE OF:\n"
                            f"{g.possible_tag_col_names}")


def validate_column_names(first_csv_row):
    col_names_validate = [key.lower() for key in first_csv_row.keys()]
    col_names = [key for key in first_csv_row.keys()]
    check_column_names(col_names_validate)
    image_col_name = None
    tag_col_name = None
    for name in col_names:
        if name == "url":
            image_col_name = name
            g.is_url = True
        if name == "path":
            image_col_name = name
        if name == "tag":
            tag_col_name = name

    return image_col_name, tag_col_name


def create_preview_table_from_csv_file(csv_path):
    csv_table = {"columns": [], "data": []}
    with open(csv_path, "r") as images_csv:
        reader = csv.DictReader(images_csv, delimiter=g.DEFAULT_DELIMITER)
        reader = [row for row in reader]
        stripped_reader = []
        for row in reader:
            stripped_row = {key: value.strip() for key, value in row.items()}
            stripped_reader.append(stripped_row)
        g.csv_reader = stripped_reader
        g.image_col_name, g.tag_col_name = validate_column_names(stripped_reader[0])

        if g.tag_col_name is not None:
            csv_table["columns"] = ["row", g.image_col_name, g.tag_col_name]
            for idx, row in enumerate(stripped_reader):
                csv_table["data"].append([idx + 1, row[g.image_col_name], row[g.tag_col_name]])
            total_tags = flat_tag_list(list(set([row[g.tag_col_name] for row in stripped_reader])))
            g.project_meta = create_project_meta_from_csv_tags(total_tags)
            need_tag = "add"
        else:
            csv_table["columns"] = ["row", g.image_col_name]
            for idx, row in enumerate(stripped_reader):
                csv_table["data"].append([idx + 1, row[g.image_col_name]])
            total_tags = 0
            need_tag = "ignore"

        images_paths = [row[g.image_col_name] for row in stripped_reader]

    return csv_table, images_paths, total_tags, need_tag


def download_and_preview_table(api, task_id):
    api.file.download(g.TEAM_ID, g.INPUT_FILE, g.local_csv_path)
    csv_table, images_paths, total_tags, need_tag = create_preview_table_from_csv_file(g.local_csv_path)

    fields = [
        {"field": "data.table", "payload": csv_table},
        {"field": "data.connecting", "payload": False},
        {"field": "state.totalImagesLen", "payload": len(images_paths)},
        {"field": "state.totalTagsLen", "payload": total_tags},
        {"field": "state.needTag", "payload": need_tag},
    ]
    api.task.set_fields(task_id, fields)
    return images_paths
