import os
import globals as g
import supervisely as sly
import init_ui

from ui.preview_data import download_and_preview_table
from ui.import_settings import process_images_from_csv


def calculate_images_size_threshold(api, csv_path, image_paths):
    csv_dir = os.path.dirname(csv_path)
    images_size = 0
    for image_path in image_paths:
        images_size += api.file.get_info_by_path(g.TEAM_ID, image_path).sizeb
    g.csv_dir_size = api.file.get_directory_size(g.TEAM_ID, csv_dir)
    images_size_threshold = round((images_size * 100) / g.csv_dir_size)
    return images_size_threshold


@g.my_app.callback("preview")
@sly.timeit
def preview(api: sly.Api, task_id, context, state, app_logger):
    images_paths = download_and_preview_table(api, task_id)
    if g.is_url is False:
        g.images_size_threshold = calculate_images_size_threshold(api, g.INPUT_FILE, images_paths)


@g.my_app.callback("process")
@sly.timeit
def process(api: sly.Api, task_id, context, state, app_logger):
    process_images_from_csv(api, state, g.image_col_name, g.tag_col_name, app_logger)


def main():
    sly.logger.info("Script arguments", extra={
        "TEAM_ID": g.TEAM_ID,
        "WORKSPACE_ID": g.WORKSPACE_ID,
        "INPUT_FILE": g.INPUT_FILE
    })

    data = {}
    state = {}

    init_ui.init_context(data, g.TEAM_ID, g.WORKSPACE_ID)
    init_ui.init_table_preview(data, state)
    init_ui.init_options(data, state)
    init_ui.init_progress(data, state)

    g.my_app.compile_template(g.root_source_dir)
    g.my_app.run(data=data, state=state, initial_events=[{"command": "preview"}])


if __name__ == "__main__":
    sly.main_wrapper("main", main)
