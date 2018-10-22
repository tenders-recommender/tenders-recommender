import random
from datetime import datetime, timedelta
from typing import List, Tuple

import dateutil
import numpy as np
from surprise import KNNBasic

from dto import Interaction
from parser import Parser
from recommender import Recommender
from test_util import load_test_interactions, add_rmse_to_file
from trainer import AlgoTrainer


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

    knn = KNNBasic(k=k, min_k=min_k, sim_options=sim_options)

    interactions = load_test_interactions()

    earlier_than, last_date = parse_date_range(interactions)
    delta = timedelta(days=7)

    while earlier_than <= last_date:
        parsed_data = Parser.parse(interactions, earlier_than=earlier_than)

        before = datetime.now()
        predictions = AlgoTrainer.calc_predictions(parsed_data.train_set,
                                                   parsed_data.test_set,
                                                   knn)
        time_elapsed = (datetime.now() - before).total_seconds()

        recommender = Recommender(parsed_data.ids_offers_map, predictions)

        rmse = recommender.calc_rmse()
        add_rmse_to_file(rmse,
                         'rmse_time_step.json',
                         ('earlier_than', earlier_than),
                         ('time_elapsed', time_elapsed))

        print(earlier_than.strftime("%Y-%m-%d") + ' ' + str(rmse))
        earlier_than += delta


def parse_date_range(interactions: List[Interaction], verbose: bool = True) -> Tuple[datetime, datetime]:
    interactions_dates: List[datetime] = sorted(map(lambda interaction: dateutil.parser.parse(interaction['when']),
                                                    interactions))
    first_date: datetime = interactions_dates[0]
    last_date: datetime = interactions_dates[len(interactions_dates) - 1]

    if verbose:
        print('First date: ' + str(first_date))
        print('Last date: ' + str(last_date))

    return first_date, last_date


if __name__ == '__main__':
    main()
