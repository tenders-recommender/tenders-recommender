from recommender_surprise.recommender import Recommender

import random
import numpy as np
from surprise import SVD, KNNBaseline, SlopeOne, BaselineOnly, CoClustering, NMF, KNNBasic, KNNWithMeans


def main():
    alg_list = [SVD, KNNBaseline, SlopeOne, BaselineOnly, CoClustering, NMF, KNNBasic, KNNWithMeans]

    seed = 0
    random.seed(seed)
    np.random.seed(seed)

    for test_number in range(1, 4):
        for alg_to_test in alg_list:
            print("TESTING ALGORITHM: " + alg_to_test.__name__ + ", TIME: " + str(test_number))
            try:
                Recommender(algorithm=alg_to_test(),
                            alg_name=alg_to_test.__name__,
                            rmse_file_name='rmse_alg.json',
                            parsed_data_file_name='parsed_data.bin')
            except Exception as e:
                print(e)
            print("")


if __name__ == '__main__':
    main()
