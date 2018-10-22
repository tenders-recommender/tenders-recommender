import json
import os
import random

import numpy as np
from surprise import KNNBasic

from recommender_surprise.service import AlgoTrainer

SAVED_FOLDER_PATH = 'saved'


def main():
    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    k_range = [45]
    min_k_range = [3]
    name_range = ['cosine', 'msd', 'pearson', 'pearson_baseline']
    min_support_range = [1, 2, 3]

    for k in k_range:
        for min_k in min_k_range:
            for name in name_range:
                for min_support in min_support_range:
                    sim_options = {
                        'name': name,
                        'min_support': min_support,
                        'user_based': True
                    }

                    knn = KNNBasic(k=k, min_k=min_k, sim_options=sim_options)

                    print("TESTING PARAMS: " + str(k) + ", " + str(min_k) + ", " + str(sim_options))
                    try:
                        r = AlgoTrainer(algorithm=knn, parsed_data_file_path=create_file_path('parsed_data.bin'))

                        add_rmse_to_file(r.calculate_rmse(),
                                         create_file_path('rmse_params.json'),
                                         alg_name=KNNBasic.__name__,
                                         time_elapsed=r.get_time_elapsed(),
                                         k=k,
                                         min_k=min_k,
                                         sim_options=sim_options)
                    except Exception as e:
                        print(e)
                    print("")


def create_file_path(file_name):
    return os.path.join(SAVED_FOLDER_PATH, file_name) \
        if file_name is not None \
        else None


def add_rmse_to_file(rmse: float,
                     file_path: str,
                     alg_name: str = None,
                     time_elapsed: float = None,
                     k: float = None,
                     min_k: float = None,
                     sim_options=None):
    entry = {'rmse': rmse}
    if alg_name is not None:
        entry['algorithm'] = alg_name
    if time_elapsed is not None:
        entry['time_elapsed'] = time_elapsed
    if k is not None:
        entry['k'] = k
    if min_k is not None:
        entry['min_k'] = min_k
    if sim_options is not None:
        entry['sim_options'] = sim_options

    entries = []
    if os.path.isfile(file_path):
        with open(file_path, 'r') as rmse_file:
            entries: list = json.load(rmse_file)

    entries.append(entry)

    with open(file_path, 'w') as rmse_file:
        json.dump(entries, rmse_file)


if __name__ == '__main__':
    main()
