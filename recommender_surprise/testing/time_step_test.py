import json
import os
import random
from datetime import datetime, timedelta
from itertools import chain
from typing import List, Tuple, Iterator

import dateutil
import numpy as np
import pytz
from surprise import KNNBasic

from recommender_surprise.dto import Interaction
from recommender_surprise.service import AlgoTrainer


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

    utc = pytz.UTC
    start_date, end_date = parse_date_range()

    delta = timedelta(days=7)
    while start_date <= end_date:
        print(start_date.strftime("%Y-%m-%d"))
        AlgoTrainer(earlier_than=start_date,
                    algorithm=knn,
                    parsed_data_file_path='rmse_summary.json')
        start_date += delta


def parse_date_range(verbose: bool = True) -> Tuple[datetime, datetime]:
    tracker_file_folder: str = os.path.join('..', '..', 'tracker')
    interactions_file_names: List[str] = [
        'observed-offers.json',
        'reported-offers.json',
        'viewed-offers.json'
    ]

    file_paths: Tuple[str, ...] = tuple(os.path.join(tracker_file_folder, file_name)
                                        for file_name in interactions_file_names)
    interactions_chain: Iterator[Interaction] = chain.from_iterable(
        [json.load(open(file_path)) for file_path in file_paths])

    interactions_dates: List[datetime] = sorted(map(lambda interaction: dateutil.parser.parse(interaction['when']),
                                                    interactions_chain))

    first_date: datetime = interactions_dates[0]
    last_date: datetime = interactions_dates[len(interactions_dates) - 1]

    if verbose:
        print('First date: ' + str(first_date))
        print('Last date: ' + str(last_date))

    return first_date, last_date


if __name__ == '__main__':
    main()
