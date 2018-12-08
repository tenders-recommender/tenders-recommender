import json
import random
from typing import Dict, List

import numpy as np
from surprise import SVD
from surprise.model_selection import GridSearchCV, KFold

from tenders_recommender.parser import Parser
from benchmarks.test_util import load_sorted_test_interactions
from benchmarks.test_util.util import create_file_path, NumpyEncoder, add_results_to_database


def test():
    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    param_grid: Dict[str, List[object]] = {
        'n_factors': [50, 100, 200],
        'n_epochs': [10, 20, 50],
        'biased': [True, False],
        'init_mean': [0, 0.1, 0.5],
        'init_std_dev': [0, 0.1, 0.5],
        'lr_all': [0.001, 0.005, 0.01],
        'reg_all': [0.01, 0.02, 0.05],
        'random_state': [None],
        'verbose': [True]
    }

    grid_search = GridSearchCV(
        algo_class=SVD,
        param_grid=param_grid,
        measures=['rmse'],
        cv=KFold(5),
        n_jobs=-1
    )

    interactions = load_sorted_test_interactions()
    parsed_data = Parser.parse(interactions)
    grid_search.fit(parsed_data.whole_data_set)

    print(grid_search.best_score['rmse'])
    print(grid_search.best_params['rmse'])
    print(grid_search.cv_results)

    add_results_to_database(grid_search.cv_results, "svd", cls=NumpyEncoder)


if __name__ == '__main__':
    test()
