from recommender_surprise.parser import Parser
from recommender_surprise.recommendation import Recommendation

import json
import os
import datetime
from bidict import bidict

from surprise import AlgoBase
from surprise import SVD
from surprise import accuracy
from surprise import dump


class Recommender(object):
    __SAVED_FOLDER_PATH = 'saved'
    __DEFAULT_ALG_PATH = os.path.join(__SAVED_FOLDER_PATH, 'alg_pred_dump')
    __DEFAULT_PARSED_DATA_PATH = os.path.join(__SAVED_FOLDER_PATH, 'parsed_data.bin')

    def __init__(self,
                 create_inited=True,
                 use_last_alg=False,
                 save_new_alg=False,
                 use_parsed_data=False,
                 save_parsed_data=False,
                 alg_path=__DEFAULT_ALG_PATH,
                 parsed_data_path=__DEFAULT_PARSED_DATA_PATH,
                 *file_paths):

        self.__offers_id_bi_map: bidict = None
        self.__algorithm: AlgoBase = None
        self.__all_predictions: list = None
        self.__user_predictions: dict = None

        if create_inited:
            self.init(use_last_alg,
                      save_new_alg,
                      use_parsed_data,
                      save_parsed_data,
                      alg_path,
                      parsed_data_path,
                      *file_paths)

    def init(self,
             use_last_alg=False,
             save_new_alg=False,
             use_parsed_data=False,
             save_parsed_data=False,
             alg_path=__DEFAULT_ALG_PATH,
             parsed_data_path=__DEFAULT_PARSED_DATA_PATH,
             *file_paths):

        parser = Parser()
        if use_parsed_data and os.path.exists(parsed_data_path):
            parsed_data = parser.load_from_file(parsed_data_path)
            print("LOADED PREVIOUSLY SAVED OFFER_ID <=> OFFER_NAME MAPPING")
            print("LOADED PREVIOUSLY SAVED DATASETS FOR TRAINING AND TESTING")
        else:
            parsed_data = parser.parse_to_file(parsed_data_path, *file_paths) \
                if save_parsed_data \
                else parser.parse(*file_paths)
            print("CREATED OFFER_ID <=> OFFER_NAME MAPPING")
            print("CREATED DATASETS FOR TRAINING AND TESTING")

        self.__offers_id_bi_map = parsed_data.offers_id_bi_map
        train_set = parsed_data.train_set
        test_set = parsed_data.test_set

        if use_last_alg and os.path.exists(alg_path):
            self.__all_predictions, self.__algorithm = dump.load(alg_path)
            print("LOADED PREVIOUSLY SAVED PREDICTIONS AND ALGORITHM")
        else:
            self.__algorithm = self.__train_algorithm(train_set)
            self.__all_predictions = self.__calculate_all_predictions(test_set)
            print("TRAINED ALGORITHM AND CALCULATED PREDICTIONS")

            if save_new_alg:
                os.makedirs(os.path.dirname(alg_path), exist_ok=True)
                dump.dump(alg_path, predictions=self.__all_predictions, algo=self.__algorithm)
                print("SAVED ALGORITHM AND PREDICTIONS TO FILE")

        self.add_rmse_results_to_file()

    def __train_algorithm(self, train_set):
        algorithm = SVD()
        algorithm.fit(train_set)
        return algorithm

    def __calculate_all_predictions(self, test_set):
        return self.__algorithm.test(test_set)

    def calculate_rmse(self, verbose=True):
        return accuracy.rmse(self.__all_predictions, verbose=verbose)

    def get_recommendations(self, given_user_id: int, top_n: int = 10):
        recommendations = []

        for user_id, offer_id, true_rating, estimation, _ in self.__all_predictions:
            if given_user_id == user_id:
                recommendations.append(Recommendation(self.__offers_id_bi_map.inv[offer_id], estimation))

        recommendations.sort(key=lambda recommendation: recommendation.estimation, reverse=True)
        return recommendations[:top_n]

    def add_rmse_results_to_file(self):
        fname = './rmse_summary.json'
        entry = {'timestamp': datetime.datetime.now().timestamp(), 'rmse': self.calculate_rmse(verbose=False)}

        if not os.path.isfile(fname):
            with open(fname, mode='w') as f:
                f.write(json.dumps([entry]))
        else:
            with open(fname) as feedsjson:
                feeds = json.load(feedsjson)

            feeds.append(entry)
            with open(fname, mode='w') as f:
                f.write(json.dumps(feeds))
