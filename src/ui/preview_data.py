import csv
import globals as g
import supervisely as sly


def create_project_meta_from_csv_tags(unique_tags):
    tag_metas = []
    for tag_name in unique_tags:
        tag_meta = sly.TagMeta(tag_name, sly.TagValueType.NONE)
        tag_metas.append(tag_meta)
    tag_meta_col = sly.TagMetaCollection(tag_metas)
    project_meta = sly.ProjectMeta(tag_metas=tag_meta_col)
    return project_meta


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


def validate_csv_table(first_csv_row):
    col_names_validate = [key.lower() for key in first_csv_row.keys()]
    col_names = [key for key in first_csv_row.keys()]

    check_column_names(col_names_validate)

    image_col_name = None
    tag_col_name = None
    for name in col_names:
        if name.lower().startswith("url"):
            image_col_name = name
        if name.lower().startswith("path"):
            image_col_name = name
            g.is_path = True
        if name.lower().startswith("tag"):
            tag_col_name = name

    return image_col_name, tag_col_name


def download_and_preview_table(api, task_id, context, state, app_logger):
    api.file.download(g.TEAM_ID, g.INPUT_FILE, g.local_csv_path)
    need_tag = g.api.task.get_field(task_id, 'state.needTag')
    csv_table = {"columns": [], "data": []}
    with open(g.local_csv_path, "r") as images_csv:
        reader = csv.DictReader(images_csv, delimiter=g.DEFAULT_DELIMITER)
        reader = [row for row in reader]
        g.csv_reader = reader
        g.image_col_name, g.tag_col_name = validate_csv_table(reader[0])

        if g.tag_col_name is not None:
            csv_table["columns"] = ["row", g.image_col_name, g.tag_col_name]
        else:
            csv_table["columns"] = ["row", g.image_col_name]
        for idx, row in enumerate(reader):
            if g.tag_col_name is not None:
                if need_tag == "add":
                    csv_table["data"].append([idx + 1, row[g.image_col_name], row[g.tag_col_name]])
            else:
                csv_table["data"].append([idx + 1, row[g.image_col_name]])

        # stats
        all_images = [row[g.image_col_name] for row in reader]
        unique_images = list(set(all_images))
        if g.tag_col_name is not None:
            unique_tags = flat_tag_list(list(set([row[g.tag_col_name] for row in reader])))
            g.project_meta = create_project_meta_from_csv_tags(unique_tags)
            unique_tags = len(unique_tags)
        else:
            unique_tags = 0
            need_tag = "ignore"

        duplicate_images = len(all_images) - len(unique_images)

    fields = [
        {"field": "data.table", "payload": csv_table},
        {"field": "data.connecting", "payload": False},
        {"field": "state.uniqueImagesLen", "payload": len(unique_images)},
        {"field": "state.duplicateImagesLen", "payload": duplicate_images},
        {"field": "state.uniqueTagsLen", "payload": unique_tags},
        {"field": "state.needTag", "payload": need_tag},
    ]
    api.task.set_fields(task_id, fields)
