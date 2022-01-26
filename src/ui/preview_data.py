import csv
import globals as g
import functions as f


def download_and_preview_table(api, task_id, context, state, app_logger):
    api.file.download(g.TEAM_ID, g.INPUT_FILE, g.local_csv_path)

    csv_table = {"columns": [], "data": []}
    with open(g.local_csv_path, "r") as images_csv:
        reader = csv.DictReader(images_csv, delimiter=g.DEFAULT_DELIMITER)
        reader = [row for row in reader]
        g.csv_reader = reader
        g.image_url_col_name, g.tag_col_name = f.validate_csv_table(reader[0])

        csv_table["columns"] = ["row", g.image_url_col_name, g.tag_col_name]
        for idx, row in enumerate(reader):
            csv_table["data"].append([idx + 1, row[g.image_url_col_name], row[g.tag_col_name]])

        # stats

        all_images = [row[g.image_url_col_name] for row in reader]
        unique_images = list(set(all_images))
        unique_tags = f.flat_tag_list(list(set([row[g.tag_col_name] for row in reader])))
        duplicate_images = len(all_images) - len(unique_images)

    fields = [
        {"field": "data.table", "payload": csv_table},
        {"field": "data.connecting", "payload": False},
        {"field": "state.uniqueImagesLen", "payload": len(unique_images)},
        {"field": "state.duplicateImagesLen", "payload": duplicate_images},
        {"field": "state.uniqueTagsLen", "payload": len(unique_tags)},
    ]
    api.task.set_fields(task_id, fields)
