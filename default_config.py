from enum import Enum

# Configurazioni di default, sovrascrivibili tramite CLI

DEFAULT_THRESHOLD = 160

DEFAULT_EDGES = 'networks/sample_networks/348.edges'
DEFAULT_CIRCLES = 'networks/sample_networks/348.circles'

DEFAULT_RANGE_MIN = 1
DEFAULT_RANGE_MAX = 10

DEFAULT_COST_FUNCTION = 1
DEFAULT_SUBMODULAR_FUNCTION = 1
DEFAULT_ALGORITHM = 1

DEFAULT_RESULTS_PATH = "results"

class Algorithms(Enum):
    COST_SEEDS_GREEDY = 1
    WTSS = 2
    MY_SEEDS = 3