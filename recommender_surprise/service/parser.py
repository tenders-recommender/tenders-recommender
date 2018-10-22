from datetime import datetime
from typing import List, Tuple, Dict, Callable, Set

import dateutil.parser
from bidict import bidict
from pandas import DataFrame
from surprise import Reader, Dataset, Trainset
from surprise.dataset import DatasetAutoFolds

from recommender_surprise.dto import ParsedData, Interaction, Testset


class Parser(object):
    __USER_ID: str = 'user_id'
    __OFFER_ID: str = 'offer_id'
    __SCORE: str = 'score'
    __WHO: str = 'who'
    __WHAT: str = 'what'
    __WHEN: str = 'when'
    __TYPE: str = 'type'

    __DEFAULT_SCORE_MAP: Dict[str, float] = {
        'observed-offer': 5.0,
        'reported-offer': 2.0,
        'viewed-offer': 3.0
    }
    __DEFAULT_SCALE: Tuple[float, float] = (1, 5)

    def parse(self,
              all_interactions: List[Interaction],
              earlier_than: datetime = None,
              score_map: Dict[str, float] = __DEFAULT_SCORE_MAP,
              rating_scale: Tuple[float, float] = __DEFAULT_SCALE) -> ParsedData:

        is_interaction_earlier_than: Callable[Interaction, bool] = lambda interaction: \
            dateutil.parser.parse(interaction[self.__WHEN]) < earlier_than

        filtered_interactions: List[Interaction] = list(filter(is_interaction_earlier_than, all_interactions)) \
            if earlier_than is not None \
            else all_interactions

        offers_set: Set[str] = {interaction[self.__WHAT] for interaction in all_interactions}
        offers_id_bi_map: bidict = bidict({offer_name: (index + 1) for index, offer_name in enumerate(offers_set)})

        data_frame: DataFrame = self.__create_data_frame(offers_id_bi_map, filtered_interactions, score_map)
        train_set, test_set = self.__create_data_sets(data_frame, rating_scale)

        return ParsedData(offers_id_bi_map, train_set=train_set, test_set=test_set)

    def __create_data_frame(self,
                            offers_id_bi_map: bidict,
                            interactions: List[Interaction],
                            score_map: Dict[str, float]) -> DataFrame:
        unique_user_offer_map: Dict[Tuple[int, str], float] = {}

        for interaction in interactions:
            user_id: int = interaction[self.__WHO]
            offer_id: str = offers_id_bi_map[interaction[self.__WHAT]]
            score: float = score_map[interaction[self.__TYPE]]

            map_key: Tuple[int, str] = (user_id, offer_id)
            if map_key not in unique_user_offer_map or unique_user_offer_map[map_key] < score:
                unique_user_offer_map[map_key] = score

        unique_interactions_list: List[Interaction] = \
            [{self.__USER_ID: user_id, self.__OFFER_ID: offer_id, self.__SCORE: score}
             for (user_id, offer_id), score in unique_user_offer_map.items()]

        return DataFrame(unique_interactions_list)

    def __create_data_sets(self,
                           data_frame: DataFrame,
                           rating_scale: Tuple[float, float]) -> Tuple[Trainset, Testset]:
        reader: Reader = Reader(rating_scale=rating_scale)

        prepared_data: DatasetAutoFolds = Dataset.load_from_df(
            data_frame[[self.__USER_ID, self.__OFFER_ID, self.__SCORE]], reader)

        train_set: Trainset = prepared_data.build_full_trainset()
        test_set: Testset = train_set.build_testset()
        return train_set, test_set
