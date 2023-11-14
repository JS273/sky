import os
import pickle
import glob
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cm
from matplotlib.patches import Rectangle
from collections.abc import Iterable 
import copy
from sky.pdftex_export import latex_graphic_export

class Axes2D:
    def __init__(self, x_label = "x", y_label = "f(x)") -> None:
        self.x_label = x_label
        self.x_scale = 'linear'
        self.xlim = [None, None]
        self.draw_xticks = True
        self.draw_xlabel = True

        self.y_label = y_label
        self.y_scale = 'linear'
        self.ylim = [None, None]
        self.draw_yticks = True
        self.draw_ylabel = True

        self.axis_equal = False
        self.plot_grid = True
        self.title = ''
        self.leg_pos = 'best'
    
    def set_2D_ax_properties(self, ax):
        
        ax.set_xscale(self.x_scale)
        if self.xlim[0] is not None or self.xlim[1] is not None:
            ax.set_xlim(left = self.xlim[0], right = self.xlim[1])
        
        ax.set_yscale(self.y_scale)
        if self.ylim[0] is not None or self.ylim[1] is not None:
            ax.set_ylim(bottom = self.ylim[0], top = self.ylim[1])

        ax.grid(self.plot_grid)

        ax.set_title(self.title)
               
        if self.draw_xlabel:
            ax.set_xlabel(self.x_label)
        else:
            ax.set_xlabel("")

        if self.draw_ylabel:
            ax.set_ylabel(self.y_label)
        else:
            ax.set_ylabel("")
        
        ax.tick_params(labelbottom = self.draw_xticks, labelleft = self.draw_yticks)

        if self.axis_equal:
            ax.axis('equal')

        return ax

class LinePlot(Axes2D):
    def __init__(self, x, y, x_label = "x", y_label = "f(x)", **kwargs):
        super().__init__(x_label, y_label)
        self.x = x
        self.y = y
        self.kwargs = kwargs

        # Default line properties
        self.linewidth = 2.0
        self.linestyle = '-'
        self.color_no = None
        self.default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

        # Set custom Plot Style
        self.set_default_line_kwargs()
        
    def set_default_line_kwargs(self):

        if 'linestyle' not in self.kwargs:
            self.kwargs["linestyle"] = self.linestyle

        if 'linewidth' not in self.kwargs:
            self.kwargs["linewidth"] = self.linewidth

    def add_line(self, y, legend = ""):

        if self.y.ndim == 1:
            self.y = self.y.reshape(-1,1)
        
        y = y.reshape(-1,1)

        self.y = np.concatenate([self.y, y], axis = 1) 

    def plot(self, ax):
        self.set_default_line_kwargs()

        if self.color_no is not None:
            self.kwargs["color"] = self.default_colors[self.color_no]

        ax.plot(self.x, self.y, **self.kwargs)
        
        ax = self.set_2D_ax_properties(ax)

        return ax

class HistPlot(Axes2D):
    def __init__(self, y, x_label = 'x', y_label = 'f(x)', **hist_kwarg):
        super().__init__(x_label, y_label)
        self.y = y
        self.hist_kwarg = hist_kwarg

        self.legend = '_'

        # Default hist properties
        self.bins = None
        self.density = True

        # Set custom Plot Style
        self.set_default_hist_kwargs()
        
    def set_default_hist_kwargs(self):

        if 'bins' not in self.hist_kwarg:
            self.hist_kwarg["bins"] = self.bins

        if 'density' not in self.hist_kwarg:
            self.hist_kwarg["density"] = self.density

    def plot(self, ax):
        self.set_default_hist_kwargs()

        ax.hist(self.y, **self.hist_kwarg)
        
        ax = self.set_2D_ax_properties(ax)

        return ax
    
class vectorFieldPlot():
    def __init__(self, x, y, dx, dy, **vec_kwarg):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.line_kwargs = vec_kwarg

        # Default ax properties
        self.x_label = "x"
        self.x_scale = 'linear'
        self.draw_xticks = True
        self.draw_xlabel = True

        self.y_label = "f(x)"
        self.y_scale = 'linear'
        self.draw_yticks = True
        self.draw_ylabel = True

        self.plot_grid = True
        self.title = ''
        self.legend = []

        # Default line properties
        self.linewidth = 2.0
        self.linestyle = '-'
        self.color_no = None
        self.default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

        # Set custom Plot Style
        self.set_default_line_kwargs()
        
    def set_default_line_kwargs(self):

        if 'linestyle' not in self.line_kwargs:
            self.line_kwargs["linestyle"] = self.linestyle

        if 'linewidth' not in self.line_kwargs:
            self.line_kwargs["linewidth"] = self.linewidth

    def plot(self, ax):

        if self.color_no is not None:
            self.line_kwargs["color"] = self.default_colors[self.color_no]

        ax.quiver(self.x, self.y,self.dx, self.dy, **self.line_kwargs)
        ax.set_yscale(self.y_scale)
        ax.set_xscale(self.x_scale)
        ax.grid(self.plot_grid)
        ax.set_title(self.title)
        ax.tick_params(labelbottom = self.draw_xticks, labelleft = self.draw_yticks)
        return ax

class BarPlot(Axes2D):
    def __init__(self, y, x = None, x_label = "x", y_label = "f(x)", **bar_kwargs):
        super().__init__(x_label, y_label)
        self.y = y.flatten()
        self.bar_kwargs = bar_kwargs

        if x is None:
            self.x = np.arange(self.y.shape[0])

        # Special ax properties
        self.legend = []
        self.x_ticklabels = None
        self.x_ticklabels_rot = 0

    def plot(self, ax):

        ax.bar(self.x, self.y, **self.bar_kwargs)
        
        if self.x_ticklabels is not None:
            ax.set_xticks(np.asarray([i for i in range(len(self.x_ticklabels))]))
            ax.set_xticklabels(self.x_ticklabels, rotation= self.x_ticklabels_rot)

        ax = self.set_2D_ax_properties(ax)

        return ax

class ContourPlot(Axes2D):
    def __init__(self, domain_grid, grid_val, **kwargs):
        super().__init__()

        self.grid = domain_grid
        self.grid_val = grid_val
        self.kwargs = kwargs

        # Special ax properties
        self.cbar = False
        self.cbar_label = ""
        self.cbar_ticks = None
        self.x_label = self.grid.labels[0]
        self.y_label = self.grid.labels[1]

        self.legend = []

        # Default cont properties
        self.levels = 50
        self.cmap = "viridis"

        # Set custom Plot Style
        self.set_default_cont_kwarg()

    def set_default_cont_kwarg(self):

        if 'levels' not in self.kwargs:
            self.kwargs["levels"] = self.levels

        if 'cmap' not in self.kwargs:
            self.kwargs["cmap"] = self.cmap
        
    def plot(self, ax):

        self.set_default_cont_kwarg()

        xx = self.grid.meshgrid_mat[0]
        yy = self.grid.meshgrid_mat[1]

        if self.grid_val.ndim == 2:
            zz = self.grid_val
        else:
            zz = self.grid.reshape_data(self.grid_val)
            
        cs = ax.contourf(xx,yy,zz, **self.kwargs)
        if self.cbar:
            if self.cbar_ticks is not None:
                cbar = plt.colorbar(cs, ax = ax, ticks = self.cbar_ticks)
            else: 
                cbar = plt.colorbar(cs, ax = ax)
            cbar.set_label(self.cbar_label)

        ax = self.set_2D_ax_properties(ax)
    
        return ax

class ImagePlot(Axes2D):
    def __init__(self, image, x_label = "x", y_label = "y", **img_kwargs):
        super().__init__(x_label, y_label)
        self.image = image
        self.img_kwargs = img_kwargs
        self.legend = ""

    def plot(self, ax):

        ax.imshow(self.image, **self.img_kwargs)
       
        ax = self.set_2D_ax_properties(ax)

        return ax

class ScatterPlot(Axes2D):
    def __init__(self, x, y, s = None, **scatter_kwargs):
        super().__init__()
        self.x = x
        self.y = y
        self.s = s
        self.scatter_kwargs = scatter_kwargs
        self.legend = []

        # Special ax properties
        self.x_label = "x"
        self.y_label = "y"
        self.fill_color = '#1f77b4'
        self.alpha = 0.5

        # Update kwargs
        self.set_default_cont_kwargs()

    def set_default_cont_kwargs(self):

        if 'c' not in self.scatter_kwargs:
            self.scatter_kwargs["c"] = self.fill_color

        if 'alpha' not in self.scatter_kwargs:
            self.scatter_kwargs["alpha"] = self.alpha

    def plot(self, ax):

        ax.scatter(self.x, self.y, s = self.s, **self.scatter_kwargs)
        
        ax = self.set_2D_ax_properties(ax)

        return ax

class ScatterGridPlot(Axes2D):
    def __init__(self, domain_grid, grid_val, **scatter_kwargs):
        super().__init__()
        self.grid = domain_grid
        self.grid_val = grid_val
        self.scatter_kwargs = scatter_kwargs
        self.legend = []

        # Special ax properties
        self.x_label = self.grid.labels[0]
        self.y_label = self.grid.labels[1]
        self.fill_color = '#1f77b4'
        self.alpha = 0.5

        # Update kwargs
        self.set_default_cont_kwargs()

    def set_default_cont_kwargs(self):

        if 'c' not in self.scatter_kwargs:
            self.scatter_kwargs["c"] = self.fill_color

        if 'alpha' not in self.scatter_kwargs:
            self.scatter_kwargs["alpha"] = self.alpha

    def plot(self, ax):

        x = self.grid.nodes[:,0]
        y = self.grid.nodes[:,1]
        z = self.grid_val
        ax.scatter(x,y, s = z, **self.scatter_kwargs)
        
        ax = self.set_2D_ax_properties(ax)

        return ax

class RectanglePlot(Axes2D):
    def __init__(self, xy, width, height, **rect_kwargs) -> None:
        super().__init__("x", "y")
        self.xy = xy
        self.width = width
        self.height = height
        self.rect_kwargs = rect_kwargs

        # Special ax properties
        self.legend = []
        self.facecolor = 'none'
        self.edgecolor = 'black'
        self.lw = 1
 
        # Update kwargs
        self.set_default_rect_kwargs()

    def set_default_rect_kwargs(self):

        if 'facecolor' not in self.rect_kwargs:
            self.rect_kwargs["facecolor"] = self.facecolor

        if 'edgecolor' not in self.rect_kwargs:
            self.rect_kwargs["edgecolor"] = self.edgecolor

        if 'lw' not in self.rect_kwargs:
            self.rect_kwargs["lw"] = self.lw

    def plot(self, ax):
        ax.add_patch(Rectangle(self.xy, self.width, self.height, **self.rect_kwargs))
       
        ax = self.set_default_rect_kwargs(ax)
    
        return ax

class PlotData():
    def __init__(self, plots, filename, savepath, stylesheet, fig_size, custom_fig, subplot_grid, col_sort):
        self.plots = plots
        self.filename = filename
        self.fig_size = fig_size
        self.custom_fig = custom_fig
        self.savepath = savepath
        self.stylesheet = stylesheet
        self.subplot_grid = subplot_grid
        self.col_sort = col_sort     

class Plotter():
    def __init__(self, save_path = None, stylesheet = None, save_format = "pdf", ink_path = r'C:\Program Files\Inkscape', save_plot_data = True, open_saved_plot = True):

        self.save_path = save_path
        self.save_format = save_format
        self.stylesheet = stylesheet
        self.save_plot_data = save_plot_data
        self.open_saved_plot = open_saved_plot
        self.ink_path = ink_path

    def plot(self, *plots, filename = None, fig_size = None, fig_title = None, subplot_grid = None, custom_fig = None, col_sort = True):

        if filename is not None: filename = filename.replace(" ", "_")
        n_subplots = len(plots)

        # load stylesheet if specified
        if self.stylesheet is not None:
            plt.style.use(self.stylesheet)

        # Create figure and ax object
        if custom_fig is not None:
            fig = copy.deepcopy(custom_fig[0])
            ax = copy.deepcopy(custom_fig[1])
        else:
            fig, ax = create_figure(n_subplots, subplot_grid, fig_size, col_sort = col_sort)

        # Loop over subplots
        for i, subplot in enumerate(plots):

            has_legend = False
            
            # Loop over plots in subplot
            if not isinstance(subplot, Iterable): subplot = [subplot]
            for j, plot_item in enumerate(subplot):
                                    
                ax[i] = plot_item.plot(ax[i])

                if not ax[i].get_legend_handles_labels() == ([], []): has_legend = True        
                if has_legend: ax[i].legend(loc = plot_item.leg_pos)
        
        if fig_title is not None:
            fig.suptitle(fig_title)    

        plt.tight_layout()
        # Saving
        if self.save_path is None:
            plt.show()

        else:
            unique_filename = self.save_plot(self.save_path, filename, fig)
            if self.save_plot_data:
                data_filename = self.save_path + "/data_" +  unique_filename + ".pkl"
                plt_data = PlotData(plots, filename, self.save_path, self.stylesheet, fig_size, custom_fig, subplot_grid, col_sort)
                with open(data_filename, 'wb') as file:
                    pickle.dump(plt_data, file)

                self.create_plotfile(self.save_path, unique_filename, data_filename)

        return fig, ax

    def save_plot(self, path, filename, fig):
        
        # Output Folder
        now = datetime.now()
        time_string = now.strftime("%H_%M_%S")
        
        if filename is None:
            name = "Plot"
        else:
            name = filename
        unique_filename = time_string + "_" + name

        if self.save_format == "pdf":
            plt.savefig(path + "/" +  unique_filename + ".pdf") 
        elif self.save_format == "png":
            plt.savefig(path + "/" +  unique_filename + ".png", format='png', dpi = 600)
        elif self.save_format == "latex":
            cwd = os.getcwd()
            filepath = os.path.join(cwd, path)
            latex_graphic_export(fig, graphic_name=unique_filename,
                                 file_path=filepath,
                                 use_replacing_rules = True,
                                 use_si_pack = True,
                                 ink_dir= self.ink_path)
            unique_filename = unique_filename + "Control"
            os.chdir(cwd)

        # Open PDF in vs code
        if self.open_saved_plot:
            if self.save_format == "latex":
                save_format = "pdf"
            else:
                save_format = self.save_format
            system_command = "code " + path + "/" +  unique_filename + "." + save_format
            os.system(system_command)

        return unique_filename
    
    def create_plotfile(self, path, filename, data_file_path):
        
        # Get package name:
        # folder = glob.glob("./src/*.egg-info")
        # file = folder[0] + "/top_level.txt"
        # with open(file) as f:
        #     pkg_name = f.read().replace('\n', '')

        f= open(path + "/" +  filename + ".py","w")
        f.write(f"from sky.plotlib import * \nimport numpy as np\nimport pickle \n \n# Load plot data \n")
        f.write(f"file_path = '{data_file_path}' \n")
        f.write("with open(file_path, 'rb') as file:\n")
        f.write("   plt_data = pickle.load(file) \n\n")
        f.write("save_path = plt_data.savepath \n")
        f.write("plots = plt_data.plots \n")
        f.write("stylesheet = plt_data.stylesheet \n")
        f.write("filename = plt_data.filename \n")
        f.write("fig_size = plt_data.fig_size \n")
        f.write("custom_fig = plt_data.custom_fig \n")
        f.write("col_sort = plt_data.col_sort \n")
        f.write("subplot_grid = plt_data.subplot_grid \n \n")

        f.write("# Recreate plot \n")
        f.write("folder_path = save_path + '/regenerated_plots' \n")
        f.write("isExist = os.path.exists(folder_path) \n")
        f.write("if not isExist: \n")
        f.write("   os.makedirs(folder_path)\n")
        f.write("plotter = Plotter(save_path = save_path + '/regenerated_plots', stylesheet= stylesheet, save_plot_data = False) \n")
        f.write("plotter.plot(*plots, filename = filename, fig_size = fig_size, custom_fig = custom_fig, subplot_grid = subplot_grid, col_sort = col_sort) \n")

def create_figure(n_subplots, subplot_grid, fig_size, col_sort = True):
        if fig_size is not None:
            fig_size = np.asarray(fig_size)
            fig_size = fig_size / 2.54      # translate cm to inch
        
        if subplot_grid is not None:

            if n_subplots != subplot_grid[0]*subplot_grid[1]:
                raise ValueError("The number of subplots and the user defined subplot grid are not matching")

            n_row = subplot_grid[0]
            n_col = subplot_grid[1]

            if fig_size is None:
                size = calc_fig_size(subplots= (n_row, n_col) )
            else:
                size = fig_size
            fig, ax = plt.subplots(n_row, n_col, figsize=size)

            if col_sort:
                ax = ax.T

            ax = ax.flatten()

        else:
            if n_subplots == 1:
                n_row = 1
                n_col = 1
                if fig_size is None:
                    size = calc_fig_size(subplots= (n_row, n_col) )
                else:
                    size = fig_size
                fig, ax = plt.subplots(n_row, n_col, figsize=size)

                ax = np.array([ax])

            elif n_subplots == 2:
                n_row = 1
                n_col = 2
                if fig_size is None:
                    size = calc_fig_size(subplots= (n_row, n_col) )
                else:
                    size = fig_size
                fig, ax = plt.subplots(n_row, n_col, figsize=size)

                if col_sort:
                    ax = ax.T
                ax = ax.flatten()

            elif n_subplots == 3:
                n_row = 1
                n_col = 3
                if fig_size is None:
                    size = calc_fig_size(subplots= (n_row, n_col) )
                else:
                    size = fig_size
                fig, ax = plt.subplots(n_row, n_col, figsize=size)

                if col_sort:
                    ax = ax.T

                ax = ax.flatten()

            elif (n_subplots > 4) & (n_subplots < 7):
                n_row = 2
                n_col = 3
                if fig_size is None:
                    size = calc_fig_size(subplots= (n_row, n_col) )
                else:
                    size = fig_size
                fig, ax = plt.subplots(n_row, n_col, figsize=size)

                if col_sort:
                    ax = ax.T

                ax = ax.flatten()

            else:
                n_col = int(np.ceil(np.sqrt(n_subplots)))
                n_row = n_col
                if fig_size is None:
                    size = calc_fig_size(subplots= (n_row, n_col) )
                else:
                    size = fig_size
                fig, ax = plt.subplots(n_row, n_col, figsize=size)

                if col_sort:
                    ax = ax.T

                ax = ax.flatten()

        return fig, ax

def calc_fig_size(subplots=(1, 1), width_pt = 450):

        # Convert from pt to inches
        inches_per_pt = 1 / 72.27

        # Golden ratio to set aesthetic figure height
        # https://disq.us/p/2940ij3
        golden_ratio = (5**.5 - 1) / 2

        # Figure width in inches
        fig_width_in = width_pt * inches_per_pt
        # Figure height in inches
        fig_height_in = fig_width_in * golden_ratio

        return (fig_width_in * subplots[1], fig_height_in * subplots[0])

def get_multcolumn_subplot(n_regular_plots, n_multi_colm, regular_plot_grid = None, fig_size = None):

    if regular_plot_grid is None:
        if n_regular_plots <= 2:
            n_row = 1
            n_col = 2
            idx_comb = get_all_comb(np.arange(0,2,dtype=int), np.arange(0,1,dtype = int))
        elif n_regular_plots <= 4:
            n_row = 2
            n_col = 2
            idx_comb = get_all_comb(np.arange(0,2,dtype=int), np.arange(0,2,dtype = int))
        elif n_regular_plots <= 6:
            n_row = 2
            n_col = 3
            idx_comb = get_all_comb(np.arange(0,3,dtype=int), np.arange(0,2,dtype = int))
        elif n_regular_plots <= 9:
            n_row = 3
            n_col = 3
            idx_comb = get_all_comb(np.arange(0,3,dtype=int), np.arange(0,3,dtype = int))
        elif n_regular_plots <= 16:
            n_row = 4
            n_col = 4
            idx_comb = get_all_comb(np.arange(0,4,dtype=int), np.arange(0,4,dtype = int))
    elif isinstance(regular_plot_grid, list):
        n_row = regular_plot_grid[0]
        n_col = regular_plot_grid[1]
        idx_comb = get_all_comb(np.arange(0,n_col,dtype=int), np.arange(0,n_row,dtype = int))
    
    n_row_total = n_row + n_multi_colm
    if fig_size is None:
        fig_size = calc_fig_size(subplots=(n_row_total, n_col))
    fig = plt.figure(figsize=fig_size)
    gs = fig.add_gridspec(n_row_total, n_col)

    ax = np.array([])

    for i in range(n_regular_plots):
        ax = np.append(ax, fig.add_subplot(gs[int(idx_comb[i,1]), int(idx_comb[i,0])]))

    idx_row = n_row
    for i in range(n_multi_colm):
        ax = np.append(ax, fig.add_subplot(gs[idx_row, :]))
        idx_row = idx_row + 1

    return fig, ax

def get_all_comb(*vector):

    n_factorial = 1
    for sample in vector:
        n_factorial = n_factorial * len(sample)
    
    nodes = np.zeros((n_factorial, len(vector)))

    meshgrid_mat = np.meshgrid(*vector)

    for idx, parameter in enumerate(meshgrid_mat):
        nodes[:,idx] = parameter.flatten()

    return nodes

def create_plots(data, sample = 0, **plt_kwargs):
    
    plt = []

    if isinstance(sample, int):
        sample = [sample]

    # Check domain 
    if data.domain.n_dim == 1:
        for sample_id in sample:
            sample_plt = LinePlot(data.domain.nodes[:,0], data.values[:,sample_id], **plt_kwargs)
            sample_plt.y_label = data.label
            plt.append(sample_plt)

    if data.domain.n_dim == 2:
        for sample_id in sample:
            sample_plt = ContourPlot(data.domain, data.values[:,sample_id], **plt_kwargs)
            sample_plt.cbar = True
            sample_plt.cbar_label = data.label
            plt.append(sample_plt)

    return plt

def create_scalar_para_plots(input, output, sample = 0, **plt_kwargs):   
    
    plt = []

    if isinstance(sample, int):
        sample = [sample]

    # Check domain 
    if output.domain.n_dim == 1:
        for sample_id in sample:
            label = ""
            for i in range(input.n_dim):
                if i == input.n_dim - 1:
                    label = label + f"{input.labels[i]} = {input.nodes[sample_id,i]:.2f}"
                else:
                    label = label + f"{input.labels[i]} = {input.nodes[sample_id,i]:.2f}; "
            
            sample_plt = LinePlot(output.domain.nodes[:,0], output.values[:,sample_id], label = label,**plt_kwargs)
            sample_plt.y_label = output.label
            plt.append(sample_plt)

    elif output.domain.n_dim == 2:
        for sample_id in sample:
            label = ""
            for i in range(input.n_dim):
                label = label + f"{input.label[i]} = {input.nodes[sample_id,i]}; "

            sample_plt = ContourPlot(output.domain, output.values[:,sample_id], **plt_kwargs)
            sample_plt.cbar = True
            sample_plt.cbar_label = output.label
            sample_plt.title = label
            plt.append(sample_plt)

    return plt