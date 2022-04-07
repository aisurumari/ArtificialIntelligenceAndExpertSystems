import numpy as np
import os

SOLUTION_LENGTH = 'slength'
SEEN_NODES = 'snodes'
PROCESSED_NODES = 'pnodes'
MAX_RECURSION_DEPTH = 'mrd'
DURATION = 'dur'

def import_data_from_csv(path):
    size_info = dict()
    data = np.genfromtxt(path, delimiter=' ', max_rows=1, dtype=int)
    size_info['rows'] = data[0]
    size_info['cols'] = data[1]
    result = np.genfromtxt(path, delimiter=' ', skip_header=1, dtype=int)
    return size_info, result


def import_result_data_from_csv(path):
    data = np.genfromtxt(path, delimiter='\n', dtype=float)
    return data


def prepare_data_for_plot(directory, algorithm):

    #for each expected length there is a dicionary with 
    # mapping from strategy to relevant statistics
    results = [{}, {}, {}, {}, {}, {}, {}]
    for filename in os.listdir(directory):
        parts = filename.split('_')

        if parts[-1] == "stats.txt" and parts[3] == algorithm:
            length = int(parts[1]) - 1
            strategy = parts[4]
            if strategy not in results[length]:
                results[length][strategy] = {
                    SOLUTION_LENGTH: [],
                    SEEN_NODES: [],
                    PROCESSED_NODES: [],
                    MAX_RECURSION_DEPTH: [],
                    DURATION: []
                }
            input_directory = os.path.join(directory, filename) 
            data = import_result_data_from_csv(input_directory)
            results[length][strategy][SOLUTION_LENGTH].append(data[0])
            results[length][strategy][PROCESSED_NODES].append(data[1])
            results[length][strategy][SEEN_NODES].append(data[2])
            results[length][strategy][MAX_RECURSION_DEPTH].append(data[3])
            results[length][strategy][DURATION].append(data[4])

    for len_exp, results_per_length in enumerate(results):
        for strat, results_per_strat in results_per_length.items():
            stats_name = results_per_strat.keys()
            for stat in stats_name:
                avg = sum(results_per_strat[stat]) / len(results_per_strat[stat])
                results_per_strat[stat] = avg

    return results
