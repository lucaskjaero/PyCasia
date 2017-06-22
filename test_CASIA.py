from os.path import isdir
from unittest import TestCase

from PIL import Image

from CASIA import CASIA


class TestCASIA(TestCase):
    def setUp(self):
        self.casia = CASIA()

        # We need at least one dataset to run tests on. Might as well try the smallest one.
        self.casia.get_dataset("HWDB1.1tst_gnt")

    def test_get_all_datasets(self):
        # Make sure that the proper number of datasets are checked.
        self.assertEqual(len(self.casia.datasets), 4)

        # We don't need to test get_dataset because this runs them all
        self.casia.get_all_datasets()
        for dataset in self.casia.datasets:
            self.assertTrue(isdir(dataset))

    def test_load_character_images(self):
        for image, character in self.casia.load_character_images():
            self.assertEquals(type(image), Image.Image)
            self.assertEquals(len(character), 1)
