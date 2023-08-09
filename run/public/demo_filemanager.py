from sky.utils.filemanager import *
import numpy as np

# Create a result folder and save the current script
tag = "Test comp"
result_folder = save_script(os.path.realpath(__file__), tag, max_daily_folders = 7, max_res_folders = 7)

import os

cwd = os.getcwd()

print(cwd)


# Programm
a = np.array([1,2,3])
print(a)

