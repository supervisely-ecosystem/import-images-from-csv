import os
import shutil  # @TODO: SDK fix — api.file.download_directory (creates root dir if download from Team Files root)
import tarfile
from typing import List, Set

import supervisely as sly
from supervisely._utils import generate_free_name
from supervisely.io.fs import download, get_file_name_with_ext, silent_remove

import init_ui
import sly_globals as g


def download_directory(team_id, remote_path, local_save_path, progress_cb=None):
    os.makedirs(local_save_path, exist_ok=True)
    sly.fs.clean_dir(local_save_path)

    local_temp_archive = os.path.join(local_save_path, "temp.tar")
    g.api.file._download(team_id, remote_path, local_temp_archive, progress_cb)
    tr = tarfile.open(local_temp_archive)
    tr.extractall(local_save_path)
    silent_remove(local_temp_archive)
    if remote_path == "/":
        remote_path = "/root"

    temp_dir = os.path.join(local_save_path, os.path.basename(os.path.normpath(remote_path)))

    file_names = os.listdir(temp_dir)
    for file_name in file_names:
        file_path = os.path.join(temp_dir, file_name)
        shutil.move(f"{file_path}", local_save_path)

    shutil.rmtree(temp_dir)


def create_project(api: sly.Api, state):
    project = None
    if state["dstProjectMode"] == "newProject":
        project = api.project.create(
            g.WORKSPACE_ID,
            state["dstProjectName"],
            sly.ProjectType.IMAGES,
            change_name_if_conflict=True,
        )
    elif state["dstProjectMode"] == "existingProject":
        project = api.project.get_info_by_id(state["dstProjectId"])

    if g.project_meta is not None:
        if g.dst_project_meta is not None:
            g.project_meta = g.project_meta.merge(g.dst_project_meta)
        api.project.update_meta(project.id, g.project_meta.to_json())
    if project is None:
        sly.logger.error("Result project is None (not found or not created)")
        return

    dataset = None
    if state["dstDatasetMode"] == "newDataset":
        dataset = api.dataset.create(
            project.id, state["dstDatasetName"], change_name_if_conflict=True
        )
    elif state["dstDatasetMode"] == "existingDataset":
        dataset = api.dataset.get_info_by_name(project.id, state["selectedDatasetName"])

    if dataset is None:
        sly.logger.error("Result dataset is None (not found or not created)")
        return

    return project, dataset


def check_is_bucket_link(link):
    bucket_prefixes = ["s3://", "azure://", "google://", "gcs://", "minio://", "fs://"]
    return any(link.startswith(prefix) for prefix in bucket_prefixes)


def download_file_from_link(api: sly.Api, link, save_path, file_name, app_logger):
    if check_is_bucket_link(link):
        try:
            api.remote_storage.download_path(link, save_path)
        except Exception as e:
            sly.logger.warn(f"Could not download file {file_name}")
            sly.logger.warn(e)
    else:
        try:
            download(link, save_path)
            app_logger.info(f"{file_name} has been successfully downloaded")
        except Exception as e:
            sly.logger.warn(f"Could not download file {file_name}")
            sly.logger.warn(e)


def download_file_from_link_directly(api: sly.Api, link, file_name, dataset, state):
    image_info = api.image.upload_link(
        dataset_id=dataset.id,
        name=file_name,
        link=link,
        force_metadata_for_links=state["forceMetadata"],
    )
    return image_info


def download_csv_dir(api: sly.Api):
    csv_dir_name = os.path.dirname(g.INPUT_FILE.lstrip("/").rstrip("/"))
    save_dir = os.path.join(os.path.dirname(g.local_csv_path), csv_dir_name)

    if csv_dir_name == "":
        csv_dir_name = "Team Files Root"
        save_dir = g.storage_dir
    remote_csv_dir = os.path.dirname(g.INPUT_FILE)
    if remote_csv_dir != "/":
        remote_csv_dir = remote_csv_dir + "/"

    csv_dir_size = api.file.get_directory_size(g.TEAM_ID, remote_csv_dir)
    progress_cb = init_ui.get_progress_cb(
        api,
        g.TASK_ID,
        1,
        f"Downloading CSV Root Directory {csv_dir_name}",
        csv_dir_size,
        is_size=True,
    )
    download_directory(g.TEAM_ID, remote_csv_dir, save_dir, progress_cb)
    init_ui.reset_progress(api, g.TASK_ID, 1)


def process_image_by_url(
    api: sly.Api, image_url, image_names, ds_images_names, dataset, app_logger
):
    image_url = image_url.strip()
    extension = os.path.splitext(image_url)[1]
    if not extension:
        sly.logger.warn(f"Image [{image_url}] doesn't have extension in link")
    image_name = os.path.basename(os.path.normpath(image_url))
    save_path = os.path.join(g.img_dir, image_name)
    if os.path.isfile(save_path):
        image_name = validate_image_name(
            image_name, image_names, ds_images_names, dataset, app_logger
        )
        save_path = os.path.join(g.img_dir, image_name)
    download_file_from_link(api, image_url, save_path, image_name, app_logger)
    return image_name, save_path


def process_image_link(
    api: sly.Api, image_url, image_names, ds_images_names, dataset, app_logger, state
):
    image_url = image_url.strip()
    extension = os.path.splitext(image_url)[1]
    if not extension:
        sly.logger.warn(f"Image [{image_url}] doesn't have extension in link")
    image_name = os.path.basename(os.path.normpath(image_url))
    image_name = validate_image_name(image_name, image_names, ds_images_names, dataset, app_logger)
    image_info = download_file_from_link_directly(api, image_url, image_name, dataset, state)
    return image_info


def process_image_by_path(image_path, image_names, ds_images_names, dataset, app_logger):
    remote_path = os.path.abspath(os.path.join(g.remote_csv_dir_path, image_path.lstrip("/")))
    if g.api.file.exists(g.TEAM_ID, remote_path):
        image_path = remote_path
    image_name = get_file_name_with_ext(image_path)
    save_path = os.path.join(g.img_dir, image_name)
    if os.path.isfile(save_path):
        image_name = validate_image_name(
            image_name, image_names, ds_images_names, dataset, app_logger
        )
        save_path = os.path.join(g.img_dir, image_name)
    g.api.file.download(g.TEAM_ID, image_path, save_path)
    return image_name, save_path


def process_image_by_local_path(image_path, image_names, ds_images_names, dataset, app_logger):
    csv_dir_name = os.path.dirname(g.INPUT_FILE)
    image_path = g.storage_dir + csv_dir_name + image_path
    image_name = get_file_name_with_ext(image_path)
    if os.path.isfile(image_path):
        image_name = validate_image_name(
            image_name, image_names, ds_images_names, dataset, app_logger
        )
    return image_name, image_path


def process_image(
    api: sly.Api, is_url, image_name, image_names, ds_images_names, dataset, app_logger
):
    if is_url:
        image_name, image_path = process_image_by_url(
            api, image_name, image_names, ds_images_names, dataset, app_logger
        )
    else:
        if not g.download_by_dirs:
            image_name, image_path = process_image_by_path(
                image_name, image_names, ds_images_names, dataset, app_logger
            )
        else:
            image_name, image_path = process_image_by_local_path(
                image_name, image_names, ds_images_names, dataset, app_logger
            )
    return image_name, image_path


def validate_image_name(image_name, image_names, ds_images_names, dataset, app_logger):
    if image_name in ds_images_names:
        new_image_name = generate_free_name(ds_images_names, image_name, True)
        app_logger.warn(
            f"{image_name} already exists in dataset: {dataset.name}, it will be renamed to: {new_image_name}"
        )
        return new_image_name

    if image_name in image_names:
        new_image_name = generate_free_name(image_names, image_name, True)
        app_logger.warn(
            f"Duplicate {image_name} in csv file, it will be renamed to: {new_image_name}"
        )
        return new_image_name
    return image_name


def process_ann(csv_row, image_path, tag_col_name):
    if csv_row.get(tag_col_name) is None or csv_row.get(tag_col_name) == "":
        ann = sly.Annotation.from_img_path(image_path)
        return ann

    tag_metas = []
    tag_names = csv_row[tag_col_name].strip()
    tag_names = tag_names.split(g.TAGS_DELIMITER)
    for tag_name in tag_names:
        if tag_name != "":
            tag_name.strip()
            tag_meta = g.project_meta.get_tag_meta(tag_name)
            tag_metas.append(tag_meta)

    tag_col = sly.TagCollection(tag_metas)

    ann = sly.Annotation.from_img_path(image_path).add_tags(tag_col)
    return ann


def process_ann_link(csv_row, tag_col_name):
    if csv_row.get(tag_col_name) is None or csv_row.get(tag_col_name) == "":
        ann = sly.Annotation(img_size=[None, None])
        return ann

    tag_metas = []
    tag_names = csv_row[tag_col_name].strip()
    tag_names = tag_names.split(g.TAGS_DELIMITER)
    for tag_name in tag_names:
        if tag_name != "":
            tag_name.strip()
            tag_meta = g.project_meta.get_tag_meta(tag_name)
            tag_metas.append(tag_meta)

    tag_col = sly.TagCollection(tag_metas)

    ann = sly.Annotation(img_size=[None, None]).add_tags(tag_col)
    return ann


def show_output_message(api: sly.Api, processed_images_counter, project, dataset_name):
    modal_message = "image" if processed_images_counter == 1 else "images"

    g.my_app.show_modal_window(
        f'{processed_images_counter} {modal_message} has been successfully imported to the project "{project.name}"'
        f', dataset "{dataset_name}". You can continue importing images to the same or new '
        f"project. If you've finished with the app, stop it manually."
    )

    project_info = api.project.get_info_by_id(project.id)
    fields = [
        {"field": "data.processing", "payload": False},
        {"field": "data.started", "payload": False},
        {"field": "data.finished", "payload": True},
        {"field": "data.resultProject", "payload": project.name},
        {"field": "data.resultProjectId", "payload": project.id},
        {
            "field": "data.resultProjectPreviewUrl",
            "payload": g.api.image.preview_url(project_info.reference_image_url, 100, 100),
        },
    ]
    g.api.task.set_fields(g.TASK_ID, fields)


def process_images_from_csv(api: sly.Api, state, image_col_name, tag_col_name, app_logger):
    if not g.is_url and g.download_by_dirs:
        download_csv_dir(api)

    processed_images_counter = 0

    project, dataset = create_project(api, state)
    ds_images_names = set([img.name for img in api.image.get_list(dataset.id)])

    progress_items_cb = init_ui.get_progress_cb(
        api, g.TASK_ID, 1, "Processing CSV", len(g.csv_reader)
    )
    all_image_names = set()
    for batch in sly.batched(g.csv_reader):
        image_paths = []
        image_names = []
        anns = []
        for row in batch:
            try:
                image_name, image_path = process_image(
                    api,
                    g.is_url,
                    row[image_col_name],
                    image_names,
                    ds_images_names,
                    dataset,
                    app_logger,
                )
                if not sly.fs.file_exists(image_path):
                    raise FileNotFoundError(f"File {image_path} not found")
                processed_images_counter += 1
            except Exception:
                app_logger.warn(f"Couldn't process: {row[image_col_name]}, item will be skipped")
                continue

            if tag_col_name is not None:
                ann = process_ann(row, image_path, tag_col_name)
                anns.append(ann)

            image_paths.append(image_path)
            image_names.append(image_name)

        free_image_names, all_image_names = get_free_names(
            api, dataset.id, image_names, all_image_names
        )
        images_infos = api.image.upload_paths(dataset.id, free_image_names, image_paths)
        if tag_col_name is not None:
            images_ids = [image_info.id for image_info in images_infos]
            api.annotation.upload_anns(images_ids, anns)
        progress_items_cb(len(batch))

    
    # -------------------------------------- Add Workflow Output ------------------------------------- #
    g.workflow.add_output(project.id)
    # ----------------------------------------------- - ---------------------------------------------- #
    init_ui.reset_progress(api, g.TASK_ID, 1)
    show_output_message(api, processed_images_counter, project, dataset.name)


def process_images_from_csv_link(api: sly.Api, state, image_col_name, tag_col_name, app_logger):
    processed_images_counter = 0

    project, dataset = create_project(api, state)
    ds_images_names = set([img.name for img in api.image.get_list(dataset.id)])

    progress_items_cb = init_ui.get_progress_cb(
        api, g.TASK_ID, 1, "Processing CSV", len(g.csv_reader)
    )
    for batch in sly.batched(g.csv_reader):
        images_infos = []
        image_names = []
        image_paths = []
        anns = []
        for row in batch:
            try:
                image_info = process_image_link(
                    api,
                    row[image_col_name],
                    image_names,
                    ds_images_names,
                    dataset,
                    app_logger,
                    state,
                )
                processed_images_counter += 1
            except Exception:
                app_logger.warn(f"Couldn't process: {row[image_col_name]}, item will be skipped")
                continue

            if tag_col_name is not None:
                ann = process_ann_link(row, tag_col_name)
                anns.append(ann)

            images_infos.append(image_info)
            image_names.append(image_info.name)

        bounds_validation = True if not state["forceMetadata"] else False

        if tag_col_name is not None:
            images_ids = [image_info.id for image_info in images_infos]
            api.annotation.upload_anns(images_ids, anns, skip_bounds_validation=bounds_validation)
        progress_items_cb(len(batch))

    
    # -------------------------------------- Add Workflow Output ------------------------------------- #
    g.workflow.add_output(project.id)
    # ----------------------------------------------- - ---------------------------------------------- #
    init_ui.reset_progress(api, g.TASK_ID, 1)
    show_output_message(api, processed_images_counter, project, dataset.name)


def get_free_names(
    api: sly.Api, dataset_id: int, names: List[str], used_names: Set[str]
) -> List[str]:
    images_in_dataset = api.image.get_list(dataset_id, force_metadata_for_links=False)
    new_used_names = {image_info.name for image_info in images_in_dataset}
    for name in new_used_names:
        used_names.add(name)
    new_names = [
        generate_free_name(used_names, name, with_ext=True, extend_used_names=True)
        for name in names
    ]
    return new_names, used_names
