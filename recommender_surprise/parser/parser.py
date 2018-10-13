import json
import os
import pickle
from datetime import datetime
from itertools import chain
from typing import List, Tuple, Union, Dict, Iterator, Callable, Set

import dateutil.parser
from bidict import bidict
from numpy.core.multiarray import ndarray
from pandas import DataFrame
from surprise import Reader, Dataset, Trainset
from surprise.dataset import DatasetAutoFolds

from recommender_surprise.dto import ParsedData


class Parser(object):
    __USER_ID: str = 'user_id'
    __OFFER_ID: str = 'offer_id'
    __SCORE: str = 'score'
    __WHO: str = 'who'
    __WHAT: str = 'what'
    __WHEN: str = 'when'
    __TYPE: str = 'type'
    __TRACKER_FILE_FOLDER: str = os.path.join('..', 'tracker')
    __INTERACTIONS_FILE_NAMES: List[str] = [
        'observed-offers.json',
        'reported-offers.json',
        'viewed-offers.json'
    ]
    __DEFAULT_SCORE_MAP: Dict[str, float] = {
        'observed-offer': 5.0,
        'reported-offer': 2.0,
        'viewed-offer': 3.0
    }
    __DEFAULT_SCALE: Tuple[float, float] = (1, 5)

    def parse(self,
              earlier_than: datetime = None,
              score_map: Dict[str, float] = __DEFAULT_SCORE_MAP,
              rating_scale: Tuple[float, float] = __DEFAULT_SCALE,
              without_train_set: bool = False,
              *file_paths: str) -> ParsedData:

        if len(file_paths) == 0:
            file_paths: Tuple[str, ...] = tuple(os.path.join(self.__TRACKER_FILE_FOLDER, file_name) for file_name in
                                                self.__INTERACTIONS_FILE_NAMES)

        all_interactions_chain: Iterator[Dict[str, Union[str, int, float]]] = chain.from_iterable(
            [json.load(open(file_path)) for file_path in file_paths])

        is_interaction_earlier_than: Callable[Dict[str, Union[str, int, float]], bool] = \
            lambda interaction: dateutil.parser.parse(interaction[self.__WHEN]) < earlier_than

        all_interactions: Tuple[Dict[str, Union[str, int, float]], ...] = tuple(all_interactions_chain) \
            if earlier_than is None \
            else tuple(filter(is_interaction_earlier_than, all_interactions_chain))

        offers_set: Set[str] = {interaction[self.__WHAT] for interaction in all_interactions}
        offers_id_bi_map: bidict = bidict({offer_name: (index + 1) for index, offer_name in enumerate(offers_set)})

        data_frame: DataFrame = self.__create_data_frame(offers_id_bi_map, all_interactions, score_map)

        if without_train_set:
            return ParsedData(offers_id_bi_map, data_frame=data_frame)

        train_set: Trainset
        test_set: List[Tuple[str, str, Union[ndarray, float]]]
        train_set, test_set = self.__create_data_sets(data_frame, rating_scale)

        return ParsedData(offers_id_bi_map, train_set=train_set, test_set=test_set)

    def parse_to_file(self,
                      result_file_path: str,
                      score_map: Dict[str, float] = __DEFAULT_SCORE_MAP,
                      rating_scale: Tuple[float, float] = __DEFAULT_SCALE,
                      *file_paths: str) -> ParsedData:

        parsed_data: ParsedData = self.parse(score_map=score_map, rating_scale=rating_scale, *file_paths)

        dir_name: str = os.path.dirname(result_file_path)
        if dir_name is not None and dir_name != '':
            os.makedirs(dir_name, exist_ok=True)

        with open(result_file_path, 'wb') as result_file:
            pickle.dump(parsed_data, result_file)

        return parsed_data

    def load_from_file(self, result_file_path: str) -> ParsedData:
        with open(result_file_path, 'rb') as result_file:
            parsed_data: ParsedData = pickle.load(result_file)

        return parsed_data

    def __create_data_frame(self,
                            offers_id_bi_map: bidict,
                            all_interactions: Tuple[Dict[str, Union[str, int, float]], ...],
                            score_map: Dict[str, float]) -> DataFrame:
        unique_user_offer_map: Dict[Tuple[int, str], float] = {}

        for interaction in all_interactions:
            user_id: int = interaction[self.__WHO]
            offer_id: str = offers_id_bi_map[interaction[self.__WHAT]]
            score: float = score_map[interaction[self.__TYPE]]

            map_key: Tuple[int, str] = (user_id, offer_id)
            if map_key not in unique_user_offer_map or unique_user_offer_map[map_key] < score:
                unique_user_offer_map[map_key] = score

        unique_interactions_list: List[Dict[str, Union[str, int, float]]] = \
            [{self.__USER_ID: user_id, self.__OFFER_ID: offer_id, self.__SCORE: score}
             for (user_id, offer_id), score in unique_user_offer_map.items()]

        return DataFrame(unique_interactions_list)

    def __create_data_sets(self,
                           data_frame: DataFrame,
                           rating_scale: Tuple[float, float]) \
            -> Tuple[Trainset, List[Tuple[str, str, Union[ndarray, float]]]]:

        reader: Reader = Reader(rating_scale=rating_scale)
        prepared_data: DatasetAutoFolds = Dataset.load_from_df(
            data_frame[[self.__USER_ID, self.__OFFER_ID, self.__SCORE]], reader)

        train_set: Trainset = prepared_data.build_full_trainset()
        test_set: List[Tuple[str, str, Union[ndarray, float]]] = train_set.build_anti_testset()
        return train_set, test_set
