import json
import os
import random

import numpy as np
from surprise import SVD, KNNBaseline, SlopeOne, BaselineOnly, CoClustering, NMF, KNNBasic, KNNWithMeans

from recommender_surprise.service import Recommender

SAVED_FOLDER_PATH = 'saved'


def main():
    alg_list = [SVD, KNNBaseline, SlopeOne, BaselineOnly, CoClustering, NMF, KNNBasic, KNNWithMeans]

    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    for test_number in range(1, 4):
        for alg_to_test in alg_list:
            print("TESTING ALGORITHM: " + alg_to_test.__name__ + ", TIME: " + str(test_number))
            try:
                r = Recommender(algorithm=alg_to_test(), parsed_data_file_path=create_file_path('parsed_data.bin'))

                add_rmse_to_file(r.calculate_rmse(),
                                 create_file_path('rmse_alg.json'),
                                 alg_name=alg_to_test.__name__,
                                 time_elapsed=r.get_time_elapsed())
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
                     time_elapsed: float = None):
    entry = {'rmse': rmse}
    if alg_name is not None:
        entry['algorithm'] = alg_name
    if time_elapsed is not None:
        entry['time_elapsed'] = time_elapsed

    entries = []
    if os.path.isfile(file_path):
        with open(file_path, 'r') as rmse_file:
            entries: list = json.load(rmse_file)

    entries.append(entry)

    with open(file_path, 'w') as rmse_file:
        json.dump(entries, rmse_file)


if __name__ == '__main__':
    main()
