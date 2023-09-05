from sky.plots.plotlib import *
from sky.plots.datastructures import *

class analytic_model_1d():
    def __init__(self, config, logger = None) -> None:
        self.xlabel = "x"
        self.ylabel = "pressure" 
        self.logger = logger
        self.amp = config.amp
        self.amp2 = config.amp2
        self.freq = config.freq

    def calculate(self, x, returnType = "numpy"):

        if self.logger is not None: self.logger.info("Mod 1 started calculation")

        y = self.amp * np.sin(2 * np.pi * self.freq * x)
        y2 = self.amp2 * np.sin(2 * np.pi * self.freq * x)
        y3 = 4* self.amp2 * np.sin(2 * np.pi * self.freq * x)

        if self.logger is not None: self.logger.info("Mod 1 finished calculation \n")


        plt = LinePlot(x,y)
        plt.x_label = self.xlabel
        plt.y_label = self.ylabel
        plt.color_no = 0
        plt.add_line(y2, legend = "Second Model")

        plt2 = LinePlot(x,y3)
        plt2.xlabel = self.xlabel
        plt2.ylabel = self.ylabel
        plt2.color_no = 1

        if returnType == "plot":
            return [plt, plt2] 
        elif returnType == "numpy":
            return y
        

class analytic_model_2d():
    def __init__(self, logger = None) -> None:
        self.xlabel = "x"
        self.ylabel = "y"
        self.logger = logger

    def calculate(self, x, y, returnType = "numpy"):

        if self.logger is not None: self.logger.info("Mod 2 started calculation")

        grid = Grid(x, y)
        y = np.sin(grid.nodes[:,0]) * np.cos(grid.nodes[:,1])

        if self.logger is not None: self.logger.info("Mod 2 finished calculation \n")

        plt = ContourPlot(grid, y)

        if returnType == "plot":
            return plt 
        elif returnType == "numpy":
            return y





    

