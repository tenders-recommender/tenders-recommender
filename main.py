import json
import os
import itertools
import pandas

from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import train_test_split


USER_ID = 'user_id'
OFFER_ID = 'offer_id'
SCORE = 'score'
WHO = 'who'
WHAT = 'what'
TYPE = 'type'
TRACKER_FILE_FOLDER = 'tracker'
INTERACTIONS_FILE_NAMES = ['observed-offers.json', 'reported-offers.json', 'viewed-offers.json']


class Recommender(object):
    __DEFAULT_SCORE_MAP = {
        'observed-offer': 5.0,
        'reported-offer': 2.0,
        'viewed-offer': 3.0
    }
    __DEFAULT_SCALE = (1, 5)

    def __init__(self, score_map: dict = __DEFAULT_SCORE_MAP, rating_scale: tuple = __DEFAULT_SCALE, *file_paths):
        self.__offers_id_map: dict = None
        self.__algorithm: SVD = None
        self.__prediction: list = None
        self.init(score_map, rating_scale, *file_paths)

    def init(self, score_map: dict = __DEFAULT_SCORE_MAP, rating_scale: tuple = __DEFAULT_SCALE, *file_paths):
        if len(file_paths) == 0:
            file_paths = [os.path.join(TRACKER_FILE_FOLDER, file_name) for file_name in INTERACTIONS_FILE_NAMES]
        all_interactions_list = list(itertools.chain.from_iterable(
            [json.load(open(file_path)) for file_path in file_paths]))
        offers_set = {interaction[WHAT] for interaction in all_interactions_list}

        self.__offers_id_map = {offer_name: (index + 1) for index, offer_name in enumerate(offers_set)}

        data_frame = self.__create_data_frame(all_interactions_list, score_map)
        train_set, test_set = self.__create_data_sets(data_frame, rating_scale)

        self.__algorithm = self.__train_algorithm(train_set)
        self.__prediction = self.__calculate_prediction(test_set)

    def __create_data_frame(self, all_interactions_list, score_map):
        unique_user_offer_map = {}

        for interaction in all_interactions_list:
            user_id = interaction[WHO]
            offer_id = self.__offers_id_map[interaction[WHAT]]
            score = score_map[interaction[TYPE]]

            map_key = (user_id, offer_id)
            if map_key not in unique_user_offer_map or unique_user_offer_map[map_key] < score:
                unique_user_offer_map[map_key] = score

        unique_interactions_list = [{USER_ID: user_id, OFFER_ID: offer_id, SCORE: score}
                                    for (user_id, offer_id), score in unique_user_offer_map.items()]

        return pandas.DataFrame(unique_interactions_list)

    def __create_data_sets(self, data_frame, rating_scale):
        reader = Reader(rating_scale=rating_scale)
        prepared_data = Dataset.load_from_df(data_frame[[USER_ID, OFFER_ID, SCORE]], reader)
        return train_test_split(prepared_data, test_size=.2)

    def __train_algorithm(self, train_set):
        algorithm = SVD()
        algorithm.fit(train_set)
        return algorithm

    def __calculate_prediction(self, test_set):
        return self.__algorithm.test(test_set)

    def calculate_rmse(self, verbose=True):
        return accuracy.rmse(self.__prediction, verbose=verbose)

    def get_recommendations_for_user(self, user_id: int):
        offers_for_user = []

        for offer_name, offer_id in self.__offers_id_map.items():
            estimation = self.__algorithm.predict(user_id, offer_id).est
            offers_for_user.append((offer_name, estimation))

        offers_for_user.sort(key=lambda pair: pair[1], reverse=True)
        return offers_for_user


if __name__ == '__main__':
    recommender = Recommender()
    recommender.calculate_rmse()
    print(recommender.get_recommendations_for_user(122)[:10])
