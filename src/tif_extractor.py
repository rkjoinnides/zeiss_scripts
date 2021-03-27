<<<<<<< HEAD
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
=======
import copy
import os
import fileIO

# This class holds the data for the SmartSEM tiff images


class TiffData():

    def __init__(self, file_path: str):

        self._file_path = file_path
        self.file_name = file_path.split("\\")[-1]
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

    # Helper fcn to determine if a line contains a parmeter
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

    def get_data(self):
        return copy.deepcopy(self._processed_data)

    def get_matching_data(self, entries_to_match: list):
        data = []
        for entry in entries_to_match:
            if entry in self._processed_data:
                data.append(self._processed_data[entry])
        return data


# Creates a config file if one does not exist, oterwise reads config data
def setup_config_file(config_file_path: str, required_data: dict):

    if not os.path.isfile(config_file_path):
        fileIO.create_config_file(config_file_path, required_data)

    else:
        fileIO.verify_config_fields(config_file_path, required_data)

    return fileIO.read_config_data(config_file_path)


def create_tifs(path_to_tifs: list):

    tiff_objects = []
    for path in path_to_tifs:
        tiff_objects.append(TiffData(path))

    return tiff_objects


def create_parameter_list(tiff_data: TiffData, exclusion_mode: int):

    parameter_list = []

    # Include selected
    if exclusion_mode == 1:
        pass
    # Exclude selected
    elif exclusion_mode == 2:
        pass
    # Include all
    else:
        parameter_list = tiff_data.get_data().keys()

    return parameter_list


def create_header(tiff_data: TiffData, run_settings: dict):

    header = ["Filename"]
    exclusion_mode = int(run_settings["General"]["parameter selection mode"])
    selected_params = [x.upper() for x in run_settings["Parameters"]]

    # Include selected
    if exclusion_mode == 1:
        tmp_params = [x for x in tiff_data.get_data() if x in selected_params]
    # Exclude selected
    elif exclusion_mode == 2:
        tmp_params = [x for x in tiff_data.get_data() if x not in selected_params]
    # Include all
    else:
        tmp_params = copy.copy(tiff_data.get_data())

    header.extend(tmp_params)

    return header


def create_csv_data(tif_data: list, header: list):

    data_list = []
    for tif in tif_data:
        tmp_data = [tif.file_name]
        tmp_data.extend(tif.get_matching_data(header))
        data_list.append(tmp_data)
    return data_list


def find_verbose_tif(tif_data: list):
    selected_tif = tif_data[0]
    for tif in tif_data:
        if len(tif.get_data().keys()) > len(selected_tif.get_data().keys()):
            selected_tif = tif
    return tif


def write_data_to_csv(tif_data: list, run_settings: dict):

    # Get run parameters from the config file
    path_to_csv = run_settings["General"]["csv directory"] + "\\tif_data.csv"

    if not os.path.isfile(path_to_csv):
        with open(path_to_csv, "w") as csv:
            csv.close()

    verbose_tif = find_verbose_tif(tif_data)

    # Form header and data in list form
    header = create_header(verbose_tif, run_settings)
    data = create_csv_data(tif_data, header)

    # Write header and data to csv
    fileIO.write_list_to_csv(data, header, path_to_csv)


if __name__ == "__main__":

    # Special list of most relevant Parameters
    selected_params = {"AP_BEAMSHIFT_X": None, "AP_BEAMSHIFT_Y": None, "AP_STIG_X": None,
                       "AP_STIG_Y": None, "AP_APERTURE_X": None, "AP_APERTURE_Y": None,
                       "AP_TARGETKV": None, "AP_IMAGE_PIXEL_SIZE": None, "AP_MAG": None,
                       "AP_WD": None, "DP_DWELL_TIME": None}

    # Specify necessary config data
    default_data = {"General": {"search directory": os.getcwd(), "parameter selection mode": "1",
                                "csv directory": os.getcwd()}, "Parameters": selected_params}

    # Read or create config if it does not exist
    script_settings = setup_config_file(os.getcwd() + "\\tif_extractor_config.ini", default_data)
    # Find all files that have .tif extensions
    tif_paths = fileIO.find_files(script_settings["General"]["search directory"], ".tif")
    # Create tif objects from file paths
    tif_data = create_tifs(tif_paths)

    # Write the tif data to csv
    write_data_to_csv(tif_data, script_settings)
>>>>>>> e76666121c1b41b8b6c864958a5e908059c39b07
