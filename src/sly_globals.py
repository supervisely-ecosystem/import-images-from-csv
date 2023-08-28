import os
import shutil
import sys
from pathlib import Path
from dotenv import load_dotenv

import supervisely as sly
from supervisely.io.fs import mkdir
from supervisely.app.v1.app_service import AppService


if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


my_app: AppService = AppService()
api: sly.Api = my_app.public_api

shutil.rmtree(my_app.data_dir, ignore_errors=True)

root_source_dir = str(Path(sys.argv[0]).parents[1])
sly.logger.info(f"Root source directory: {root_source_dir}")
sys.path.append(root_source_dir)

TASK_ID = int(os.environ["TASK_ID"])
TEAM_ID = int(os.environ["context.teamId"])
WORKSPACE_ID = int(os.environ["context.workspaceId"])
INPUT_FILE = os.environ["modal.state.slyFile"]

download_by_dirs = True
THRESHOLD_SIZE_LIMIT = 0.80

storage_dir = my_app.data_dir
local_csv_path = os.path.join(storage_dir, "images.csv")
remote_csv_dir_path = os.path.dirname(INPUT_FILE)
img_dir = os.path.join(storage_dir, "img_dir")
mkdir(img_dir, True)

DEFAULT_DELIMITER = ";"
TAGS_DELIMITER = ","

possible_image_url_col_names = ["url"]
possible_image_path_col_names = ["path"]
possible_tag_col_names = ["tag"]

# --placeholders--
image_col_name = None

tag_col_name = None
csv_reader = None

is_url = False
project_meta = None
