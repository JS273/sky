import os
import shutil
import configargparse

def get_config_demo_model(config_file, result_folder, logger = None):

    p = configargparse.ArgParser(config_file_parser_class=configargparse.YAMLConfigFileParser)
    p.add('-c', default = config_file, is_config_file=True, help='config file path')
    p.add('--amp', default = 1.0, type=float, help='Amplitude of Model 1')
    p.add('--nx', default = 100, type=float, help='Spatial discretization')
    p.add('--freq', default = 10, type=float, help='frequency')
    
    config = p.parse_args()

    # write configs to logger
    if logger is not None: logger.info("User input (cmd > config > default): \n" + p.format_values())    

    # Copy config file to result path
    config_filename = os.path.basename(config_file)
    shutil.copy(config_file, result_folder + "/" + config_filename)

    return config