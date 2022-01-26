import init_ui
import globals as g
import functions as f
import supervisely as sly


def process_images_from_csv(api, state, image_url_col_name, tag_col_name, app_logger):
    project = None
    ds_images_names = None
    csv_images_len = len(g.csv_reader)
    if state["dstProjectMode"] == "newProject":
        project = api.project.create(g.WORKSPACE_ID, state["dstProjectName"], sly.ProjectType.IMAGES,
                                     change_name_if_conflict=True)
    elif state["dstProjectMode"] == "existingProject":
        project = api.project.get_info_by_id(state["dstProjectId"])
    if project is None:
        sly.logger.error("Result project is None (not found or not created)")
        return

    dataset = None
    if state["dstDatasetMode"] == "newDataset":
        dataset = api.dataset.create(project.id, state["dstDatasetName"], change_name_if_conflict=True)
    elif state["dstDatasetMode"] == "existingDataset":
        dataset = api.dataset.get_info_by_name(project.id, state["selectedDatasetName"])
        ds_images = g.api.image.get_list(dataset.id)
        ds_images_names = [img.name for img in ds_images]

    if dataset is None:
        sly.logger.error("Result dataset is None (not found or not created)")
        return

    project_meta = sly.ProjectMeta()
    progress_items_cb = init_ui.get_progress_cb(api, g.TASK_ID, 1, "processing CSV", csv_images_len)
    for batch in sly.batched(g.csv_reader):
        image_paths = []
        image_names = []
        anns = []
        for row in batch:
            if len(row[image_url_col_name]) == 0:
                continue
            success, image_name, image_path = f.process_image_by_url(row[image_url_col_name], app_logger)

            if image_name in ds_images_names:
                csv_images_len -= 1
                app_logger.warn(f"{image_name} already exists in dataset: {dataset.name}")
                continue

            if success is False:
                continue
            ann, project_meta = f.process_ann(row, project_meta, image_path, tag_col_name)

            image_paths.append(image_path)
            image_names.append(image_name)
            anns.append(ann)

        api.project.update_meta(project.id, project_meta.to_json())
        images_infos = api.image.upload_paths(dataset.id, image_names, image_paths)
        images_ids = [image_info.id for image_info in images_infos]
        api.annotation.upload_anns(images_ids, anns)
        progress_items_cb(len(batch))

    init_ui.reset_progress(api, g.TASK_ID, 1)
    init_ui.reset_progress(api, g.TASK_ID, 2)
    g.my_app.show_modal_window(
        f"{csv_images_len} images has been successfully imported to the project \"{project.name}\""
        f", dataset \"{dataset.name}\". You can continue importing images to the same or new "
        f"project. If you've finished with the app, stop it manually.")
    api.app.set_field(g.TASK_ID, "data.processing", False)
