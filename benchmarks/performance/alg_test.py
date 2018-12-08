import random
from datetime import datetime
from typing import List, Dict

import numpy as np
from surprise import SVD, KNNBaseline, SlopeOne, BaselineOnly, CoClustering, NMF, KNNBasic, KNNWithMeans, Prediction

from benchmarks.test_util import load_sorted_test_interactions, add_results_to_database
from tenders_recommender.model import Interaction, ParsedData
from tenders_recommender.parser import Parser
from tenders_recommender.recommender import Recommender
from tenders_recommender.trainer import AlgoTrainer
from surprise.model_selection import KFold


def test() -> [Dict[str, object]]:
    alg_list = [SVD, KNNBaseline, SlopeOne, BaselineOnly, CoClustering, NMF, KNNBasic, KNNWithMeans]

    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    interactions: List[Interaction] = load_sorted_test_interactions()
    parsed_data: ParsedData = Parser.parse(interactions)
    kf = KFold(n_splits=3)
    entries = []

    for trainset, testset in kf.split(parsed_data.whole_data_set):
        for alg_to_test in alg_list:
            print("TESTING ALGORITHM: " + alg_to_test.__name__ + ", TIME: ")
            try:
                before = datetime.now()
                predictions: List[Prediction] = AlgoTrainer.calc_predictions(trainset,
                                                                             testset,
                                                                             alg_to_test())
                time_elapsed = (datetime.now() - before).total_seconds()

                recommender = Recommender(parsed_data.ids_offers_map, predictions)

                entry: Dict[str, object] = {'rmse': recommender.calc_rmse()}
                entry['algorithm'] = alg_to_test.__name__
                entry['time_elapsed'] = time_elapsed
                entries.append(entry)

            except Exception as e:
                print(e)
            print("")

    return entries


if __name__ == '__main__':
    results = test()
    add_results_to_database(results, "algorithm_comparison")
