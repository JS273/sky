from sky.filemanager import save_script
from sky.plotlib import Plotter
import os, sys
import numpy as np

# Add path to demo model 
sys.path.append(os.path.abspath("./run/public/"))
from demo_model.analytic import analytic_model_2d

# ---------------------
# --- Setup section ---
# ---------------------

# result folder
tag = "1d_sin_wave"
result_folder = save_script(os.path.realpath(__file__), tag, max_daily_folders = 7, max_res_folders = 7)


# -------------------
# --- Run section ---
# -------------------

# create and run model A
my_mod = analytic_model_2d()
x = np.linspace(0.0, 10, 10)
y = np.linspace(0.0, 10, 20)
plt = my_mod.calculate(x,y, returnType= "plot")

# ----------------
# --- Plotting ---
# ----------------

# Plotting
plotter = Plotter(save_path = result_folder, save_format= "latex", ink_path= r'C:\Program Files\Inkscape')
_ = plotter.plot(plt, filename = f'{tag}')

