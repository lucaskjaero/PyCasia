# PyCasia
Open source library to work with the [CASIA Chinese Handwriting dataset](http://www.nlpr.ia.ac.cn/databases/handwriting/Home.html).
## Installation
PyCasia is on the [Python Package Index](https://pypi.python.org/pypi/Pycasia), so installation is as easy as `pip install pycasia`. While it may run on Python 2, only Python 3 is officially supported.
## Using the library
The pycasia.CASIA object is the interface for all the data. You can use it to explore the dataset, or use it as a base class for a more complicated use.

### Datasets
Datasets are directories full of data files from a given distribution. They come in isolated character [(GNT)](http://www.nlpr.ia.ac.cn/databases/handwriting/Offline_database.html) or handwritten text [(DGR)](http://www.nlpr.ia.ac.cn/databases/handwriting/Offline_database.html) files. Four are automatically downloaded by the library, but you can add more.

These datasets are downloaded from the publicly available data hosted on the project webpage. You should expect a long download during your first run.
#### Included datasets
`HWDB1.1trn_gnt_P1` and `HWDB1.1trn_gnt_P2` are two parts of the publicly available set for training applications. They were split for easy downloading.
`HWDB1.1tst_gnt` is the training portion of that set.
`competition-gnt` is the dataset from some Chinese handwriting competitions.
#### Adding datasets
To add other datasets, add a new dictionary in the `datasets` variable of the `CASIA` object. You will need to include the download URL and the dataset type, either `GNT` or `DGR`. If you have data that isn't publicly available, make sure there is a folder named after the dataset in the base dataset directory, and the download code won't be called.

Example:
```
CASIA.datasets["competition-gnt"] = {
    "url": "http://www.nlpr.ia.ac.cn/databases/Download/competition/competition-gnt.zip",
    "type": "GNT"
}
```

### Getting the data
You can download all datasets using the `get_all_datasets()` method, or just specific datasets using the `get_dataset(dataset)` method.
#### Dataset Location
On OS X and Linux, datasets are stored in `~/CASIA_data`. On Windows, they're saved in the `CASIA_data` in your home directory. If you want to save the data in a diffent location, specify a path when you create the CASIA object. Eg: `dataset = CASIA(path="/CASIA_data")`

### Using the data
You can load all of the character image (GNT) data using the `load_character_images()` method, or a particular dataset using the `load_dataset(dataset)` method. If you want to read the data on a file by file basis, just use the static `CASIA.load_gnt_file()` method to get the data.

These are generators yielding data as (image, label) pairs. The images are Pillow.Image.Image objects.

### Getting raw data
You may want to explore the data by yourself. You can get the data as JPEGs by calling the `get_raw()` function. You can then inspect the data to your leisure.

### Building your own interfaces on top of PyCasia
You can build your own class to implement more complicated usage of the dataset. Just inherit from `CASIA`.

## Current status:
Early release. Features may change. Can open individual character images (GNT files) but not sentences. So far, no plans to develop readers to use DGR files or online datasets. Pull requests welcome.

## Current Issues
#### Download issues
The datasets are hosted in mainland China, and are often difficult to download from other countries, as the connection gets reset. `get_dataset` attempts the download five times, but sometimes that doesn't work. You can try again, or download the data manually. WGET has been effective for manual downloads.

#### Limited dataset
While useful for many applications, the publicly available data is only a fraction of the total set. If you need more, you should fill out an [application form](http://www.nlpr.ia.ac.cn/databases/handwriting/Application_form.html) from the projects maintainers to get the full set.

#### Copyright issues
The datasets are only licensed for research use, and certainly no commercial use. If you want to publish your data, you should fill out an [application form](http://www.nlpr.ia.ac.cn/databases/handwriting/Application_form.html) from the projects maintainers. You should not host the data in any form, including in your repository.
