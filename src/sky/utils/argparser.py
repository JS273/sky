import os
import shutil
import configargparse

def get_config(config_file, result_folder, logger = None):

    p = configargparse.ArgParser(config_file_parser_class=configargparse.YAMLConfigFileParser)
    p.add('-c', default = config_file, is_config_file=True, help='config file path')
    p.add('--seed', default = 0, type=int, help='seed')
    p.add('--device', default = "cpu", type=str, help='device [cpu or gpu]')
    p.add('--train_samples', default = 128, type=int, help='number of training samples')
    p.add('--test_samples', default = 64, type=int, help='number of test samples')
    p.add('--train_batch', default = 8, type=int, help='training batch size')
    p.add('--test_batch', default = 8, type=int, help='test batch size')
    p.add('--optimizer', default = "Adam", type=str, help='optimizer')
    p.add('--precision', default = 32, type=int, help='torch float precision')
    config = p.parse_args()

    # write configs to logger
    if logger is not None: logger.info("User input (cmd > config > default): \n" + p.format_values())    

    # Copy config file to result path
    config_filename = os.path.basename(config_file)
    shutil.copy(config_file, result_folder + "/" + config_filename)

    return config