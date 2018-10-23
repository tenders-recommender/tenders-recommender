import random
from datetime import datetime
from typing import List

import numpy as np
from surprise import SVD, KNNBaseline, SlopeOne, BaselineOnly, CoClustering, NMF, KNNBasic, KNNWithMeans, Prediction

from tenders_recommender.dto import Interaction, ParsedData
from tenders_recommender.parser import Parser
from tenders_recommender.recommender import Recommender
from tenders_recommender.trainer import AlgoTrainer
from test.test_util import load_sorted_test_interactions, add_rmse_to_file


def main():
    alg_list = [SVD, KNNBaseline, SlopeOne, BaselineOnly, CoClustering, NMF, KNNBasic, KNNWithMeans]

    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    interactions: List[Interaction] = load_sorted_test_interactions()
    parsed_data: ParsedData = Parser.parse(interactions)

    for test_number in range(1, 4):
        for alg_to_test in alg_list:
            print("TESTING ALGORITHM: " + alg_to_test.__name__ + ", TIME: " + str(test_number))
            try:
                before = datetime.now()
                predictions: List[Prediction] = AlgoTrainer.calc_predictions(parsed_data.train_set,
                                                                             parsed_data.test_set,
                                                                             alg_to_test())
                time_elapsed = (datetime.now() - before).total_seconds()

                recommender = Recommender(parsed_data.ids_offers_map, predictions)

                add_rmse_to_file(recommender.calc_rmse(),
                                 'rmse_alg.json',
                                 ('alg_name', alg_to_test.__name__),
                                 ('time_elapsed', time_elapsed))
            except Exception as e:
                print(e)
            print("")


if __name__ == '__main__':
    main()
