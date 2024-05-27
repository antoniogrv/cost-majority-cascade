import algorithms.cost_seeds_greedy
import algorithms.wtss
import helpers.submodular_functions as sf

from default_config import Algorithms

class SpreadingAlgorithm():
    def __init__(self, selected_algorithm_index, selected_submodular_function_index, graph, threshold, cost_function, verbose):
        self.selected_algorithm_index = selected_algorithm_index
        self.selected_submodular_function_index = selected_submodular_function_index

        self.verbose = verbose

        self.G = graph
        self.threshold = threshold
        self.cost_function = cost_function
        self.submodular_function = self.setup_submodular_function()


    def setup_submodular_function(self):
        if self.selected_submodular_function_index == 1:
            submodular_function = sf.first
        elif self.selected_submodular_function_index == 2:
            submodular_function = sf.second
        elif self.selected_submodular_function_index == 3:
            submodular_function = sf.third
        else:
            submodular_function = None

        return submodular_function


    def get_seed_set(self):
        if self.selected_algorithm_index == Algorithms.COST_SEEDS_GREEDY.value:
            seed_set = algorithms.cost_seeds_greedy.cost_seeds_greedy(
                graph = self.G,
                threshold = self.threshold,
                cost_function = self.cost_function, 
                submodular_function = self.submodular_function, 
                verbose = self.verbose
            )
        elif self.selected_algorithm_index == Algorithms.WTSS.value:
            seed_set = algorithms.wtss.WTSS(
                G = self.G,
                k = self.threshold,
                cost_function = self.cost_function
            )
        
        return seed_set
