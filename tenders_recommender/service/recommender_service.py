import operator
from typing import List
from threading import Lock

from cachetools import LRUCache, cachedmethod
from surprise import Prediction, AlgoBase, SVD

from tenders_recommender.dao import UsersInteractionsDao
from tenders_recommender.model import Recommendation, Interaction, ParsedData, UsersInteractions
from tenders_recommender.parser import Parser
from tenders_recommender.recommender import Recommender
from tenders_recommender.trainer import AlgoTrainer


class RecommenderService(object):

    def __init__(self, cache_size: int):
        self.cache = LRUCache(maxsize=cache_size)
        self.__training_lock = Lock()
        self.__recommender: Recommender = None

    def populate_interactions(self, new_interactions: List[Interaction]) -> None:
        UsersInteractionsDao.insert_users_interactions(UsersInteractions(new_interactions))

    def train_algorithm(self) -> None:
        is_acquired = self.__training_lock.acquire(blocking=False)

        if is_acquired:
            try:
                all_interactions = UsersInteractionsDao.query_all_users_interactions()

                parsed_data: ParsedData = Parser.parse(all_interactions)

                algorithm: AlgoBase = SVD(
                    n_factors=50,
                    n_epochs=50,
                    biased=True,
                    init_mean=0,
                    init_std_dev=0,
                    lr_all=0.01,
                    reg_all=0.01,
                )

                all_predictions: List[Prediction] = AlgoTrainer.calc_predictions(parsed_data.train_set,
                                                                                 parsed_data.test_set,
                                                                                 algorithm)
                self.__recommender = Recommender(parsed_data.ids_offers_map, all_predictions)
                self.cache.clear()
            finally:
                self.__training_lock.release()
        else:
            raise ValueError('Algorithm is already being trained.')

    def get_rmse(self) -> float:
        return self.__recommender.calc_rmse()

    def get_recommendations(self, given_user_id: int, top_n: int = 10) -> List[Recommendation]:
        return self.__get_recommendations(given_user_id)[:top_n]

    @cachedmethod(operator.attrgetter('cache'))
    def __get_recommendations(self, given_user_id: int) -> List[Recommendation]:
        return self.__recommender.calc_recommendations(given_user_id)
