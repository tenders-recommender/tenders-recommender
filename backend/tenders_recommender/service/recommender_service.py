import operator
from typing import List

from cachetools import LRUCache, cachedmethod
from surprise import KNNBasic, Prediction, AlgoBase

from tenders_recommender.dto import Recommendation, Interaction, ParsedData
from tenders_recommender.parser import Parser
from tenders_recommender.recommender import Recommender
from tenders_recommender.trainer import AlgoTrainer


class RecommenderService(object):

    def __init__(self, cache_size: int):
        self.cache = LRUCache(maxsize=cache_size)
        self.__interactions: List[Interaction] = []
        self.__recommender: Recommender = None

    def populate_interactions(self, new_interactions: List[Interaction]):
        self.__interactions.extend(new_interactions)

    def train_algorithm(self, interactions: List[Interaction] = None):
        if not interactions:
            interactions = self.__interactions.copy()
        self.__interactions.clear()

        parsed_data: ParsedData = Parser.parse(interactions)

        algorithm: AlgoBase = KNNBasic(
            k=45,
            min_k=1,
            sim_options={
                'name': 'pearson',
                'min_support': 1,
                'user_based': True
            }
        )

        all_predictions: List[Prediction] = AlgoTrainer.calc_predictions(parsed_data.train_set,
                                                                         parsed_data.test_set,
                                                                         algorithm)
        self.__recommender = Recommender(parsed_data.ids_offers_map, all_predictions)
        self.cache.clear()

    @cachedmethod(operator.attrgetter('cache'))
    def get_rmse(self) -> float:
        return self.__recommender.calc_rmse()

    def get_recommendations(self, given_user_id: int, top_n: int = 10) -> List[Recommendation]:
        return self.__get_recommendations(given_user_id)[:top_n]

    @cachedmethod(operator.attrgetter('cache'))
    def __get_recommendations(self, given_user_id: int) -> List[Recommendation]:
        return self.__recommender.calc_recommendations(given_user_id)
