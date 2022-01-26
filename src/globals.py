import os
import sys
from pathlib import Path

import supervisely as sly
from supervisely.io.fs import mkdir


my_app = sly.AppService()
api: sly.Api = my_app.public_api

root_source_dir = str(Path(sys.argv[0]).parents[1])
sly.logger.info(f"Root source directory: {root_source_dir}")
sys.path.append(root_source_dir)

TASK_ID = int(os.environ["TASK_ID"])
TEAM_ID = int(os.environ['context.teamId'])
WORKSPACE_ID = int(os.environ['context.workspaceId'])
INPUT_FILE = os.environ["modal.state.slyFile"]


storage_dir = my_app.data_dir
local_csv_path = os.path.join(storage_dir, "images.csv")
remote_csv_dir_path = os.path.dirname(INPUT_FILE)

DEFAULT_DELIMITER = ','
TAGS_DELIMITER = ';'

possible_image_url_col_names = ["url", "urls"]
possible_image_path_col_names = ["path", "paths"]
possible_tag_col_names = ["tag", "tags"]

image_col_name = None
tag_col_name = None
csv_reader = None
is_path = False

img_dir = os.path.join(storage_dir, "img_dir")
mkdir(img_dir)
