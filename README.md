<div align="center" markdown>
<img src="https://i.imgur.com/hqtNXYg.jpg"/>


# CSV to Images Project

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Demo-Video">Demo Video</a> •
    <a href="#Demo-Data">Demo Data</a> •
  <a href="#Results">Results</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-csv-catalog)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-csv-catalog)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-csv-catalog&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-csv-catalog&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-csv-catalog&counter=runs&label=runs&123)](https://supervise.ly)

</div>

# Overview

Application converts **.CSV catalog** [**(example)**](https://github.com/supervisely-ecosystem/import-csv-catalog/releases/download/v0.0.1/test_snacks_catalog.csv) to Supervisely Images Project

Application key points:  
- `.CSV` required fields: **image_url**, **tags**
- `.CSV` delimeter is **comma**
- Each images from the catalog will be tagged with appropriate tags


# How to Run
1. Add [Import CSV catalog](https://ecosystem.supervise.ly/apps/import-csv-catalog) to your team from Ecosystem.

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-csv-catalog" src="https://i.imgur.com/t1O1T52.png" width="350px" style='padding-bottom: 20px'/>  

2. Run app from the context menu of the `.CSV` file:

<img src="https://i.imgur.com/8s9IREE.png" width="100%"/>


# Demo Data

- [.CSV table to import example](https://github.com/supervisely-ecosystem/import-csv-catalog/releases/download/v0.0.1/test_snacks_catalog.csv) — table example

# Demo Video
<a data-key="sly-embeded-video-link" href="https://www.youtube.com/watch?v=CbE5l_ObuhQ" data-video-code="CbE5l_ObuhQ">
    <img src="https://i.imgur.com/0fhnAB7.png" alt="SLY_EMBEDED_VIDEO_LINK"  width="70%">
</a>

# Results

After running the application, you will be redirected to the `Tasks` page.  
Once application processing has finished, your project will be available.  
Click on the project name to proceed to it.

<img src="https://i.imgur.com/G4BOKH4.png"/>
