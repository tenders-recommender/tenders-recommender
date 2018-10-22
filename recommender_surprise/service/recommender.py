from typing import Dict, List

from surprise import Prediction, accuracy

from recommender_surprise.dto import Recommendation


class Recommender(object):

    def __init__(self, id_offers_map: Dict[int, str], all_predictions: List[Prediction]):
        self.__id_offers_map = id_offers_map
        self.__all_predictions = all_predictions

    def calc_rmse(self, verbose: bool = False) -> float:
        return accuracy.rmse(self.__all_predictions, verbose=verbose)

    def calc_recommendations(self, given_user_id: int) -> List[Recommendation]:
        recommendations: List[Recommendation] = []

        for user_id, offer_id, true_rating, estimation, _ in self.__all_predictions:
            if given_user_id == user_id:
                recommendations.append(Recommendation(self.__id_offers_map[offer_id], estimation))

        recommendations.sort(key=lambda recommendation: recommendation.estimation, reverse=True)
        return recommendations
