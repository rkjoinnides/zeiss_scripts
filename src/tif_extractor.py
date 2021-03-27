import copy
import os

import file_IO


class TiffData():

    def __init__(self, file_path: str):

        self._file_path = file_path
        self._raw_data_chunk = self._form_chunk()

        self._processed_data = {}
        self.assign_values()

    # This function returns a list containing the relevant SmartSEM parameters
    def _form_chunk(self):

        # Try and open the file
        try:
            f = open(self._file_path, 'rb')
        except FileNotFoundError:
            raise("No such file %s", self._file_path)

        start_found = False
        chunk = []
        parameter_prefixes = ["AP", "DP"]
        line_param = last_line_param = False

        # Iterate through the file looking for first and last parameters
        for i, line in enumerate(f):

            line_param = (self._contains_parameter(line.decode("ANSI"),
                          parameter_prefixes))

            # case for first found parameter
            if (line_param and (not start_found)):
                start_found = True

            # Check if this is the last valid line
            if (not line_param and not last_line_param and start_found):
                break

            if start_found:
                chunk.append(line.decode("ANSI").strip("\r\n"))

            last_line_param = line_param

        f.close()

        return chunk

    def _contains_parameter(self, line: str, prefixes: list, prefix_length=2):

        if (line[0:prefix_length] in prefixes):
            return True
        return False

    # The structure of the data chunk is that the even lines contains the
    # smartSEM parameter names, the line directly after contains the parameter
    # value.

    def assign_values(self):

        last_param = ""

        for i, line in enumerate(self._raw_data_chunk):

            # Even lines contain smartSEM parameter names
            if i % 2 == 0:
                self._processed_data[line] = []
                last_param = line

            # Odd lines contain parameter values
            else:
                self._processed_data[last_param].append(line)

    def get_values(self):
        return copy.deepcopy(self._processed_data)


# Creates a config file if one does not exist, oterwise reads config data
def setup_config_file(config_file_path):

    required_data = {"Section1": {"s1t1": "aaa", "s1t2": "bbb"},
                     "Section2": {"s2t1": "ccc", "s2t2": "ddd"}}

    if not os.isfile(config_file_path):
        file_IO.create_config_file(config_file_path, required_data)

    else:
        file_IO.verify_config_fields(config_file_path, required_data)


def create_tifs(path_to_tifs: list):

    tiff_objects = []
    for path in path_to_tifs:
        tiff_objects.append(TiffData(path))

    return tiff_objects


if __name__ == "__main__":

    tiff_files = file_IO.find_files(".", ".tif")
    t = create_tifs(tiff_files)
    print(t)
