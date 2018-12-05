import random
from datetime import datetime

import numpy as np
from surprise import KNNBasic

from tenders_recommender.parser import Parser
from tenders_recommender.recommender import Recommender
from tenders_recommender.trainer import AlgoTrainer
from benchmarks.test_util import load_sorted_test_interactions, add_rmse_to_file


def main():
    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    k_range = [1, 10, 20, 45]
    min_k_range = [1, 2, 3]
    name_range = ['cosine', 'msd', 'pearson', 'pearson_baseline']
    min_support_range = [1, 2, 3]

    interactions = load_sorted_test_interactions()
    parsed_data = Parser.parse(interactions)

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
                        before = datetime.now()
                        predictions = AlgoTrainer.calc_predictions(parsed_data.train_set,
                                                                   parsed_data.test_set,
                                                                   knn)
                        time_elapsed = (datetime.now() - before).total_seconds()

                        recommender = Recommender(parsed_data.ids_offers_map, predictions)

                        add_rmse_to_file(recommender.calc_rmse(),
                                         'rmse_knn_params.json',
                                         ('alg_name', KNNBasic.__name__),
                                         ('time_elapsed', time_elapsed),
                                         ('k', k),
                                         ('min_k', min_k),
                                         ('sim_options', sim_options))
                    except Exception as e:
                        print(e)
                    print("")


if __name__ == '__main__':
    main()
