from sky.filemanager import save_script
from run.test_model.logger import init_logger
from run.test_model.analytic import analytic_model_1d, analytic_model_2d
from run.test_model.argparser import get_config_demo_save_sim             # This module has to be created in every project itself, since it is project specific
import os
import numpy as np

# ---------------------
# --- Setup section ---
# ---------------------

# result folder
tag = "1d_sin_wave"
result_folder = save_script(os.path.realpath(__file__), tag, max_daily_folders = 7, max_res_folders = 7)

# logger
logger = init_logger(result_folder, "logfile")

# Get user input from: cmd line > config file > defaults
config = get_config_demo_save_sim("run\public\save_sim_para\sim_para.yaml", result_folder, logger)
print(config)

# -------------------
# --- Run section ---
# -------------------

# create and run model A
my_mod = analytic_model_1d(config = config, logger = logger)
x = np.linspace(0.0, 10, config.nx)
y = my_mod.calculate(x, returnType= "numpy")
print(np.max(y))

# Create and run model B
my_mod_B = analytic_model_2d(logger = logger)
x_disc = np.linspace(0.0, 10, 100)
y_disc = np.linspace(0.0, 10, 50)
y = my_mod_B.calculate(x_disc, y_disc, returnType= "numpy")
print(y)

