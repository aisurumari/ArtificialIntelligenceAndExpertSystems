import matplotlib.pyplot as plt

import csvImporter
import numpy as np


def create_plot(data, alg):

    #All the stats that we care about
    stats = [ 
        csvImporter.SOLUTION_LENGTH, 
        csvImporter.SOLUTION_LENGTH,
        csvImporter.SEEN_NODES,
        csvImporter.PROCESSED_NODES,
        csvImporter.MAX_RECURSION_DEPTH,
        csvImporter.DURATION 
    ]

    #Stat to title of plot
    stats_to_title = {
        csvImporter.SOLUTION_LENGTH: "Średnia długość rozwiązania \n" + alg,
        csvImporter.PROCESSED_NODES:  "Średnia liczba przetworzonych stanów \n" + alg,
        csvImporter.SEEN_NODES: "Średnia liczba stanów odwiedzonych \n" + alg,
        csvImporter.MAX_RECURSION_DEPTH: "Średnia maksymalna głębokość rekursji \n" + alg,
        csvImporter.DURATION: "Średni czas wykononania \n" + alg
    }

    #Stat to the label of y plot
    stats_to_ylabel = {
        csvImporter.SOLUTION_LENGTH: "Długość rozwiązania",
        csvImporter.PROCESSED_NODES:   "Liczba przetworzonych stanów",
        csvImporter.SEEN_NODES: "Liczba stanów odwiedzonych",
        csvImporter.MAX_RECURSION_DEPTH:  "Głębokość rekursji",
        csvImporter.DURATION: "Czas wykononania [ms]"
    }

    #Prepare plot for each stat
    for stat in stats: 

        #Create new figure
        fig, ax = plt.subplots()
        labels_names = ["1","2","3","4","5","6","7"] #prepare labels
        x_loc = np.arange(len(labels_names)) # the label locations
        width = 0.1 # the width of the bars
        
        #Get all strategies for given algorith. For astr that would be ["manh", "hamm"]
        strategies =  data[0].keys()
        # Prepare location for bars
        rects_offsets = np.arange(len(strategies))
        middle_point = len(strategies) // 2
        rects_offsets = [(offset - middle_point)/10 for offset in rects_offsets]
        
        #prepare arrays with values for each strategy
        data_to_plot = {} # strategy -> values for each distance
        for strategy in strategies: 
            if strategy not in data_to_plot:
                data_to_plot[strategy] = []
            for i in range(7):
                data_to_plot[strategy].append(data[i][strategy][stat])

        #Draw bars
        for offset, strategy in zip(rects_offsets, strategies):
            rect = ax.bar(x_loc + offset, data_to_plot[strategy], width, label=strategy)   


        ax.set_ylabel(stats_to_ylabel[stat])
        ax.set_title(stats_to_title[stat])
        ax.set_xticks(x_loc, labels=labels_names)
        ax.legend()
        fig.tight_layout()
        plt.savefig(f"plots/{alg}_{stat}")

def create_plot_merged(bfs_data, dfs_data, astr_data): 
    stats = [ csvImporter.SOLUTION_LENGTH, 
    csvImporter.SOLUTION_LENGTH,
    csvImporter.SEEN_NODES,
    csvImporter.PROCESSED_NODES,
    csvImporter.MAX_RECURSION_DEPTH,
    csvImporter.DURATION ]

    stats_to_title = {
        csvImporter.SOLUTION_LENGTH: "Średnia długość rozwiązania \n",
        csvImporter.PROCESSED_NODES:  "Średnia liczba przetworzonych stanów \n",
        csvImporter.SEEN_NODES: "Średnia liczba stanów odwiedzonych \n",
        csvImporter.MAX_RECURSION_DEPTH: "Średnia maksymalna głębokość rekursji \n",
        csvImporter.DURATION: "Średni czas wykononania \n"
    }

    stats_to_ylabel = {
        csvImporter.SOLUTION_LENGTH: "Długość rozwiązania",
        csvImporter.PROCESSED_NODES:   "Liczba przetworzonych stanów",
        csvImporter.SEEN_NODES: "Liczba stanów odwiedzonych",
        csvImporter.MAX_RECURSION_DEPTH:  "Głębokość rekursji",
        csvImporter.DURATION: "Czas wykononania"
    }

    alg_names = ['bfs', 'dfs', 'astr']

    for stat in stats: 
        #prepare arrays with values for each strategy
        data_to_plot = {} #algorithm -> values for each distance
        data_to_plot['bfs'] = []
        data_to_plot['dfs'] = []
        data_to_plot['astr'] = []
   
        bfs_strategies = bfs_data[0].keys()
        for length in range(7):
            count = 0
            total = 0
            for strategy in bfs_strategies:
                total +=  bfs_data[length][strategy][stat]
                count += 1
            data_to_plot['bfs'].append(total/count)

        dfs_strategies = dfs_data[0].keys()
        for length in range(7):
            count = 0
            total = 0
            for strategy in dfs_strategies:
                total +=  dfs_data[length][strategy][stat]
                count += 1
            data_to_plot['dfs'].append(total/count)

        astr_strategies = astr_data[0].keys()
        for length in range(7):
            count = 0
            total = 0
            for strategy in astr_strategies:
                total +=  astr_data[length][strategy][stat]
                count += 1
            data_to_plot['astr'].append(total/count)

        fig, ax = plt.subplots()
        labels = ["1","2","3","4","5","6","7"] #prepare labels
        x_loc = np.arange(len(labels)) # the label locations
        width = 0.1 # the width of the bars
        
        # Prepare location for bars
        rects_offsets = np.arange(len(alg_names))
        middle_point = len(alg_names) // 2
        rects_offsets = [(offset - middle_point)/10 for offset in rects_offsets]

        for offset, alg_name in zip(rects_offsets, alg_names):
            rect = ax.bar(x_loc + offset, data_to_plot[alg_name], width, label=alg_name)   

        ax.set_ylabel(stats_to_ylabel[stat])
        ax.set_title(stats_to_title[stat])
        #ax.set_xticks(x_loc, Labels=labels)
        ax.legend()
        fig.tight_layout()
        plt.savefig(f"plots/merged_{stat}")



bfs_data = csvImporter.prepare_data_for_plot("puzzles", "bfs")
dfs_data = csvImporter.prepare_data_for_plot("puzzles", "dfs")
astr_data = csvImporter.prepare_data_for_plot("puzzles", "astr")
create_plot(bfs_data, "BFS")
create_plot(dfs_data, "DFS")
create_plot(astr_data, "ASTR")
create_plot_merged(bfs_data, dfs_data, astr_data)