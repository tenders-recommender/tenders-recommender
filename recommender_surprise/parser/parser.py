import itertools
import json
import os
import pickle
from datetime import datetime

import dateutil.parser
import pandas
from bidict import bidict
from surprise import Reader, Dataset

from recommender_surprise.dto import ParsedData


class Parser(object):
    __USER_ID = 'user_id'
    __OFFER_ID = 'offer_id'
    __SCORE = 'score'
    __WHO = 'who'
    __WHAT = 'what'
    __WHEN = 'when'
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

    def parse(self,
              earlier_than: datetime = None,
              score_map=__DEFAULT_SCORE_MAP,
              rating_scale=__DEFAULT_SCALE,
              without_train_set=False,
              *file_paths):

        if len(file_paths) == 0:
            file_paths = [os.path.join(self.__TRACKER_FILE_FOLDER, file_name) for file_name in
                          self.__INTERACTIONS_FILE_NAMES]

        all_interactions = itertools.chain.from_iterable([json.load(open(file_path)) for file_path in file_paths])

        if earlier_than is not None:
            all_interactions_list = list(filter(lambda interaction:
                                                dateutil.parser.parse(interaction[self.__WHEN]) < earlier_than,
                                                all_interactions))
        else:
            all_interactions_list = list(all_interactions)

        offers_set = {interaction[self.__WHAT] for interaction in all_interactions_list}
        offers_id_bi_map = bidict({offer_name: (index + 1) for index, offer_name in enumerate(offers_set)})

        data_frame = self.__create_data_frame(offers_id_bi_map, all_interactions_list, score_map)

        if without_train_set:
            return ParsedData(offers_id_bi_map, data_frame=data_frame)

        train_set, test_set = self.__create_data_sets(data_frame, rating_scale)

        return ParsedData(offers_id_bi_map, train_set, test_set)

    def parse_to_file(self,
                      result_file_path,
                      score_map=__DEFAULT_SCORE_MAP,
                      rating_scale=__DEFAULT_SCALE,
                      *file_paths):

        parsed_data = self.parse(score_map=score_map, rating_scale=rating_scale, *file_paths)

        dirname = os.path.dirname(result_file_path)
        if dirname is not None and dirname != '':
            os.makedirs(dirname, exist_ok=True)
        with open(result_file_path, 'wb') as result_file:
            pickle.dump(parsed_data, result_file)

        return parsed_data

    def load_from_file(self, result_file_path):
        with open(result_file_path, 'rb') as result_file:
            parsed_data: ParsedData = pickle.load(result_file)

        return parsed_data

    def __create_data_frame(self, offers_id_bi_map, all_interactions_list, score_map):
        unique_user_offer_map = {}

        for interaction in all_interactions_list:
            user_id = interaction[self.__WHO]
            offer_id = offers_id_bi_map[interaction[self.__WHAT]]
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
