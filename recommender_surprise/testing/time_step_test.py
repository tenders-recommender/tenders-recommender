import random
from datetime import datetime, timedelta

import numpy as np
import pytz
from surprise import KNNBasic

from recommender_surprise.service import Recommender


def main():
    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    k = 20
    min_k = 3
    sim_options = {'name': 'pearson',
                   'min_support': 2,
                   'user_based': True
                   }
    knn = KNNBasic(k=k, min_k=min_k, sim_options=sim_options)

    utc = pytz.UTC
    start_date = datetime.strptime('30 Oct 2015', '%d %b %Y').replace(tzinfo=utc)
    end_date = datetime.strptime('20 Nov 2015', '%d %b %Y').replace(tzinfo=utc)

    delta = timedelta(days=7)
    while start_date <= end_date:
        print(start_date.strftime("%Y-%m-%d"))
        Recommender(earlier_than=start_date,
                    algorithm=knn,
                    parsed_data_file_path='rmse_summary.json')
        start_date += delta


if __name__ == '__main__':
    main()
