from typing import List

from surprise import AlgoBase, Trainset, Prediction

from dto import Testset


class AlgoTrainer(object):
    @staticmethod
    def calc_predictions(train_set: Trainset,
                         test_set: Testset,
                         algorithm: AlgoBase) -> List[Prediction]:
        AlgoTrainer.__train_algorithm(algorithm, train_set)
        return AlgoTrainer.__calc_all_predictions(algorithm, test_set)

    @staticmethod
    def __train_algorithm(algorithm: AlgoBase, train_set: Trainset) -> None:
        algorithm.fit(train_set)

    @staticmethod
    def __calc_all_predictions(algorithm: AlgoBase, test_set: Testset) -> List[Prediction]:
        return algorithm.test(test_set)
