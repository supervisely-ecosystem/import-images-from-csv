import os
import supervisely as sly
from supervisely.io.fs import mkdir, get_file_name


my_app = sly.AppService()
api: sly.Api = my_app.public_api

TASK_ID = int(os.environ["TASK_ID"])
TEAM_ID = int(os.environ['context.teamId'])
WORKSPACE_ID = int(os.environ['context.workspaceId'])
INPUT_FILE = os.environ["modal.state.slyFile"]

project_name = get_file_name(INPUT_FILE)

storage_dir = my_app.data_dir
local_csv_path = os.path.join(storage_dir, "catalog.csv")
api.file.download(TEAM_ID, INPUT_FILE, local_csv_path)

DEFAULT_DELIMITER = ','

possible_image_url_col_names = ["image url", "image-url", "image_url", "imageurl"]
possible_tag_col_names = ["tag", "tags"]

img_dir = os.path.join(storage_dir, "img_dir")
mkdir(img_dir)
