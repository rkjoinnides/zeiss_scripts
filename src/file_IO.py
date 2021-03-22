import configparser
import os
import csv


# Create an ini file using dict and path
def create_config_file(config_file_path: str, data: dict):

    if os.path.isfile(config_file_path):
        print("Config file {} already exists!".format(config_file_path))
        return

    # copy the data to configparser obj
    config_data = configparser.ConfigParser()
    for section in data:
        config_data[section] = {}
        for field in data[section]:
            config_data[section][field] = data[section][field]

    with open(config_file_path, "w") as cf:
        config_data.write(cf)

    # print("Created config file at ", config_file_path)


# Verifies that all fields within default data exist, creates them if not
def verify_config_fields(config_file_path: str, default_data: dict):

    write_needed = False
    read_data = configparser.ConfigParser()
    read_data.read(config_file_path)

    for section in default_data:

        # Create section if not there
        if section not in read_data:
            read_data[section] = {}

        for field in default_data[section]:

            if field not in read_data[section]:
                read_data[section][field] = default_data[section][field]

    if write_needed:
        read_data.write(config_file_path)


# Returns a copy of config file data (assumes config file exists)
def read_config_data(conifg_file_path: str):

    data_to_return = {}
    config_data = configparser.ConfigParser()
    config_data.read(conifg_file_path)

    for section in config_data:
        data_to_return[section] = {}
        for field in config_data[section]:
            data_to_return[section][field] = config_data[section][field]

    return data_to_return


def find_files(search_path: str, file_pattern: str):

    files_to_return = []

    for path, subdirs, files in os.walk(search_path):

        for name in files:

            if name.rfind(file_pattern) != -1:

                files_to_return.append(path + "\\" + name)

    return files_to_return


def write_list_to_csv(data: list, header: list = None, file_path: str = None):

    if file_path is None:
        file_path = os.getcwd() + "\\data.csv"

    with open(file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        if header is not None:
            csv_writer.writerow(header)
        for entry in data:
            csv_writer.writerows(data)


if __name__ == "__main__":
    test_dict = {"TestSection": {"test1": "a", "test2": "b"}}
    create_config_file(os.getcwd() + "\\testConfig", test_dict)
