import unittest
import os
import context

from src import file_IO


class File_IOTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls, self):
        cls.test_dir = ".\\test_dir"
        os.mkdir(cls.test_dir)
        os.chdir(cls.test_dir)

        f = open("exampletif1.tif", "w")
        f.close()

    @classmethod
    def tearDownClass(cls, self):

        os.remove("exampletif1.tif")
        os.chdir("..")
        os.rmdir(cls.test_dir)

    # find files finds all files
    def test_find_files(self):
        l1 = file_IO.find_files(".", ".tif")
        self.assertEqual(len(l1), 1)


class GeneralTest(unittest.TestCase):

    def test1(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":

    unittest.main()
