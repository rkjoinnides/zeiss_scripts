import unittest
import os
import random
import string

import context
from src import fileIO

# class File_IOTests(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls, self):
#         cls.test_dir = ".\\test_dir"
#         os.mkdir(cls.test_dir)
#         os.chdir(cls.test_dir)

#         f = open("exampletif1.tif", "w")
#         f.close()

#     @classmethod
#     def tearDownClass(cls, self):

#         os.remove("exampletif1.tif")
#         os.chdir("..")
#         os.rmdir(cls.test_dir)

#     # find files finds all files
#     def test_find_files(self):
#         l1 = file_IO.find_files(".", ".tif")
#         self.assertEqual(len(l1), 1)


# class GeneralTest(unittest.TestCase):

#     def test1(self):
#         self.assertEqual(1, 1)

class ConfigHandlingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create a directory for testing and enter
        cls.test_dir = ".\\ConfigHandlerTestDir"
        os.mkdir(cls.test_dir)
        os.chdir(cls.test_dir)

        # create a number of config files
        cls.config_file_names = []

        for i in range(20):

            config_file_name = "Config" + str(i) + ".ini"
            data = generate_random_config_data()
            fileIO.create_config_file(".\\" + config_file_name, data)
            cls.config_file_names.append(config_file_name)

    @classmethod
    def tearDownClass(cls):

        # remove the created config files
        for f in cls.config_file_names:
            os.remove(f)

        # exit the testing directory and remove it
        os.chdir("..")
        os.rmdir(cls.test_dir)

    # Check that all files were created
    def test_creation1(self):
        msg = "The file "
        file_exists = True
        for f in self.config_file_names:
            if not os.path.isfile(".\\" + f):
                file_exists = False
                msg += "f does not exist!"
                break
        self.assertTrue(file_exists, msg)

    # Check that already existing file is not re-created
    def test_creation2(self):
        fileIO.create_config_file(".\\Config0.ini")


def generate_random_config_data():

    data = {}
    num_sections = random.randint(1, 50)

    for s in range(num_sections):
        section_length = random.randint(1, 25)
        section_name = "".join(random.choices(string.ascii_letters + string.digits,
                               k=section_length))
        data[section_name] = {}

        num_fields = random.randint(1, 50)
        for f in range(num_fields):
            field_length = random.randint(1, 25)
            field_name = "".join(random.choices(string.ascii_letters + string.digits,
                                 k=field_length))

            entry_length = random.randint(1, 25)
            entry_content = "".join(random.choices(string.ascii_letters + string.digits,
                                    k=entry_length))

            data[field_name] = entry_content

    return(data)


if __name__ == "__main__":

    unittest.main()
