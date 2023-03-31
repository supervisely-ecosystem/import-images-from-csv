<div align="center" markdown>
<img src="https://imgur.com/IcPLSjq.png"/>


# CSV to Images Project

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Usage">Usage</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Demo">Demo</a> •
  <a href="#Screenshot">Screenshot</a> 
  
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-images-from-csv)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-images-from-csv)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/import-images-from-csv.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/import-images-from-csv.png)](https://supervise.ly)

</div>

# Overview

Application imports Supervisely Images Project using **.CSV file** 

Application key points:  
- Import Images from **Team Files** (⭐ _fastest_)
- Import Images by <b>URLs</b>
- Automatically **assign Tags** to each Image (_optional_)
- `.CSV` columns delimiter is **`;`** (**semicolon**), tags delimiter is **`,`** (**comma**)


🔥 Starting from version v1.0.7, the application supports cloud storage link integration and data validation features. You can learn how to use sorrage links properly in [this article](https://docs.supervise.ly/enterprise-edition/advanced-tuning/s3#links-plugin-cloud-providers-support).



# Usage



<details>
  <summary>1. Import Images from <b>Team Files</b> ⭐ </summary>
<br>

1. Create `.CSV` file with columns: 
   - **path** — relative path to image, from .CSV file directory and below 
   - **tag(optional)** — image tag  
2. Drag and drop this `.CSV` file and folder(s) with images to Team Files

### Example 1: CSV file in Team Files root and images in subdirectories:


**Path to CSV file**: /images.csv
  
[example 1 — download demo files](https://github.com/supervisely-ecosystem/import-images-from-csv/files/7977236/Example1.zip)
  
```text
path;tag
/dogs/img_01.jpeg;dog
/dogs/img_02.jpeg;dog
/cats/img_01.jpeg;cat
/cats/img_02.jpeg;cat
/horses/img_01.jpeg;horse
/horses/img_02.jpeg;horse
```
  
**Tree**:
```text
.
├── images.csv                                      
├── dogs                    
│ ├── img_01.jpeg
│ └── img_02.jpeg
├── cats
│ ├── img_01.jpeg
│ └── img_02.jpeg
└── horses
  ├── img_01.jpeg
  └── img_02.jpeg
```


### Example 2: CSV file in subdirectory and images on the same level:

**Path to CSV file**: /demo-images-from-csv/images.csv
  
[example 2 — download demo files](https://github.com/supervisely-ecosystem/import-images-from-csv/files/7977235/Example2.zip)
  
```text
path;tag
/img_01.jpeg;dog
/img_02.jpeg;dog
/img_03.jpeg;cat
/img_04.jpeg;cat
/img_05.jpeg;horse
/img_06.jpeg;horse
```

**Tree**:
```text
.
├── some_file_in_root_directory_1.json
├── some_file_in_root_directory_2.json
├── some_file_in_root_directory_3.json
└── demo-images-from-csv
    ├── images.csv
    ├── img_01.jpeg
    ├── img_02.jpeg
    ├── img_03.jpeg
    ├── img_04.jpeg
    ├── img_05.jpeg
    └── img_06.jpeg       
```

### Example 3: CSV file in subdirectory and images subdirectories:

**Path to CSV file**: /demo-images-from-csv/images.csv
  
[example 3 — download demo files](https://github.com/supervisely-ecosystem/import-images-from-csv/files/7977234/Example3.zip)
  
```text
path;tag
/dogs/img_01.jpeg;dog
/dogs/img_02.jpeg;dog
/cats/img_01.jpeg;cat
/cats/img_02.jpeg;cat
/horses/img_01.jpeg;horse
/horses/img_02.jpeg;horse
```

**Tree**:
```text
.
├── some_file_in_root_directory_1.json           
├── some_file_in_root_directory_2.json
└── demo-images-from-csv
  ├── images.csv                    
  ├── dogs
  │ ├── img_01.jpeg
  │ └── img_02.jpeg    
  ├── cats
  │ ├── img_01.jpeg
  │ └── img_02.jpeg   
  └── horses
    ├── img_01.jpeg
    └── img_02.jpeg                      
```

</details>



<details>
  <summary>2. Import Images by <b>URLs</b></summary>

<br>  
  
1. Create `.CSV` file with following columns: 
   - **url** — full URL-link to image, ends with image extension (.jpg, .png)
   - **tag** (optional) — image tag  
2. Drag and drop this `.CSV` file to Team Files  
3. Application will download images by url and upload it to project.

### Example 4:

**Path to CSV file**: any location
  
[example 4 — download demo files](https://github.com/supervisely-ecosystem/import-images-from-csv/files/7977425/Example4.zip)
  
```text
url;tag
https://images.io/image_example_1.png;tag1,tag2
https://images.io/image_example_2.png;tag3
https://images.io/image_example_3.png;
https://images.io/image_example_4.png;big tag with spaces,tag4
https://images.io/image_example_5.png;tag1,tag3
```
</details>

  
# How to Run
1. Add [Import Images from CSV](https://ecosystem.supervise.ly/apps/import-images-from-csv) to your team from Ecosystem.

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-images-from-csv" src="https://imgur.com/Cqe7fjv.png" width="450px" style='padding-bottom: 20px'/>  

2. Run app from the context menu of the `.CSV` file:

<img src="https://imgur.com/s29C9PG.png" width="100%"/>


# Demo
<a data-key="sly-embeded-video-link" href="https://youtu.be/JkZ3Sg-hRH4" data-video-code="JkZ3Sg-hRH4">
    <img src="https://imgur.com/JHPAtHa.jpg" alt="SLY_EMBEDED_VIDEO_LINK"  width="70%">
</a>

# Screenshot

### App interface
<img src="https://user-images.githubusercontent.com/57998637/229188358-9f6cf04a-bb2b-436e-81cd-3ea0493080a6.png" width="1238px"/>


### Cloud storage link example
<img src="https://user-images.githubusercontent.com/57998637/229191946-d58f8da8-e03e-4e81-bcf2-4c8d804a9843.png" width="1198px">
