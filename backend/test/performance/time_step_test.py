import random
from datetime import datetime, timedelta
from typing import List, Tuple, Callable

import dateutil
import numpy as np
from surprise import KNNBasic, SVD

from tenders_recommender.dto import Interaction
from tenders_recommender.parser import Parser
from tenders_recommender.recommender import Recommender
from tenders_recommender.trainer import AlgoTrainer
from test.test_util import load_sorted_test_interactions, add_rmse_to_file


def main():
    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    k = 45
    min_k = 1
    sim_options = {
        'name': 'pearson',
        'min_support': 1,
        'user_based': True
    }

    all_interactions = load_sorted_test_interactions()
    print('Amount of interactions: ' + str(len(all_interactions)))

    first_date = dateutil.parser.parse(all_interactions[0]['when'])
    last_date = dateutil.parser.parse(all_interactions[len(all_interactions) - 1]['when'])
    print('First date: ' + str(first_date))
    print('Last date: ' + str(last_date))
    delta = timedelta(days=7)

    earlier_than = first_date
    interactions_slice_index = 0

    while earlier_than <= last_date:
        earlier_than += delta

        interactions_slice_index = get_interactions_slice_index(all_interactions,
                                                                earlier_than,
                                                                interactions_slice_index)
        filtered_interactions = all_interactions[0:interactions_slice_index:1]

        parsed_data = Parser.parse(filtered_interactions)
        knn = KNNBasic(k=k, min_k=min_k, sim_options=sim_options)

        before = datetime.now()
        predictions = AlgoTrainer.calc_predictions(parsed_data.train_set,
                                                   parsed_data.test_set,
                                                   knn)
        time_elapsed = (datetime.now() - before).total_seconds()

        recommender = Recommender(parsed_data.ids_offers_map, predictions)

        rmse = recommender.calc_rmse()
        add_rmse_to_file(rmse,
                         'rmse_time_step.json',
                         ('earlier_than', earlier_than.timestamp()),
                         ('time_elapsed', time_elapsed),
                         ('interactions', len(filtered_interactions)))

        print(earlier_than.strftime("%Y-%m-%d") +
              ', rmse: ' + str(rmse) +
              ', interactions: ' + str(len(filtered_interactions)))


def get_interactions_slice_index(all_interactions: List[Interaction],
                                 earlier_than: datetime,
                                 previous_index=0) -> int:
    is_interaction_earlier_than: Callable[[Interaction], bool] = lambda inter: \
        dateutil.parser.parse(inter['when']) < earlier_than

    for index, interaction in enumerate(all_interactions):
        if index < previous_index:
            continue
        if not is_interaction_earlier_than(interaction):
            return index

    return len(all_interactions)


if __name__ == '__main__':
    main()
