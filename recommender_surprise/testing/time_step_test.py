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

    k = 10
    min_k = 3
    sim_options = {'name': 'cosine',
                   'min_support': 1,
                   'user_based': False
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
                    alg_name=KNNBasic.__name__,
                    rmse_file_name='Knn_rmse_summary.json')
        start_date += delta


if __name__ == '__main__':
    main()
