import glob
import struct
import zipfile

from codecs import decode
from collections import Counter
from os import makedirs, remove
from os.path import expanduser, isdir, isfile
from urllib.request import urlretrieve

import numpy as np

from PIL.Image import fromarray

from tqdm import tqdm

from .statusbar import DLProgress

__author__ = 'Lucas Kjaero'


class CASIA:
    """
    Class to download and use data from the CASIA dataset.
    """
    def __init__(self, path=None):
        self.datasets = {
            "competition-gnt": {
                "url": "http://www.nlpr.ia.ac.cn/databases/Download/competition/competition-gnt.zip",
                "type": "GNT",
            },
            "HWDB1.1trn_gnt_P1": {
                "url": "http://www.nlpr.ia.ac.cn/databases/Download/feature_data/HWDB1.1trn_gnt_P1.zip",
                "type": "GNT",
            },
            "HWDB1.1trn_gnt_P2": {
                "url": "http://www.nlpr.ia.ac.cn/databases/Download/feature_data/HWDB1.1trn_gnt_P2.zip",
                "type": "GNT",
            },
            "HWDB1.1tst_gnt": {
                "url": "http://www.nlpr.ia.ac.cn/databases/download/feature_data/HWDB1.1tst_gnt.zip",
                "type": "GNT",
            },
        }
        self.character_sets = [dataset for dataset in self.datasets if self.datasets[dataset]["type"] == "GNT"]
        self.sentence_sets = [dataset for dataset in self.datasets if self.datasets[dataset]["type"] == "DGR"]

        # Set the dataset path
        if path is None:
            self.base_dataset_path = expanduser("~/CASIA_data/")
        else:
            self.base_dataset_path = expanduser(path)

        if not isdir(self.base_dataset_path):
            makedirs(self.base_dataset_path)

    def get_all_datasets(self):
        """
        Make sure the datasets are present. If not, downloads and extracts them.
        Attempts the download five times because the file hosting is unreliable.
        :return: True if successful, false otherwise
        """
        success = True

        for dataset in tqdm(self.datasets):
            individual_success = self.get_dataset(dataset)
            if not individual_success:
                success = False

        return success

    def get_dataset(self, dataset):
        """
        Checks to see if the dataset is present. If not, it downloads and unzips it.
        """
        # If the dataset is present, no need to download anything.
        success = True
        dataset_path = self.base_dataset_path + dataset
        if not isdir(dataset_path):

            # Try 5 times to download. The download page is unreliable, so we need a few tries.
            was_error = False
            for iteration in range(5):

                # Guard against trying again if successful
                if iteration == 0 or was_error is True:
                    zip_path = dataset_path + ".zip"

                    # Download zip files if they're not there
                    if not isfile(zip_path):
                        try:
                            with DLProgress(unit='B', unit_scale=True, miniters=1, desc=dataset) as pbar:
                                urlretrieve(self.datasets[dataset]["url"], zip_path, pbar.hook)
                        except Exception as ex:
                            print("Error downloading %s: %s" % (dataset, ex))
                            was_error = True

                    # Unzip the data files
                    if not isdir(dataset_path):
                        try:
                            with zipfile.ZipFile(zip_path) as zip_archive:
                                zip_archive.extractall(path=dataset_path)
                                zip_archive.close()
                        except Exception as ex:
                            print("Error unzipping %s: %s" % (zip_path, ex))
                            # Usually the error is caused by a bad zip file.
                            # Delete it so the program will try to download it again.
                            try:
                                remove(zip_path)
                            except FileNotFoundError:
                                pass
                            was_error = True

            if was_error:
                print("\nThis recognizer is trained by the CASIA handwriting database.")
                print("If the download doesn't work, you can get the files at %s" % self.datasets[dataset]["url"])
                print("If you have download problems, "
                      "wget may be effective at downloading because of download resuming.")
                success = False

        return success

    def get_raw(self, verbose=True):
        """
        Used to create easily introspectable image directories of all the data.
        :return:
        """
        assert self.get_all_datasets() is True, "Datasets aren't properly downloaded, " \
                                                "rerun to try again or download datasets manually."

        for dataset in self.datasets:
            # Create a folder to hold the dataset
            prefix_path = self.base_dataset_path + "raw/" + dataset
            if not isdir(prefix_path):
                makedirs(prefix_path)

            label_count = Counter()

            for image, label in tqdm(self.load_dataset(dataset, verbose=verbose)):
                #assert type(image) == "PIL.Image.Image", "image is not the correct type. "

                # Make sure there's a folder for the class label.
                label_path = prefix_path + "/" + label
                if not isdir(label_path):
                    makedirs(label_path)

                label_count[label] = label_count[label] + 1

                image.save(label_path + "/%s_%s.jpg" % (label, label_count[label]))

    def load_character_images(self, verbose=True):
        """
        Generator to load all images in the dataset. Yields (image, character) pairs until all images have been loaded.
        :return: (Pillow.Image.Image, string) tuples
        """
        for dataset in self.character_sets:
            assert self.get_dataset(dataset) is True, "Datasets aren't properly downloaded, " \
                                                      "rerun to try again or download datasets manually."

        for dataset in self.character_sets:
            for image, label in self.load_dataset(dataset, verbose=verbose):
                yield image, label

    def load_dataset(self, dataset, verbose=True):
        """
        Load a directory of gnt files. Yields the image and label in tuples.
        :param dataset: The directory to load.
        :return:  Yields (Pillow.Image.Image, label) pairs.
        """
        assert self.get_dataset(dataset) is True, "Datasets aren't properly downloaded, " \
                                                  "rerun to try again or download datasets manually."

        if verbose:
            print("Loading %s" % dataset)

        dataset_path = self.base_dataset_path + dataset
        for path in tqdm(glob.glob(dataset_path + "/*.gnt")):
            for image, label in self.load_gnt_file(path):
                yield image, label

    @staticmethod
    def load_gnt_file(filename):
        """
        Load characters and images from a given GNT file.
        :param filename: The file path to load.
        :return: (image: Pillow.Image.Image, character) tuples
        """

        # Thanks to nhatch for the code to read the GNT file, available at https://github.com/nhatch/casia
        with open(filename, "rb") as f:
            while True:
                packed_length = f.read(4)
                if packed_length == b'':
                    break

                length = struct.unpack("<I", packed_length)[0]
                raw_label = struct.unpack(">cc", f.read(2))
                width = struct.unpack("<H", f.read(2))[0]
                height = struct.unpack("<H", f.read(2))[0]
                photo_bytes = struct.unpack("{}B".format(height * width), f.read(height * width))

                # Comes out as a tuple of chars. Need to be combined. Encoded as gb2312, gotta convert to unicode.
                label = decode(raw_label[0] + raw_label[1], encoding="gb2312")
                # Create an array of bytes for the image, match it to the proper dimensions, and turn it into an image.
                image = fromarray(np.array(photo_bytes, dtype=np.uint8).reshape(height, width))

                yield image, label
