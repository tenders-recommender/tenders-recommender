from recommender_surprise.recommendation import Recommendation

import json
import os
import itertools
import pandas
from bidict import bidict

from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import accuracy
from surprise import dump
import datetime


class Recommender(object):
    __USER_ID = 'user_id'
    __OFFER_ID = 'offer_id'
    __SCORE = 'score'
    __WHO = 'who'
    __WHAT = 'what'
    __TYPE = 'type'
    __TRACKER_FILE_FOLDER = os.path.join('..', 'tracker')
    __INTERACTIONS_FILE_NAMES = [
        'observed-offers.json',
        'reported-offers.json',
        'viewed-offers.json'
    ]

    __DEFAULT_SCORE_MAP = {
        'observed-offer': 5.0,
        'reported-offer': 2.0,
        'viewed-offer': 3.0
    }
    __DEFAULT_SCALE = (1, 5)
    __DEFAULT_ALG_PATH = os.path.join('saved', 'alg_pred_dump')

    def __init__(self, create_inited=False, use_last_alg=True, alg_path=__DEFAULT_ALG_PATH,
                 score_map=__DEFAULT_SCORE_MAP, rating_scale=__DEFAULT_SCALE, *file_paths):
        self.__offers_id_bi_map: bidict = None
        self.__algorithm: SVD = None
        self.__all_predictions: list = None
        self.__user_predictions: dict = None
        if create_inited:
            self.init(use_last_alg, alg_path, score_map, rating_scale, *file_paths)

    def init(self, use_last_alg=True, alg_path=__DEFAULT_ALG_PATH,
             score_map=__DEFAULT_SCORE_MAP, rating_scale=__DEFAULT_SCALE, *file_paths):
        if len(file_paths) == 0:
            file_paths = [os.path.join(self.__TRACKER_FILE_FOLDER, file_name)
                          for file_name in self.__INTERACTIONS_FILE_NAMES]
        all_interactions_list = list(itertools.chain.from_iterable(
            [json.load(open(file_path)) for file_path in file_paths]))
        offers_set = {interaction[self.__WHAT] for interaction in all_interactions_list}

        self.__offers_id_bi_map = bidict({offer_name: (index + 1) for index, offer_name in enumerate(offers_set)})
        print("CREATED OFFER_ID <=> OFFER_NAME MAPPING")

        if use_last_alg and os.path.exists(alg_path):
            self.__all_predictions, self.__algorithm = dump.load(alg_path)
            print("LOADED PREVIOUSLY SAVED PREDICTIONS AND ALGORITHM")
        else:
            data_frame = self.__create_data_frame(all_interactions_list, score_map)
            train_set, test_set = self.__create_data_sets(data_frame, rating_scale)
            print("CREATED DATASETS FOR TRAINING AND TESTING")

            self.__algorithm = self.__train_algorithm(train_set)
            self.__all_predictions = self.__calculate_all_predictions(test_set)
            print("TRAINED ALGORITHM AND CALCULATED PREDICTIONS")

            # os.makedirs(os.path.dirname(alg_path), exist_ok=True)
            # dump.dump(alg_path, predictions=self.__all_predictions, algo=self.__algorithm)
            # print("SAVED ALGORITHM AND PREDICTIONS TO FILE")

        # self.__user_predictions = self.__create_user_predictions()
        # print("CREATED TOP PREDICTIONS FOR EVERY USER")
        self.add_rmse_results_to_file()


    def __create_data_frame(self, all_interactions_list, score_map):
        unique_user_offer_map = {}

        for interaction in all_interactions_list:
            user_id = interaction[self.__WHO]
            offer_id = self.__offers_id_bi_map[interaction[self.__WHAT]]
            score = score_map[interaction[self.__TYPE]]

            map_key = (user_id, offer_id)
            if map_key not in unique_user_offer_map or unique_user_offer_map[map_key] < score:
                unique_user_offer_map[map_key] = score

        unique_interactions_list = [{self.__USER_ID: user_id, self.__OFFER_ID: offer_id, self.__SCORE: score}
                                    for (user_id, offer_id), score in unique_user_offer_map.items()]

        return pandas.DataFrame(unique_interactions_list)

    def __create_data_sets(self, data_frame, rating_scale):
        reader = Reader(rating_scale=rating_scale)
        prepared_data = Dataset.load_from_df(data_frame[[self.__USER_ID, self.__OFFER_ID, self.__SCORE]], reader)

        train_set = prepared_data.build_full_trainset()
        test_set = train_set.build_anti_testset()
        return train_set, test_set

    def __train_algorithm(self, train_set):
        algorithm = SVD()
        algorithm.fit(train_set)
        return algorithm

    def __calculate_all_predictions(self, test_set):
        return self.__algorithm.test(test_set)

    # def __create_user_predictions(self):
    #     user_predicitons = {}
    #
    #     for user_id, offer_id, true_rating, estimation, _ in self.__all_predictions:
    #         user_predicitons.setdefault(user_id, []).append((offer_id, estimation))
    #
    #     for user_id, offers_with_scores in user_predicitons.items():
    #         offers_with_scores.sort(key=lambda pair: pair[1], reverse=True)
    #         user_predicitons[user_id] = offers_with_scores[:10]
    #
    #     return user_predicitons

    def calculate_rmse(self, verbose=True):
        return accuracy.rmse(self.__all_predictions, verbose=verbose)

    # def get_recommendations(self, user_id: int, top_n: int = 10):
    #     return self.__user_predictions[user_id][:top_n]

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
