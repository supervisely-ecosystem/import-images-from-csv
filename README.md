<div align="center" markdown>
<img src="https://i.imgur.com/esnMjEo.png"/>


# CSV to Images Project

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Demo-Video">Demo Video</a> •
    <a href="#Demo-Data">Demo Data</a> •
  <a href="#Results">Results</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-images-from-csv)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-images-from-csv)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-from-csv&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-from-csv&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-from-csv&counter=runs&label=runs&123)](https://supervise.ly)

</div>

# Overview

Application converts **.CSV file** [**(example)**](https://github.com/supervisely-ecosystem/import-images-from-csv/releases/download/v0.0.1/test_snacks_catalog.csv) to Supervisely Images Project

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

<img src="https://i.imgur.com/XaIFXen.png" width="100%"/>

# Demo Data

- [.CSV table to import example](https://github.com/supervisely-ecosystem/import-images-from-csv/releases/download/v0.0.1/test_snacks_catalog.csv) — table example
