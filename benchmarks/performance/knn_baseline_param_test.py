from surprise import KNNBaseline
import random
from typing import Dict, List

import numpy as np
from surprise.model_selection import GridSearchCV, KFold

from tenders_recommender.parser import Parser
from benchmarks.test_util import load_sorted_test_interactions
from benchmarks.test_util.util import NumpyEncoder, add_results_to_database


def test():
    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    param_grid_als: Dict[str, List[object]] = {'bsl_options': {'method': 'als',
                                                               'reg_u': [8, 10, 12, 14],
                                                               'reg_i': [2, 3, 4, 5],
                                                               'n_epochs': [5, 6, 7, 8]
                                                               },
                                               'min_k': [1, 2, 3],
                                               'k': [1, 10, 20, 45],

                                               'sim_options': {'name': ['cosine', 'msd', 'pearson', 'pearson_baseline'],
                                                               'min_support': [1, 2, 3],
                                                               'user_based': [True]}
                                               }

    param_grid_sgd: Dict[str, List[object]] = {'bsl_options': {'method': ['als', 'sgd'],
                                                               'learning_rate': [0.001, 0.005, 0.01],
                                                               'reg': [1, 2],
                                                               'n_epochs': [5, 6, 7, 8]
                                                               },
                                               'min_k': [1, 2, 3],
                                               'k': [1, 10, 20, 45],
                                               'learning_rate': [0.001, 0.005, 0.01],
                                               'sim_options': {'name': ['cosine', 'msd', 'pearson', 'pearson_baseline'],
                                                               'min_support': [1, 2, 3],
                                                               'user_based': [True]}
                                               }

    grid_search_als = GridSearchCV(
        algo_class=KNNBaseline,
        param_grid=param_grid_als,
        measures=['rmse'],
        cv=KFold(5),
        n_jobs=-1
    )

    interactions = load_sorted_test_interactions()
    parsed_data = Parser.parse(interactions)
    grid_search_als.fit(parsed_data.whole_data_set)

    print("KNNBaseline ALS:")
    print(grid_search_als.best_score['rmse'])
    print(grid_search_als.best_params['rmse'])
    print(grid_search_als.cv_results)

    add_results_to_database(grid_search_als.cv_results, "knnbaseline_als", cls=NumpyEncoder)

    grid_search_sgd = GridSearchCV(
        algo_class=KNNBaseline,
        param_grid=param_grid_sgd,
        measures=['rmse'],
        cv=KFold(5),
        n_jobs=-1
    )

    grid_search_sgd.fit(parsed_data.whole_data_set)
    print("KNNBaseline SGD:")
    print(grid_search_sgd.best_score['rmse'])
    print(grid_search_sgd.best_params['rmse'])
    print(grid_search_sgd.cv_results)

    add_results_to_database(grid_search_als.cv_results, "knnbaseline_sgd", cls=NumpyEncoder)


if __name__ == '__main__':
    test()
