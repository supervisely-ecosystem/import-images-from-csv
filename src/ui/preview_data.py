import csv
import globals as g
import functions as f


def download_and_preview_table(api, task_id, context, state, app_logger):
    api.file.download(g.TEAM_ID, g.INPUT_FILE, g.local_csv_path)

    need_tag = g.api.task.get_field(task_id, 'state.needTag')

    csv_table = {"columns": [], "data": []}
    with open(g.local_csv_path, "r") as images_csv:
        reader = csv.DictReader(images_csv, delimiter=g.DEFAULT_DELIMITER)
        reader = [row for row in reader]
        g.csv_reader = reader
        g.image_col_name, g.tag_col_name = f.validate_csv_table(reader[0])

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
            unique_tags = f.flat_tag_list(list(set([row[g.tag_col_name] for row in reader])))
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
