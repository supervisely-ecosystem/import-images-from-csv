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
- `.CSV` file have to contain one of the following columns: **url** or **path**. If column **url** is defined then app will download image by url and upload it to project. If column **path** is defined then app will treat it as a relative path with respect to `.CSV` file location, get image from Team Files and add it to project. Both **url** and **path** columns can not be defined at the same time, use only one of them.
- `.CSV` file may contain optional column **tag**. If this column is defined, corresponding tags will be added to the image during import. Delimiter in **tags** column is **`;`** (**semicolon**)
- `.CSV` columns delimiter is **`,`** (**comma**)
- If you want to import images by **paths**, you must use relative paths to images from `.CSV` file

# Prepare Data in Team Files

## 1. Images from URLs

1. Create `.CSV` file with columns: **url**, **tag(optional)**
2. Drag and drop this `.CSV` file to Team Files

`.CSV` file with **urls** example([download]()):
```text
url,tag
https://images.io/image_example_1.png,tag1;tag2
https://images.io/image_example_2.png,tag3
https://images.io/image_example_3.png,
https://images.io/image_example_4.png,big tag with spaces;tag4
https://images.io/image_example_5.png,tag1;tag3
```

## 2. Images from Paths
1. Create `.CSV` file with columns: **path**, **tag(optional)**
2. Drag and drop this `.CSV` file and folder(s) with images to Team Files

### Example 1: CSV file in Team Files root and images in subdirectories:

`.CSV` file with **paths** example([download]()):

**Path to CSV file**: /images.csv
```text
path,tag
/dogs/img_01.jpeg,dog
/dogs/img_02.jpeg,dog
/cats/img_01.jpeg,cat
/cats/img_02.jpeg,cat
/horses/img_01.jpeg,horse
/horses/img_02.jpeg,horse
```

### Example 2: CSV file in subdirectory and images on the same level:

`.CSV` file with **paths** example([download]()):

**Path to CSV file**: /demo-images-from-csv/images.csv
```text
path,tag
/img_01.jpeg,dog
/img_02.jpeg,dog
/img_03.jpeg,cat
/img_04.jpeg,cat
/img_05.jpeg,horse
/img_06.jpeg,horse
```


### Example 3: CSV file in subdirectory and images subdirectories:

`.CSV` file with **paths** example([download]()):

**Path to CSV file**: /demo-images-from-csv/images.csv
```text
path,tag
/dogs/img_01.jpeg,dog
/dogs/img_02.jpeg,dog
/cats/img_01.jpeg,cat
/cats/img_02.jpeg,cat
/horses/img_01.jpeg,horse
/horses/img_02.jpeg,horse
```

# How to Run
1. Add [Import Images from CSV](https://ecosystem.supervise.ly/apps/import-images-from-csv) to your team from Ecosystem.

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-images-from-csv" src="https://i.imgur.com/vW65imr.png" width="450px" style='padding-bottom: 20px'/>  

2. Run app from the context menu of the `.CSV` file:

<img src="https://i.imgur.com/6Ej5E8C.png" width="100%"/>

3. Wait until the app is started, press `Open` button in `Workspace tasks`

<img src="https://i.imgur.com/FDMhaqu.png" width="100%"/>


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
