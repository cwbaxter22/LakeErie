import unittest
import sys

sys.append("../../src/backend")
from data_transformer import DataTransformer

class TestDataTransformer(unittest.TestCase):
    
    # test to make sure that the function can call DataLoader.get_devices()

    # test to make sure that the file path of <raw>/<project> exists

    # test to make sure that the file path of <raw>/<project>/<device_name> exists

    # test to make sure that the directory <raw>/<project>/<device_name> contains csv files
    
    # test to make sure that across_parameter_aggregate can read in a csv

    # test to make sure that across_parameter_aggregate only merges files that follow the format: <device_name>_<parameter_name>.csv

    # test to make sure that a file from a different device doesn't get merged with other devices. 

    # test to make sure that across_parameter_aggregate only merges one file per parameter
        # throw an error if it detects to files with the same parameter name

    # test to make sure that across_parameter_aggregate can merge two csv files

    # test to make sure that the directory <processed> exists

    # test to make sure that the directory <processed>/<project> exists

    # test to make sure that the directory <processed>/<project>/<device_name> exists

    # test to make sure that across_parameter_aggregate can write a csv file

    # test to make sure that that csv file is named all_data.csv
    # test to make sure that the csv file is written to the correct directory
    # test to make sure that the csv file data follows the format times, parameter, value, units



    # test to make sure that device_aggregate runs for every device

    # test to make sure that tidy_data_transform 




    def test_(self): 
        pass