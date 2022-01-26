import globals as g
import supervisely as sly
import init_ui

from ui.preview_data import download_and_preview_table
from ui.import_settings import process_images_from_csv


@g.my_app.callback("preview")
@sly.timeit
def preview(api: sly.Api, task_id, context, state, app_logger):
    download_and_preview_table(api, task_id, context, state, app_logger)


@g.my_app.callback("process")
@sly.timeit
def process(api: sly.Api, task_id, context, state, app_logger):
    process_images_from_csv(api, state, g.image_url_col_name, g.tag_col_name, app_logger)


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
