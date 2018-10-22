import operator
from threading import RLock
from typing import List

from cachetools import LRUCache, cachedmethod
from surprise import KNNBasic, Prediction, AlgoBase

from recommender_surprise.dto import Recommendation, Interaction, ParsedData
from recommender_surprise.service.parser import Parser
from recommender_surprise.service.algo_trainer import AlgoTrainer
from recommender_surprise.service.recommender import Recommender


class RecommenderService(object):

    def __init__(self, cache_size: int):
        self.cache = LRUCache(maxsize=cache_size)
        self.__interactions: List[Interaction] = []
        self.__recommender: Recommender = None

    def populate_interactions(self, new_interactions: List[Interaction]):
        self.__interactions += new_interactions

    def train_algorithm(self):
        parser: Parser = Parser()
        parsed_data: ParsedData = parser.parse(self.__interactions)

        algo: AlgoBase = KNNBasic(
            k=45,
            min_k=1,
            sim_options={
                'name': 'pearson',
                'min_support': 1,
                'user_based': True
            }
        )
        all_predictions: List[Prediction] = AlgoTrainer.train(parsed_data.train_set, parsed_data.test_set, algo)

        self.__recommender = Recommender(parsed_data.offers_id_bi_map.inv, all_predictions)
        self.cache.clear()

    @cachedmethod(operator.attrgetter('cache'))
    def get_rmse(self) -> float:
        return self.__recommender.calc_rmse()

    def get_recommendations(self, given_user_id: int, top_n: int = 10) -> List[Recommendation]:
        return self.__get_recommendations(given_user_id)[:top_n]

    @cachedmethod(operator.attrgetter('cache'))
    def __get_recommendations(self, given_user_id: int) -> List[Recommendation]:
        return self.__recommender.calc_recommendations(given_user_id)