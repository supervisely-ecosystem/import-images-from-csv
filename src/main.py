import os

import init_ui
import sly_globals as g
import supervisely as sly
from ui.import_settings import process_images_from_csv, process_images_from_csv_link
from ui.preview_data import download_and_preview_table


def define_download_method(api, csv_path, images_paths):
    csv_root_path = os.path.join(os.path.dirname(csv_path), "")
    images_paths = [
        os.path.join(csv_root_path, image_path[1:]) for image_path in images_paths
    ]  # relative to absolute

    files_in_directory = api.file.list2(g.TEAM_ID, csv_root_path)

    root_directory_size = 0
    files_to_download_size = 0

    for file_info in files_in_directory:
        if file_info.path in images_paths:
            files_to_download_size += file_info.sizeb
        root_directory_size += file_info.sizeb

    g.download_by_dirs = bool(files_to_download_size / root_directory_size > g.THRESHOLD_SIZE_LIMIT)


@g.my_app.callback("preview")
@sly.timeit
def preview(api: sly.Api, task_id, context, state, app_logger):
    images_paths = download_and_preview_table(api, task_id)
    if not g.is_url:
        g.images_size_threshold = define_download_method(api, g.INPUT_FILE, images_paths)


@g.my_app.callback("process")
@sly.timeit
def process(api: sly.Api, task_id, context, state, app_logger):
    if state["dstProjectMode"] == "existingProject":
        dst_project_id = state["dstProjectId"]
        project_meta = sly.ProjectMeta.from_json(api.project.get_meta(dst_project_id))
        g.dst_project_meta = project_meta

    if state["addMode"] == "copyData":
        process_images_from_csv(api, state, g.image_col_name, g.tag_col_name, app_logger)
    elif state["addMode"] == "addByLink":
        process_images_from_csv_link(api, state, g.image_col_name, g.tag_col_name, app_logger)


def main():
    sly.logger.info(
        "Script arguments",
        extra={"TEAM_ID": g.TEAM_ID, "WORKSPACE_ID": g.WORKSPACE_ID, "INPUT_FILE": g.INPUT_FILE},
    )

    data = {}
    state = {}

    init_ui.init_context(data, g.TEAM_ID, g.WORKSPACE_ID)
    init_ui.init_table_preview(data, state)
    init_ui.init_options(data, state)
    init_ui.init_progress(data, state)

    g.my_app.compile_template(g.root_source_dir)
    g.my_app.run(data=data, state=state, initial_events=[{"command": "preview"}])


if __name__ == "__main__":
    sly.main_wrapper("main", main, log_for_agent=False)
