import numpy as np
from scipy import interpolate

class Grid:
    def __init__(self, *dimension_samples, labels = ["x", "y", "z"]):

        self.dimension_samples = dimension_samples
        self.labels = labels

        self.n_dim = len(dimension_samples)
        self.n_nodes_per_dim = []
        self.min_per_dim = np.array([])
        self.max_per_dim = np.array([])
        self.l_per_dim = np.array([])
        self.dx_per_dim = np.array([])

        for sample in dimension_samples:
            self.n_nodes_per_dim.append(len(sample))
            self.min_per_dim = np.append(self.min_per_dim, np.min(sample))
            self.max_per_dim = np.append(self.max_per_dim, np.max(sample))
            self.l_per_dim = np.append(self.l_per_dim, np.max(sample) - np.min(sample))
            if sample.size > 1:
                self.dx_per_dim = np.append(self.dx_per_dim, sample[1] - sample[0])


        self.nodes, self.meshgrid_mat = self.full_factorial_grid()
        self.size = self.nodes.shape[0]

    @classmethod
    def create_2D_grid_from_coord(cls,x,y):
        x_min = np.min(x)
        x_max = np.max(x)
        y_min = np.min(y)
        y_max = np.max(y)

        flag_x_nodes_greater_0 = x > 1e-15
        flag_y_nodes_greater_0 = y > 1e-15
        delta_x = np.min(x[flag_x_nodes_greater_0])
        delta_y = np.min(y[flag_y_nodes_greater_0])

        n_elem_x = int(x_max / delta_x)
        n_elem_y = int(y_max / delta_y)

        x_discretization = np.linspace(x_min, x_max, n_elem_x + 1)
        y_discretization = np.linspace(y_min, y_max, n_elem_y + 1)
        grid = cls(x_discretization,y_discretization)

        return grid

    def full_factorial_grid(self):

        n_factorial = 1
        for sample in self.dimension_samples:
            n_factorial = n_factorial * len(sample)

        nodes = np.zeros((n_factorial, self.n_dim))
        meshgrid_mat = np.meshgrid(*self.dimension_samples)

        for idx, parameter in enumerate(meshgrid_mat):
            nodes[:,idx] = parameter.flatten()

        return nodes, meshgrid_mat

    def reshape_data(self, fun_evals):
        
        if self.n_dim == 1:
            fun_evals_grid = fun_evals

        elif self.n_dim == 2:
            fun_evals_grid = fun_evals.reshape(self.n_nodes_per_dim[1], self.n_nodes_per_dim[0])

        return fun_evals_grid

    def create_interpolator(self, fun_evals):

        interpolator = []

        if self.n_dim == 1:
            interpolator = interpolate.interp1d(self.nodes[:,0], fun_evals, axis = 0)
        elif self.n_dim == 2:
            zz = self.reshape_data(fun_evals = fun_evals)
            interpolator = interpolate.RectBivariateSpline(self.dimension_samples[0], self.dimension_samples[1], zz.T)

        return interpolator
    
    def create_legend(self, dim = 0):

        legendText = []

        for i in range(self.n_nodes_per_dim[dim]):
            legendText.append(f'{self.labels[dim]} = {self.dimension_samples[dim][i] :.2}')

        return legendText

    def sample_picker(self, *condition):
        
        a = []

        return a
    
    def get_euclid_distance(self, node_ids, l_max):
        
        distance_mat = np.ones((self.size, len(node_ids))) * 10000

        for idx, node_id in enumerate(node_ids):
            node_x = self.nodes[node_id, 0]
            node_y = self.nodes[node_id, 1]

            nodes_in_square = self.get_nodes_in_square(node_id, l_max)

            x_coords = self.nodes[nodes_in_square,0]
            y_coords = self.nodes[nodes_in_square,1]

            delta_x = x_coords - node_x
            delta_y = y_coords - node_y

            distance_mat[nodes_in_square,idx] = np.sqrt(np.square(delta_x) + np.square(delta_y))

        return distance_mat

    def get_nodes_in_square(self, node_id, l):
        
        n_nodes_x = l/self.dx_per_dim[0]
        n_idx_x = int(np.floor(n_nodes_x/2))

        n_nodes_y = l/self.dx_per_dim[1]
        n_idx_y = int(np.floor(n_nodes_y/2))

        node_ids = np.arange(0,self.size, dtype= int)

        node_ids_mat = self.reshape_data(node_ids)

        node_id_in_mat = np.argwhere(node_ids_mat == node_id)
        x_id = node_id_in_mat[0,0]
        y_id = node_id_in_mat[0,1]

        node_ids_in_square = node_ids_mat[x_id-n_idx_x : x_id+n_idx_x +1, y_id-n_idx_y : y_id+n_idx_y +1]

        node_ids_in_square = node_ids_in_square.flatten()

        return node_ids_in_square
    
class GridData:
    def __init__(self, grid, data, label = "f(x)"):
        self.domain = grid
        if data.ndim == 1:
            data = data.reshape(-1,1)
        self.values = data        # Data in flattened form
        self.n_samples = data.shape[1]
        self.label = label

    def get_shaped_data(self):
        'Returns data of shape n_samples x d_1 x d_2 x d_n'

        if self.domain.n_dim == 1:
            shaped_data = self.values.T

        elif self.domain.n_dim == 2:
            shaped_data = np.zeros((self.n_samples, self.domain.n_nodes_per_dim[0], self.domain.n_nodes_per_dim[1]))

            for idx, data_point in enumerate(self.values.T):
                shaped_data[idx,:,:] = self.domain.reshape_data(data_point)
        
        return shaped_data

