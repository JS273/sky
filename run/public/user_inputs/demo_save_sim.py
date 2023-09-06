from sky.filemanager import save_script
import os, sys
import numpy as np
import matplotlib.pyplot as plt

# Add path to demo model 
sys.path.append(os.path.abspath("./run/public/"))
from demo_model.utils.logger import init_logger
from demo_model.analytic import analytic_model_1d
from demo_model.utils.argparser import get_config_demo_model            # This module has to be created in every project itself, since it is project specific

# ---------------------
# --- Setup section ---
# ---------------------

# result folder
tag = "1d_sin_wave"
result_folder = save_script(os.path.realpath(__file__), tag, max_daily_folders = 7, max_res_folders = 7)

# logger
logger = init_logger(result_folder, "logfile")

# Get user input from: cmd line > config file > defaults
config = get_config_demo_model("run\public\save_sim_para\sim_para.yaml", result_folder, logger)
print(config)

# -------------------
# --- Run section ---
# -------------------

# create and run model A
my_mod = analytic_model_1d(config = config, logger = logger)
x = np.linspace(0.0, 10, config.nx)
y = my_mod.calculate(x, returnType= "numpy")

# ----------------
# --- Plotting ---
# ----------------

# Plotting
fig, ax = plt.subplots()
ax.plot(x,y)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Demo')
plt.savefig(result_folder + "/" + tag + "_plot.pdf")

plt.show()

