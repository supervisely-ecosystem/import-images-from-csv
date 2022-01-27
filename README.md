<div align="center" markdown>
<img src="https://i.imgur.com/esnMjEo.png"/>


# CSV to Images Project

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Demo-Video">Demo Video</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-images-from-csv)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-images-from-csv)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-from-csv&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-from-csv&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-from-csv&counter=runs&label=runs&123)](https://supervise.ly)

</div>

# Overview

Application converts **.CSV file** [**(example)**](https://github.com/supervisely-ecosystem/import-images-from-csv/releases/download/v0.0.1/demo_files.zip) to Supervisely Images Project

Application key points:  
- `.CSV` required field: **urls** or **paths** (hard-coded field name)
- `.CSV` optional field: **tags** (hard-coded field name)
- `.CSV` delimeter is **comma**
- delimeter for multiple **tags** is **semicolon**
- Each images from the catalog will be tagged with appropriate tags
- If you want to import images by **paths**, you must use relative paths to images from `.CSV` file


# How to Run
1. Add [Import Images from CSV](https://ecosystem.supervise.ly/apps/import-images-from-csv) to your team from Ecosystem.

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-images-from-csv" src="https://i.imgur.com/vW65imr.png" width="450px" style='padding-bottom: 20px'/>  

2. Run app from the context menu of the `.CSV` file:

<img src="https://i.imgur.com/6Ej5E8C.png" width="100%"/>

3. Wait until the app is started, press `Open` button in `Workspace tasks`

<img src="https://i.imgur.com/FDMhaqu.png" width="100%"/>

# How to Use

1. **Preview CSV file** section contains all information about csv file and some of it's stats
2. **Import settings** section is configurable. You can configure destination project, dataset, and choose whether you want to assign or ignore tags. Assign/ignore option only available if there are tags in the `.CSV` file.
3. You can import images from `.CSV` file to multiple destinations during one application session
4. When you have finished working with the application, **stop it manually**

<img src="https://i.imgur.com/XaIFXen.png" width="100%"/>

# Demo Video
<a data-key="sly-embeded-video-link" href="https://youtu.be/TrRd1sfT-q4" data-video-code="TrRd1sfT-q4">
    <img src="https://i.imgur.com/Fg3pecP.png" alt="SLY_EMBEDED_VIDEO_LINK"  width="70%">
</a>
