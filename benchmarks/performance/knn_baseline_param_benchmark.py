from surprise import KNNBaseline
import random
from typing import Dict, List

import numpy as np
from surprise.dataset import DatasetAutoFolds
from surprise.model_selection import GridSearchCV, KFold

from tenders_recommender.parser import Parser
from benchmarks.test_util import load_sorted_test_interactions
from benchmarks.test_util.util import NumpyEncoder, add_results_to_database


def prepare_data() -> DatasetAutoFolds:
    interactions = load_sorted_test_interactions()
    parsed_data = Parser.parse(interactions)
    return parsed_data.whole_data_set


def prepare_param_grid_als() -> Dict[str, List[object]]:
    param_grid_als: Dict[str, List[object]] = {'bsl_options': {'method': ['als'],
                                                               'reg_u': [8, 14],
                                                               'reg_i': [2, 5],
                                                               'n_epochs': [5, 8]
                                                               },
                                               'min_k': [1, 2],
                                               'k': [2, 20],
                                               'sim_options': {'name': ['cosine', 'msd', 'pearson', 'pearson_baseline'],
                                                               'min_support': [1, 3],
                                                               'user_based': [True]}
                                               }
    return param_grid_als


def prepare_param_grid_sgd() -> Dict[str, List[object]]:
    param_grid_sgd: Dict[str, List[object]] = {'bsl_options': {'method': ['sgd'],
                                                               'learning_rate': [0.001, 0.01],
                                                               'reg': [1, 2],
                                                               'n_epochs': [5, 8]
                                                               },
                                               'min_k': [1, 2],
                                               'k': [2, 20],
                                               'sim_options': {'name': ['cosine', 'msd', 'pearson', 'pearson_baseline'],
                                                               'min_support': [1, 3],
                                                               'user_based': [True]}
                                               }
    return param_grid_sgd


def test(data_set: DatasetAutoFolds, param_grid, type: str) -> None:
    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    grid_search = GridSearchCV(
        algo_class=KNNBaseline,
        param_grid=param_grid,
        measures=['rmse'],
        cv=KFold(4),
        n_jobs=-1
    )

    grid_search.fit(data_set)
    print(type)
    print(grid_search.best_score['rmse'])
    print(grid_search.best_params['rmse'])
    print(grid_search.cv_results)

    add_results_to_database(grid_search.cv_results, type, cls=NumpyEncoder)


if __name__ == '__main__':
    data_set = prepare_data()
    test(data_set, prepare_param_grid_als(), "knn_baseline_als")
    test(data_set, prepare_param_grid_sgd(), "knn_baseline_sgd")
