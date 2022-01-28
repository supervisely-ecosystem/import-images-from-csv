<div align="center" markdown>
<img src="https://i.imgur.com/esnMjEo.png"/>


# CSV to Images Project

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Demo">Demo</a> •
  <a href="#Usage">Usage</a> 
  
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
- `.CSV` file have to containe one of the following columns: **url** or **path**. If column **url** is defined then app will download image by url and upload it to project. If column **path** is defined then app will treat it as a relative path with respect to csv file location, get image from team files and add it to ptoject.
- `.CSV` file may contain optional column **tags**. If this columns is defines, corresponding tags will be added to the image during import. Delimeter in **tags** column is **`;`** (**semicolon**)
- `.CSV` columns delimiter is **`,`** (**comma**)
- 
- If you want to import images by **paths**, you must use relative paths to images from `.CSV` file


# How to Run
1. Add [Import Images from CSV](https://ecosystem.supervise.ly/apps/import-images-from-csv) to your team from Ecosystem.

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-images-from-csv" src="https://i.imgur.com/vW65imr.png" width="450px" style='padding-bottom: 20px'/>  

2. Run app from the context menu of the `.CSV` file:

<img src="https://i.imgur.com/6Ej5E8C.png" width="100%"/>

3. Wait until the app is started, press `Open` button in `Workspace tasks`

<img src="https://i.imgur.com/FDMhaqu.png" width="100%"/>

4. User can remove files from


# Demo
<a data-key="sly-embeded-video-link" href="https://youtu.be/TrRd1sfT-q4" data-video-code="TrRd1sfT-q4">
    <img src="https://i.imgur.com/Fg3pecP.png" alt="SLY_EMBEDED_VIDEO_LINK"  width="70%">
</a>


# Usage

1. **Preview CSV file** section contains all information about csv file and some of it's stats
2. **Import settings** section is configurable. You can configure destination project, dataset, and choose whether you want to assign or ignore tags. Assign/ignore option only available if there are tags in the `.CSV` file.
3. You can import images from `.CSV` file to multiple destinations during one application session
4. When you have finished working with the application, **stop it manually**

<img src="https://i.imgur.com/XaIFXen.png" width="100%"/>
