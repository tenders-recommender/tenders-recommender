from collections import OrderedDict
from types import MappingProxyType
from typing import List, Tuple, Dict

from pandas import DataFrame
from surprise import Reader, Dataset, Trainset
from surprise.dataset import DatasetAutoFolds

from tenders_recommender.dto import ParsedData, Interaction, Testset

USER_ID: str = 'user_id'
OFFER_ID: str = 'offer_id'
SCORE: str = 'score'
WHO: str = 'who'
WHAT: str = 'what'
WHEN: str = 'when'
TYPE: str = 'type'

DEFAULT_SCORE_MAP = MappingProxyType({
    'observed-offer': 5.0,
    'reported-offer': 5.0,
    'viewed-offer': 4.0
})
DEFAULT_SCALE: Tuple[float, float] = (1, 5)


class Parser(object):

    @staticmethod
    def parse(all_interactions: List[Interaction],
              score_map: Dict[str, float] = DEFAULT_SCORE_MAP,
              rating_scale: Tuple[float, float] = DEFAULT_SCALE) -> ParsedData:
        unique_offers = list(OrderedDict.fromkeys(map(lambda interaction: interaction[WHAT], all_interactions)))
        offers_ids_map: Dict[str, int] = {offer_name: (index + 1) for index, offer_name in enumerate(unique_offers)}

        data_frame: DataFrame = Parser.__create_data_frame(offers_ids_map, all_interactions, score_map)
        whole_data_set, train_set, test_set = Parser.__create_data_sets(data_frame, rating_scale)
        ids_offers_map: Dict[int, str] = {value: key for key, value in offers_ids_map.items()}

        return ParsedData(ids_offers_map, whole_data_set=whole_data_set, train_set=train_set, test_set=test_set)

    @staticmethod
    def __create_data_frame(offers_ids_map: Dict[str, int],
                            interactions: List[Interaction],
                            score_map: Dict[str, float]) -> DataFrame:
        unique_user_offer_map: Dict[Tuple[int, int], float] = {}

        for interaction in interactions:
            user_id: int = interaction[WHO]
            offer_id: int = offers_ids_map[interaction[WHAT]]
            score: float = score_map[interaction[TYPE]]

            map_key: Tuple[int, int] = (user_id, offer_id)
            if map_key not in unique_user_offer_map or unique_user_offer_map[map_key] < score:
                unique_user_offer_map[map_key] = score

        unique_interactions_list: List[Interaction] = \
            [{USER_ID: u_id, OFFER_ID: o_id, SCORE: s}
             for (u_id, o_id), s in unique_user_offer_map.items()]

        return DataFrame(unique_interactions_list)

    @staticmethod
    def __create_data_sets(data_frame: DataFrame,
                           rating_scale: Tuple[float, float]) -> Tuple[DatasetAutoFolds, Trainset, Testset]:
        reader: Reader = Reader(rating_scale=rating_scale)

        whole_data_set: DatasetAutoFolds = Dataset.load_from_df(
            data_frame[[USER_ID, OFFER_ID, SCORE]], reader)

        train_set: Trainset = whole_data_set.build_full_trainset()
        test_set: Testset = train_set.build_anti_testset()
        return whole_data_set, train_set, test_set
