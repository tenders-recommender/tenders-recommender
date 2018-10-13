import os
from datetime import datetime

from bidict import bidict
from surprise import AlgoBase
from surprise import SVD
from surprise import accuracy
from surprise import dump

from recommender_surprise.dto import Recommendation
from recommender_surprise.parser import Parser


class Recommender(object):
    def __init__(self,
                 algorithm: AlgoBase = SVD,
                 earlier_than: datetime = None,
                 alg_file_path: str = None,
                 parsed_data_file_path: str = None,
                 *file_names_to_parse):

        self.__algorithm: AlgoBase = algorithm
        self.__time_elapsed = None
        self.__offers_id_bi_map: bidict = None
        self.__all_predictions: list = None

        self.__alg_file_path = alg_file_path
        self.__parsed_data_file_path = parsed_data_file_path

        self.__init(earlier_than, *file_names_to_parse)

    def __init(self, earlier_than, *file_names_to_parse):
        parser = Parser()

        if self.__parsed_data_file_path is not None and os.path.exists(self.__parsed_data_file_path):
            parsed_data = parser.load_from_file(self.__parsed_data_file_path)
            print("LOADED PREVIOUSLY SAVED OFFER_ID <=> OFFER_NAME MAPPING")
            print("LOADED PREVIOUSLY SAVED DATASETS FOR TRAINING AND TESTING")
        else:
            parsed_data = parser.parse_to_file(self.__parsed_data_file_path, *file_names_to_parse) \
                if self.__parsed_data_file_path is not None \
                else parser.parse(earlier_than=earlier_than, *file_names_to_parse)
            print("CREATED OFFER_ID <=> OFFER_NAME MAPPING")
            print("CREATED DATASETS FOR TRAINING AND TESTING")

        self.__offers_id_bi_map = parsed_data.offers_id_bi_map
        train_set = parsed_data.train_set
        test_set = parsed_data.test_set

        if self.__alg_file_path is not None and os.path.exists(self.__alg_file_path):
            self.__all_predictions, self.__algorithm = dump.load(self.__alg_file_path)
            print("LOADED PREVIOUSLY SAVED PREDICTIONS AND ALGORITHM")
        else:
            before_time = datetime.now()
            self.__train_algorithm(train_set)
            self.__all_predictions = self.__calculate_all_predictions(test_set)
            print("TRAINED ALGORITHM AND CALCULATED PREDICTIONS")
            self.__time_elapsed = (datetime.now() - before_time).total_seconds()

            if self.__alg_file_path is not None:
                os.makedirs(os.path.dirname(self.__alg_file_path), exist_ok=True)
                dump.dump(self.__alg_file_path, predictions=self.__all_predictions, algo=self.__algorithm)
                print("SAVED ALGORITHM AND PREDICTIONS TO FILE")

    def __train_algorithm(self, train_set):
        self.__algorithm.fit(train_set)

    def __calculate_all_predictions(self, test_set):
        return self.__algorithm.test(test_set)

    def calculate_rmse(self, verbose=False):
        return accuracy.rmse(self.__all_predictions, verbose=verbose)

    def get_recommendations(self, given_user_id: int, top_n: int = 10):
        recommendations = []

        for user_id, offer_id, true_rating, estimation, _ in self.__all_predictions:
            if given_user_id == user_id:
                recommendations.append(Recommendation(self.__offers_id_bi_map.inv[offer_id], estimation))

        recommendations.sort(key=lambda recommendation: recommendation.estimation, reverse=True)
        return recommendations[:top_n]

    def get_time_elapsed(self):
        return self.__time_elapsed
