from datetime import datetime
from typing import List, Tuple, Dict, Callable, Set

import dateutil.parser
from pandas import DataFrame
from surprise import Reader, Dataset, Trainset
from surprise.dataset import DatasetAutoFolds

from dto import ParsedData, Interaction, Testset


USER_ID: str = 'user_id'
OFFER_ID: str = 'offer_id'
SCORE: str = 'score'
WHO: str = 'who'
WHAT: str = 'what'
WHEN: str = 'when'
TYPE: str = 'type'

DEFAULT_SCORE_MAP: Dict[str, float] = {
    'observed-offer': 5.0,
    'reported-offer': 2.0,
    'viewed-offer': 3.0
}
DEFAULT_SCALE: Tuple[float, float] = (1, 5)


class Parser(object):

    @staticmethod
    def parse(all_interactions: List[Interaction],
              earlier_than: datetime = None,
              score_map: Dict[str, float] = DEFAULT_SCORE_MAP,
              rating_scale: Tuple[float, float] = DEFAULT_SCALE) -> ParsedData:

        is_interaction_earlier_than: Callable[Interaction, bool] = lambda interaction: \
            dateutil.parser.parse(interaction[WHEN]) < earlier_than

        filtered_interactions: List[Interaction] = list(filter(is_interaction_earlier_than, all_interactions)) \
            if earlier_than is not None \
            else all_interactions

        offers_set: Set[str] = {interaction[WHAT] for interaction in all_interactions}
        offers_ids_map: Dict[str, int] = {offer_name: (index + 1) for index, offer_name in enumerate(offers_set)}

        data_frame: DataFrame = Parser.__create_data_frame(offers_ids_map, filtered_interactions, score_map)
        train_set, test_set = Parser.__create_data_sets(data_frame, rating_scale)
        ids_offers_map: Dict[int, str] = {value: key for key, value in offers_ids_map.items()}

        return ParsedData(ids_offers_map, train_set=train_set, test_set=test_set)

    @staticmethod
    def __create_data_frame(offers_ids_map: Dict[str, int],
                            interactions: List[Interaction],
                            score_map: Dict[str, float]) -> DataFrame:
        unique_user_offer_map: Dict[Tuple[int, str], float] = {}

        for interaction in interactions:
            user_id: int = interaction[WHO]
            offer_id: str = offers_ids_map[interaction[WHAT]]
            score: float = score_map[interaction[TYPE]]

            map_key: Tuple[int, str] = (user_id, offer_id)
            if map_key not in unique_user_offer_map or unique_user_offer_map[map_key] < score:
                unique_user_offer_map[map_key] = score

        unique_interactions_list: List[Interaction] = \
            [{USER_ID: user_id, OFFER_ID: offer_id, SCORE: score}
             for (user_id, offer_id), score in unique_user_offer_map.items()]

        return DataFrame(unique_interactions_list)

    @staticmethod
    def __create_data_sets(data_frame: DataFrame,
                           rating_scale: Tuple[float, float]) -> Tuple[Trainset, Testset]:
        reader: Reader = Reader(rating_scale=rating_scale)

        prepared_data: DatasetAutoFolds = Dataset.load_from_df(
            data_frame[[USER_ID, OFFER_ID, SCORE]], reader)

        train_set: Trainset = prepared_data.build_full_trainset()
        test_set: Testset = train_set.build_testset()
        return train_set, test_set
